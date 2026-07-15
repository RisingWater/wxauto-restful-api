from app.utils.wx_package_manager import has_feature
from typing import Optional, Union, List
from fastapi.responses import FileResponse, Response
from app.models.response import APIResponse
from app.services.file_service import FileService
from .init import WeChat, WxClient, WeChatLogin, Chat, HumanMessage
from PIL import Image
import tempfile
import shutil
import os
import win32gui
import ctypes
from ctypes import wintypes

# 初始化
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# 函数声明
kernel32.OpenEventW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
kernel32.OpenEventW.restype = wintypes.HANDLE
kernel32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
kernel32.WaitForSingleObject.restype = wintypes.DWORD
kernel32.ResetEvent.argtypes = [wintypes.HANDLE]
kernel32.ResetEvent.restype = wintypes.BOOL
kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
kernel32.CloseHandle.restype = wintypes.BOOL

# Windows API
user32 = ctypes.WinDLL('user32', use_last_error=True)

# 常量
SW_SHOWMINIMIZED = 2   # 最小化
SW_RESTORE = 9         # 还原

def minimize_window(hwnd):
    """最小化窗口"""
    if not hwnd:
        return False
    
    # 参数1: HWND, 参数2: 显示命令
    result = user32.ShowWindow(hwnd, SW_SHOWMINIMIZED)
    return bool(result)

def restore_window(hwnd):
    """还原窗口（从最小化/最大化恢复）"""
    if not hwnd:
        return False
    
    result = user32.ShowWindow(hwnd, SW_RESTORE)
    return bool(result)

def check_and_reset_wechat_event():
    """检查微信消息Event是否被触发，如果是则Reset"""
    event_name = "Global\\TrayMonitor_RecvMessageEvent"
    
    # 1. 打开Event
    h_event = kernel32.OpenEventW(
        0x1F0003,       # EVENT_ALL_ACCESS
        False,          # 不继承
        event_name
    )
    
    if not h_event:
        print(f"无法打开Event: {event_name}")
        return False
    
    # 2. 立即检查（不等待）
    result = kernel32.WaitForSingleObject(h_event, 0)
    
    if result == 0:  # WAIT_OBJECT_0
        # 3. Event被触发，Reset它
        kernel32.ResetEvent(h_event)
        print("检测到微信新消息，Event已Reset")
        return True
    else:
        print("未检测到新消息")
        return False

    # 4. 关闭句柄
    kernel32.CloseHandle(h_event)

def get_wechat(wxname: str) -> WeChat:
    """获取微信实例
    
    Args:
        wxname: 微信客户端名称
        
    Returns:
        WeChat实例
    """
    # 检查字典是否为空或者实例无效
    if WxClient:  # 字典不为空
        # 获取第一个实例
        cached_key = list(WxClient.keys())[0]
        cached_wx = WxClient[cached_key]
        # 检查窗口是否可用
        if not win32gui.IsWindow(cached_wx.core.HWND):
            print(f"微信窗口实例已不存在，清空缓存准备重建实例")
            WxClient.clear()  # 清空字典

    if not WxClient:  # 字典为空（要么本来空，要么刚被清空）
        print(f"重建微信窗口实例")
        try:
            wx = WeChat() # 这里失败也会抛出异常
        except Exception as e:
            print(f"创建微信窗口实例失败，窗口不存在，需要登录: {e}")
            raise  # 直接重新抛出相同的异常

        if win32gui.IsWindow(wx.core.HWND):
            WxClient["default"] = wx  # 添加键值对
        else:
            print(f"微信窗口异常，窗口不存在")
            raise Exception("微信窗口异常，微信窗口不存在")

    return list(WxClient.values())[0]  # 返回第一个（也是唯一一个）值

def get_wechat_login() -> WeChatLogin:
    """获取微信实例
        
    Returns:
        WeChatLogin实例
    """
    wx = WeChatLogin()
    return wx

def get_wechat_subwin(wxname: str, who: str) -> Optional[Chat]:
    """获取微信子窗口
    
    Args:
        wxname: 微信客户端名称
        who: 聊天对象
        
    Returns:
        Chat实例或None
    """
    wx = get_wechat(wxname)
    subwins = wx.GetAllSubWindow()
    if targets := [i for i in subwins if i.who == who]:
        return targets[0]
    else:
        return None

class WeChatService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WeChatService, cls).__new__(cls)
        return cls._instance

    def send_message(
            self, 
            msg: str,
            who: Optional[str] = None, 
            clear: bool = True, 
            at: Optional[Union[str, list]] = None, 
            exact: bool = False, 
            wxname: Optional[str] = None
        ) -> APIResponse:
        """发送消息"""
        try:
            wx = get_wechat(wxname)
            restore_window(wx.core.HWND)
            result = wx.SendMsg(msg=msg, who=who, clear=clear, at=at, exact=exact)
            minimize_window(wx.core.HWND)
            return APIResponse(success=bool(result), message=result['message'], data=result['data'])
        except Exception as e:
            return APIResponse(success=False, message=str(e))

    def send_file(
            self,
            file_id: str,
            who: Optional[str] = None,
            exact: bool = False,
            wxname: Optional[str] = None
        ) -> APIResponse:
        """发送文件"""
        try:
            # 获取文件信息
            file_service = FileService()
            file_info = file_service.get_file(file_id)
            if not file_info:
                return APIResponse(success=False, message="文件不存在")
            
            # 检查文件是否存在
            if not file_info.file_path or not os.path.exists(file_info.file_path):
                return APIResponse(success=False, message="文件路径不存在")
            
            # 发送文件
            wx = get_wechat(wxname)

            restore_window(wx.core.HWND)

            result = wx.SendFiles(filepath=file_info.file_path, who=who, exact=exact)

            minimize_window(wx.core.HWND)
            
            if result:
                return APIResponse(
                    success=True, 
                    message="文件发送成功", 
                    data={
                        "file_id": file_id,
                        "filename": file_info.filename,
                        "file_path": file_info.file_path,
                        "recipient": who
                    }
                )
            else:
                return APIResponse(success=False, message="文件发送失败")
                
        except Exception as e:
            return APIResponse(success=False, message=f"发送文件时发生错误: {str(e)}")

    def chat_with(
            self, 
            who: str,
            exact: bool = False,
            wxname: Optional[str] = None
        ) -> APIResponse:
        """切换聊天窗口"""
        try:
            wx = get_wechat(wxname)
            result = wx.ChatWith(who=who, exact=exact)
            if result:
                return APIResponse(success=True, message='主窗口聊天切换成功', data={'chatname': result})
            else:
                return APIResponse(success=False, message='主窗口聊天切换失败')
        except Exception as e:
            return APIResponse(success=False, message=str(e))

    def get_all_sub_window(
            self,
            wxname: Optional[str] = None
        ) -> APIResponse:
        """获取所有子窗口"""
        try:
            wx = get_wechat(wxname)
            result = wx.GetAllSubWindow()
            data = [{'name': i.who, 'type': i.chat_type} for i in result]
            return APIResponse(success=True, message='', data=data)
        except Exception as e:
            return APIResponse(success=False, message=str(e))

    def get_all_message(
            self,
            who: str,
            wxname: Optional[str] = None
        ) -> APIResponse:
        """获取所有消息"""
        try:
            wx = get_wechat(wxname)
            if who:
                if not wx.ChatWith(who):
                    return APIResponse(success=False, message='找不到聊天窗口')
            result = wx.ChatInfo()
            msgs = wx.GetAllMessage()
            result['msg'] = [msg.info for msg in msgs]
            return APIResponse(success=True, message='', data=result)
        except Exception as e:
            return APIResponse(success=False, message=str(e))

    # wxautox特有功能
    def send_url_card(
            self,
            url: str,
            friends: Union[str, List[str]],
            timeout: int = 10,
            wxname: Optional[str] = None
        ) -> APIResponse:
        """发送URL卡片（wxautox特有）"""
        if not has_feature("send_url_card"):
            return APIResponse(success=False, message="此功能需要wxautox版本支持")
        
        try:
            wx = get_wechat(wxname)
            result = wx.SendUrlCard(url=url, friends=friends, timeout=timeout)
            return APIResponse(success=bool(result), message=result['message'], data=result['data'])
        except Exception as e:
            return APIResponse(success=False, message=str(e))
        
    def add_listen_chat(
            self,
            who: str,
            wxname: Optional[str] = None
        ) -> APIResponse:
        """添加监听聊天"""
        
        try:
            wx = get_wechat(wxname)
            if who in [i.who for i in wx.GetAllSubWindow()]:
                return APIResponse(success=False, message='该聊天已监听中')
            wxapi = wx._api if hasattr(wx, '_api') else wx.core
            subwin = wxapi.open_separate_window(who)
            if subwin is None:
                return APIResponse(success=False, message='找不到聊天窗口')
            return APIResponse(success=True, message=f'{who} 聊天窗口已添加监听')
        except Exception as e:
            return APIResponse(success=False, message=str(e))
        
    def get_next_new_message(
        self,
        filter_mute: bool = False,
        wxname: Optional[str] = None
    ) -> APIResponse:
        """获取下一个新消息，并自动下载媒体文件和转换语音"""

        recved_event = check_and_reset_wechat_event()
        if not recved_event:
            return APIResponse(success=True, message='', data={})
    
        try:
            wx = get_wechat(wxname)
            restore_window(wx.core.HWND)
            result = wx.GetNextNewMessage(filter_mute=filter_mute)
            
            if result and 'msg' in result:
                processed_messages = []
                
                for msg in result['msg']:
                    msg_info = msg.info
                    msg_info['raw'] = msg
                    msg_class_name = msg.__class__.__name__

                    if hasattr(msg, 'sender_remark'):
                        msg_info.update({
                            "sender_remark": msg.sender_remark
                        })
                    
                    # 处理图片、视频（有 download 方法两个参数）
                    is_media_message = any(media_type in msg_class_name for media_type in ['Image', 'Video'])
                    
                    if is_media_message and hasattr(msg, 'download'):
                        # 创建临时目录
                        temp_dir = tempfile.mkdtemp()

                        try:
                            # 下载文件到临时目录
                            file_path = msg.download(dir_path=temp_dir, timeout=30)
                            
                            # 调用上传接口
                            file_service = FileService()
                            upload_result = file_service.upload_file_by_path(
                                file_path=str(file_path),
                                description=f"WeChat file from {msg_info.get('chat_name', 'unknown')}",
                                uploader="wechat_bot"
                            )
                            
                            # 更新消息信息，使用file_id作为文件名
                            msg_info.update({
                                "file_id": upload_result["file_id"],  # 使用file_id作为标识
                                "file_info": upload_result,  # 保存完整的文件信息
                                "download_success": True
                            })
                                
                        except Exception as download_error:
                            msg_info.update({
                                "download_error": str(download_error),
                                "download_success": False
                            })
                        finally:
                            # 确保删除临时目录和文件
                            shutil.rmtree(temp_dir, ignore_errors=True)

                    # 文件下载处理方法（有 download 方法三个参数）
                    elif 'File' in msg_class_name and hasattr(msg, 'download'):
                        # 创建临时目录
                        temp_dir = tempfile.mkdtemp()

                        try:
                            # 下载文件到临时目录
                            file_path = msg.download(dir_path=temp_dir, force_click=False, timeout=30)
                            
                            # 调用上传接口
                            file_service = FileService()
                            upload_result = file_service.upload_file_by_path(
                                file_path=str(file_path),
                                description=f"WeChat file from {msg_info.get('chat_name', 'unknown')}",
                                uploader="wechat_bot"
                            )
                            
                            # 更新消息信息，使用file_id作为文件名
                            msg_info.update({
                                "file_id": upload_result["file_id"],  # 使用file_id作为标识
                                "file_info": upload_result,  # 保存完整的文件信息
                                "download_success": True
                            })
                        except Exception as download_error:
                            msg_info.update({
                                "download_error": str(download_error),
                                "download_success": False
                            })
                        finally:
                            # 确保删除临时目录和文件
                            shutil.rmtree(temp_dir, ignore_errors=True)
                        
                    # 单独处理语音消息（有 to_text 方法）
                    elif 'Voice' in msg_class_name and hasattr(msg, 'to_text'):
                        try:
                            # 转换语音为文本
                            text_content = msg.to_text()
                            
                            # 添加语音转文本结果
                            msg_info.update({
                                "voice_to_text": text_content,
                                "voice_convert_success": True
                            })
                            
                        except Exception as voice_error:
                            msg_info.update({
                                "voice_to_text": "",
                                "voice_convert_error": str(voice_error),
                                "voice_convert_success": False
                            })
                    elif 'Link' in msg_class_name and hasattr(msg, 'get_url'):
                        try:
                            url_content = msg.get_url()
                            msg_info.update({
                                "url": url_content,
                                "get_url_success": True
                            })

                        except Exception as url_error:
                            msg_info.update({
                                "url": "",
                                "get_url_error": str(url_error),
                                "get_url_success": False
                            })
                    
                    processed_messages.append(msg_info)
                
                result['msg'] = processed_messages
                
            return APIResponse(success=True, message='', data=result)
            
        except Exception as e:
            return APIResponse(success=False, message=str(e))

        finally:
            minimize_window(wx.core.HWND)

    def send_quote_by_id(
            self,
            content: str,
            msg_id: str,
            wxname: Optional[str] = None
        ) -> APIResponse:
        """根据ID发送引用消息"""
        try:
            wx = get_wechat(wxname)
            if (msg := wx.GetMessageById(msg_id)) is not None:
                if isinstance(msg, HumanMessage):
                    result = msg.quote(text=content)
                    return APIResponse(success=bool(result), message=result['message'], data=result['data'])
                else:
                    return APIResponse(success=False, message=f'当前消息不可引用(消息类型："{msg.type}"  内容："{msg.content}")')
            else:
                return APIResponse(success=False, message=f"消息不存在：{msg_id}")    
        except Exception as e:
            return APIResponse(success=False, message=str(e))

    def get_new_friends(
            self,
            acceptable: bool = True,
            wxname: Optional[str] = None
        ) -> APIResponse:
        """获取新朋友（wxautox特有）"""
        if not has_feature("get_new_friends"):
            return APIResponse(success=False, message="此功能需要wxautox版本支持")
        
        try:
            wx = get_wechat(wxname)
            result = wx.GetNewFriends(acceptable=acceptable)
            return APIResponse(success=True, message='', data=result)
        except Exception as e:
            return APIResponse(success=False, message=str(e))

    def accept_new_friend(
            self,
            new_friend_id: str,
            remark: str = '',
            tags: List[str] = [],
            wxname: Optional[str] = None
        ) -> APIResponse:
        """接受新朋友（wxautox特有）"""
        if not has_feature("accept_new_friend"):
            return APIResponse(success=False, message="此功能需要wxautox版本支持")
        
        try:
            wx = get_wechat(wxname)
            result = wx.AcceptNewFriend(new_friend_id=new_friend_id, remark=remark, tags=tags)
            return APIResponse(success=bool(result), message=result['message'], data=result['data'])
        except Exception as e:
            return APIResponse(success=False, message=str(e))

    def switch_to_chat_page(
            self,
            wxname: Optional[str] = None
        ) -> APIResponse:
        """切换到聊天页面（wxautox特有）"""
        if not has_feature("switch_to_chat_page"):
            return APIResponse(success=False, message="此功能需要wxautox版本支持")
        
        try:
            wx = get_wechat(wxname)
            result = wx.SwitchToChat()
            return APIResponse(success=bool(result), message=result['message'], data=result['data'])
        except Exception as e:
            return APIResponse(success=False, message=str(e))

    def switch_to_contact_page(
            self,
            wxname: Optional[str] = None
        ) -> APIResponse:
        """切换到联系人页面（wxautox特有）"""
        if not has_feature("switch_to_contact_page"):
            return APIResponse(success=False, message="此功能需要wxautox版本支持")
        
        try:
            wx = get_wechat(wxname)
            result = wx.SwitchToContactPage()
            return APIResponse(success=bool(result), message=result['message'], data=result['data'])
        except Exception as e:
            return APIResponse(success=False, message=str(e))
        
    def is_online(
            self,
            wxname: Optional[str] = None
        ) -> APIResponse:
        
        try:
            wx = get_wechat(wxname)
            return APIResponse(success=True, message='在线', data={'status': 'online', 'online': True})
        except Exception as e:
            return APIResponse(success=False, message=str(e))

    def login(
            self,
            wxname: Optional[str] = None
        ) -> APIResponse:
        try:
            wx = get_wechat_login()
            wx.ClearHint()
            result = wx.Login()
            if result:
                return APIResponse(success=True, message='已登录或登录成功', data={'status': 'ok'})
            else:
                return APIResponse(success=False, message='未能登录成功，请获取二维码后扫码登录', data={'status': 'need_qrcode'})
        except Exception as e:
            return APIResponse(success=False, message=str(e))

    def qrcode(
            self,
            wxname: Optional[str] = None
    ) -> FileResponse:
        try:
            wx = get_wechat_login()
            pil_image = wx.GetQRCode() 
            if pil_image:
                # 创建临时文件
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                    pil_image.save(tmp_file, format='PNG')
                    tmp_file_path = tmp_file.name
            
                # 返回文件响应
                return FileResponse(
                    path=tmp_file_path,
                    media_type="image/png",
                    filename="qrcode.png",
                    background=lambda: os.unlink(tmp_file_path)  # 响应完成后删除临时文件
                )
            else:
                # 返回默认错误图片或空响应
                return Response(
                    content="QR code not available",
                    status_code=404,
                    media_type="text/plain"
                )
        except Exception as e:
            return Response(
                content=f"Error generating QR code: {str(e)}",
                status_code=500,
                media_type="text/plain"
            )
