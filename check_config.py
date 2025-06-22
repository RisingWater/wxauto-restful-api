#!/usr/bin/env python3
"""
wxauto API 配置检查脚本
验证配置文件并显示当前配置信息
"""

import sys
from pathlib import Path
from app.utils.config import settings
from app.utils.logger import setup_logger

def check_config() -> None:
    """检查配置文件并显示配置信息"""
    logger = setup_logger()
    
    print("=" * 50)
    print("wxauto API 配置检查")
    print("=" * 50)
    
    # 检查配置文件是否存在
    config_path = Path("config.yaml")
    if config_path.exists():
        print(f"✓ 配置文件存在: {config_path}")
    else:
        print(f"⚠ 配置文件不存在: {config_path}")
        print("  将使用默认配置")
    
    print("\n服务器配置:")
    print(f"  主机地址: {settings.server.host}")
    print(f"  端口: {settings.server.port}")
    print(f"  热重载: {'启用' if settings.server.reload else '禁用'}")
    
    print(f"\nAPI配置:")
    print(f"  API前缀: {settings.api.prefix}")
    print(f"  文档地址: http://{settings.server.host}:{settings.server.port}{settings.api.docs_url}")
    print(f"  ReDoc地址: http://{settings.server.host}:{settings.server.port}{settings.api.redoc_url}")
    
    print(f"\n数据库配置:")
    print(f"  数据库类型: {settings.database.type}")
    if settings.database.type == "sqlite":
        print(f"  数据库路径: {settings.database.sqlite.path}")
    
    print(f"\n文件上传配置:")
    print(f"  上传目录: {settings.upload.base_dir}")
    print(f"  最大文件大小: {settings.upload.max_size} bytes ({settings.upload.max_size / 1024 / 1024:.1f} MB)")
    
    print(f"\n日志配置:")
    print(f"  日志级别: {settings.logging.level}")
    print(f"  日志文件: {settings.logging.file}")
    
    print(f"\n认证配置:")
    print(f"  API令牌: {'已设置' if settings.auth.token != 'your-secret-token-here' else '使用默认值'}")
    
    print("\n" + "=" * 50)
    print("配置检查完成")
    print("=" * 50)

if __name__ == "__main__":
    try:
        check_config()
    except Exception as e:
        print(f"配置检查失败: {e}")
        sys.exit(1) 