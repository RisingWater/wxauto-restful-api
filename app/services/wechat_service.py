from app.utils.wx_package_manager import (
    wx_manager,
    get_wx_class, 
    get_wx_function, 
    has_feature, 
    is_wxautox
)
from pythoncom import CoInitialize
from typing import Optional, Union, List
from app.models.response import APIResponse
from app.services.file_service import FileService
import os

# 动态导入wx包
WeChat = get_wx_class("WeChat")
Chat = get_wx_class("Chat")
HumanMessage = wx_manager.package.msgs.base.HumanMessage
try:
    get_wx_clients = get_wx_function("get_wx_clients")
except:
    def get_wx_clents():
        wx = WeChat()
        return {wx.nickname: wx}

# 初始化COM
CoInitialize()

# 如果是wxautox版本，设置额外配置
if is_wxautox():
    try:
        WxParam = get_wx_class("WxParam")
        WxResponse = get_wx_class("WxResponse")
        wxlog = get_wx_class("wxlog")
        
        # 设置wxautox特有配置
        wxlog.set_debug(True)
        WxParam.MESSAGE_HASH = True
        WxParam.ENABLE_FILE_LOGGER = False
    except Exception as e:
        print(f"警告：无法设置wxautox特有配置: {e}")

# 获取微信客户端
try:
    WxClient = {i.nickname: i for i in get_wx_clients()}
except Exception as e:
    print(f"警告：无法获取微信客户端: {e}")
    WxClient = {}

def get_wechat(wxname: str) -> WeChat:
    """获取微信实例
    
    Args:
        wxname: 微信客户端名称
        
    Returns:
        WeChat实例
    """
    if (not wxname) and WxClient:
        wx = list(WxClient.values())[0]
    elif wxname in WxClient:
        wx = WxClient[wxname]
    else:
        wx = WeChat(nickname=wxname)
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
            at: Optional[str | list] = None, 
            exact: bool = False, 
            wxname: Optional[str] = None
        ) -> APIResponse:
        """发送消息"""
        try:
            wx = get_wechat(wxname)
            result = wx.SendMsg(msg=msg, who=who, clear=clear, at=at, exact=exact)
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
            result = wx.SendFiles(filepath=file_info.file_path, who=who, exact=exact)
            
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
        # try:
        #     print('走到wechat了')
        #     wx = get_wechat(wxname)
        #     if who:
        #         if not wx.ChatWith(who):
        #             return APIResponse(success=False, message='找不到聊天窗口')
        #     result = wx.ChatInfo()
        #     msgs = wx.GetAllMessage()
        #     result['msg'] = [msg.info for msg in msgs]
        #     return APIResponse(success=True, message='', data=result)
        # except Exception as e:
        #     return APIResponse(success=False, message=str(e))

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
            subwin = wx._api.open_separate_window(who)
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
        """获取下一个新消息"""
        
        try:
            wx = get_wechat(wxname)
            result = wx.GetNextNewMessage(filter_mute=filter_mute)
            if result:
                result['msg'] = [msg.info for msg in result['msg']]
            return APIResponse(success=True, message='', data=result)
        except Exception as e:
            return APIResponse(success=False, message=str(e))

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
            result = wx.SwitchToChatPage()
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