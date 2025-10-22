import os
import hashlib
from datetime import datetime
from typing import Optional, Tuple, List
from fastapi import UploadFile, HTTPException
from app.models.file import FileInfo, FileUploadResponse
from app.models.base import QueryParams
from app.database.factory import DatabaseFactory
from app.utils.config import settings
import shutil

class FileService:
    """文件服务"""
    
    def __init__(self) -> None:
        """初始化文件服务"""
        self.db = DatabaseFactory.get_database()
        self.base_dir = settings.upload.base_dir
        self.max_size = settings.upload.max_size
        self.allowed_types = settings.upload.allowed_types
        self.chunk_size = settings.upload.chunk_size
        
        # 确保上传目录存在
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
            
        # 创建文件表
        self.db.create_table("files", {
            "id": "TEXT PRIMARY KEY",
            "filename": "TEXT NOT NULL",
            "file_type": "TEXT NOT NULL",
            "file_size": "INTEGER NOT NULL",
            "file_hash": "TEXT NOT NULL",
            "file_path": "TEXT NOT NULL",
            "upload_time": "TIMESTAMP NOT NULL",
            "description": "TEXT",
            "uploader": "TEXT",
            "download_count": "INTEGER DEFAULT 0",
            "is_deleted": "INTEGER DEFAULT 0"
        })
        
    def _calculate_hash(self, file: UploadFile) -> str:
        """计算文件哈希值
        
        Args:
            file: 上传的文件
            
        Returns:
            str: 文件哈希值
        """
        sha256 = hashlib.sha256()
        while chunk := file.file.read(self.chunk_size):
            sha256.update(chunk)
        file.file.seek(0)  # 重置文件指针
        return sha256.hexdigest()

    def _calculate_hash_by_path(self, file_path: str) -> str:
        """计算本地文件的哈希值
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 文件的SHA256哈希值
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(self.chunk_size):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
        
    def _get_file_path(self, file_hash: str, filename: str) -> str:
        """获取文件存储路径
        
        Args:
            file_hash: 文件哈希值
            filename: 原始文件名
            
        Returns:
            str: 文件存储路径
        """
        # 使用哈希值作为子目录
        sub_dir = os.path.join(self.base_dir, file_hash)
        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)
            
        # 获取文件扩展名
        _, ext = os.path.splitext(filename)
        return os.path.join(sub_dir, filename)
        
    def _validate_file(self, file: UploadFile) -> None:
        """验证文件
        
        Args:
            file: 上传的文件
            
        Raises:
            HTTPException: 文件验证失败
        """
        # 检查文件大小
        file_size = 0
        while chunk := file.file.read(self.chunk_size):
            file_size += len(chunk)
            if file_size > self.max_size:
                raise HTTPException(status_code=400, detail="文件大小超过限制")
        file.file.seek(0)
        
        # 检查文件类型
        if self.allowed_types and file.content_type not in self.allowed_types:
            raise HTTPException(status_code=400, detail="不支持的文件类型")

    def _validate_file_by_path(self, file_path: str) -> str:
        """验证文件
        
        Args:
            file_path: 文件路径
            
        Raises:
            ValueError: 文件验证失败
            FileNotFoundError: 文件不存在
        """
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 检查文件读取权限
        if not os.access(file_path, os.R_OK):
            raise ValueError(f"没有文件读取权限: {file_path}")
        
        # 检查文件大小
        file_size = os.path.getsize(file_path)
        if file_size > self.max_size:
            raise ValueError(f"文件大小超过限制: {file_size} > {self.max_size}")

        import mimetypes
        file_type, _ = mimetypes.guess_type(file_path)

        # 检查文件类型
        if self.allowed_types:
            if file_type not in self.allowed_types:
                raise ValueError(f"不支持的文件类型: {file_type}")
            
        return file_type or "application/octet-stream"
            
    async def upload_file(
        self,
        file: UploadFile,
        description: Optional[str] = None,
        uploader: Optional[str] = None
    ) -> FileUploadResponse:
        """上传文件
        
        Args:
            file: 上传的文件
            description: 文件描述
            uploader: 上传者
            
        Returns:
            FileUploadResponse: 文件上传响应
        """
        # 验证文件
        self._validate_file(file)
        
        # 计算文件哈希值
        file_hash = self._calculate_hash(file)
        
        # 获取文件存储路径
        file_path = self._get_file_path(file_hash, file.filename)
        
        # 检查文件是否已存在
        existing_file = self.db.get_by_id("files", file_hash)
        if existing_file:
            # 文件已存在，返回现有文件信息
            return FileUploadResponse(
                file_id=existing_file["id"],
                filename=existing_file["filename"],
                file_type=existing_file["file_type"],
                file_size=existing_file["file_size"],
                file_hash=existing_file["file_hash"],
                file_path=existing_file["file_path"],
                upload_time=existing_file["upload_time"],
                is_new=False
            )
            
        # 保存文件
        with open(file_path, "wb") as f:
            while chunk := file.file.read(self.chunk_size):
                f.write(chunk)
                
        file_type = file.content_type or "application/octet-stream"

        # 记录文件信息
        file_info = {
            "id": file_hash,
            "filename": file.filename,
            "file_type": file_type,
            "file_size": os.path.getsize(file_path),
            "file_hash": file_hash,
            "file_path": file_path,
            "upload_time": datetime.now().isoformat(),
            "description": description,
            "uploader": uploader,
            "download_count": 0,
            "is_deleted": 0
        }
        
        self.db.insert("files", file_info)
        
        return FileUploadResponse(
            file_id=file_info["id"],
            filename=file_info["filename"],
            file_type=file_info["file_type"],
            file_size=file_info["file_size"],
            file_hash=file_info["file_hash"],
            file_path=file_info["file_path"],
            upload_time=file_info["upload_time"],
            is_new=True
        )
        
    def get_file(self, file_id: str) -> Optional[FileInfo]:
        """获取文件信息
        
        Args:
            file_id: 文件ID
            
        Returns:
            Optional[FileInfo]: 文件信息
        """
        file_info = self.db.get_by_id("files", file_id)
        if not file_info or file_info["is_deleted"]:
            return None
        return FileInfo(**file_info)
        
    def delete_file(self, file_id: str) -> bool:
        """删除文件
        
        Args:
            file_id: 文件ID
            
        Returns:
            bool: 是否删除成功
        """
        return self.db.update("files", file_id, {"is_deleted": 1})
        
    def list_files(self, skip: int = 0, limit: int = 100) -> Tuple[int, List[FileInfo]]:
        """列出文件
        
        Args:
            skip: 跳过数量
            limit: 限制数量
            
        Returns:
            Tuple[int, List[FileInfo]]: 总数和文件列表
        """
        params = QueryParams(
            skip = skip,
            limit = limit,
            filters = {"is_deleted": 0},
            sort_by = "upload_time",
            sort_order = "DESC"
        )
        result = self.db.query("files", params)
        return result.total, [FileInfo(**item) for item in result.items] 
    
    async def download_file(self, file_id: str) -> Tuple[str, str, str]:
        """下载文件
        
        Args:
            file_id: 文件ID
            
        Returns:
            Tuple[str, str, str]: (文件路径, 文件名, 内容类型)
            
        Raises:
            HTTPException: 文件不存在或已被删除
        """
        # 获取文件信息
        file_info = self.db.get_by_id("files", file_id)
        
        if not file_info or file_info["is_deleted"]:
            raise HTTPException(status_code=404, detail="文件不存在或已被删除")
        
        # 检查文件是否实际存在
        file_path = file_info["file_path"]
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 更新下载次数
        self.db.update("files", file_id, {
            "download_count": file_info["download_count"] + 1
        })
        
        return (
            file_path, 
            file_info["filename"], 
            file_info["file_type"]
        )

    def upload_file_by_path(
        self,
        file_path: str,
        description: Optional[str] = None,
        uploader: Optional[str] = None
    ) -> dict:
        """通过文件路径上传文件
        
        Args:
            file_path: 本地文件路径
            description: 文件描述
            uploader: 上传者
            
        Returns:
            dict: 文件信息字典
            
        Raises:
            FileNotFoundError: 当文件不存在时
            PermissionError: 当没有文件读取权限时
        """
        
        # 验证文件
        file_type = self._validate_file_by_path(file_path)
        
        # 获取文件名
        filename = os.path.basename(file_path)
        
        # 计算文件哈希值
        file_hash = self._calculate_hash_by_path(file_path)
        
        # 获取文件存储路径（复制到指定位置）
        target_path = self._get_file_path(file_hash, filename)
        
        # 检查文件是否已存在
        existing_file = self.db.get_by_id("files", file_hash)
        if existing_file:
            # 文件已存在，返回现有文件信息
            return {
                "file_id": existing_file["id"],
                "filename": existing_file["filename"],
                "file_type": existing_file["file_type"],
                "file_size": existing_file["file_size"],
                "file_hash": existing_file["file_hash"],
                "file_path": existing_file["file_path"],
                "upload_time": existing_file["upload_time"],
                "description": existing_file.get("description"),
                "uploader": existing_file.get("uploader"),
                "is_new": False
            }
        
        # 复制文件到目标位置
        shutil.copy2(file_path, target_path)
                
        # 记录文件信息
        file_info = {
            "id": file_hash,
            "filename": filename,
            "file_type": file_type,
            "file_size": os.path.getsize(target_path),
            "file_hash": file_hash,
            "file_path": target_path,
            "upload_time": datetime.now().isoformat(),
            "description": description,
            "uploader": uploader,
            "download_count": 0,
            "is_deleted": 0
        }
        
        self.db.insert("files", file_info)
        
        return {
            "file_id": file_info["id"],
            "filename": file_info["filename"],
            "file_type": file_info["file_type"],
            "file_size": file_info["file_size"],
            "file_hash": file_info["file_hash"],
            "file_path": file_info["file_path"],
            "upload_time": file_info["upload_time"],
            "description": file_info["description"],
            "uploader": file_info["uploader"],
            "is_new": True
        }