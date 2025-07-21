from app.utils.wx_package_manager import get_wx_class, get_wx_function, has_feature, is_wxautox
from pythoncom import CoInitialize
from typing import Optional, Union, List
from app.models.response import APIResponse
from .wechat_service import get_wechat_subwin

# 动态导入wx包
WeChat = get_wx_class("WeChat")
Chat = get_wx_class("Chat")
try:
    get_wx_clients = get_wx_function("get_wx_clients")
except:
    def get_wx_clents():
        wx = WeChat()
        return {wx.nickname: wx}

# 初始化COM
CoInitialize()

# 如果是wxautox版本，导入额外模块
if is_wxautox():
    try:
        WxResponse = get_wx_class("WxResponse")
    except Exception as e:
        print(f"警告：无法导入WxResponse: {e}")

# 获取微信客户端
try:
    WxClient = {i.nickname: i for i in get_wx_clients()}
except Exception as e:
    print(f"警告：无法获取微信客户端: {e}")
    WxClient = {}

def get_wechat(wxname: str) -> WeChat:
    """获取微信实例"""
    if (not wxname) and WxClient:
        wx = list(WxClient.values())[0]
    elif wxname in WxClient:
        wx = WxClient[wxname]
    else:
        wx = WeChat(nickname=wxname)
    return wx

class ChatService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatService, cls).__new__(cls)
        return cls._instance
    
    def __repr__(self):
        return f'<Chat Service object at {id(self)}>'

    def send_message(
        self,
        msg: str,
        who: str,
        clear: bool = True,
        at: Optional[str | list] = None,
        wxname: Optional[str] = None
    ) -> APIResponse:
        subwin = get_wechat_subwin(wxname, who)
        if subwin:
            result = subwin.SendMsg(msg=msg, clear=clear, at=at)
            return APIResponse(success=bool(result), message=result['message'], data=result['data'])
        else:
            return APIResponse(success=False, message='找不到该聊天窗口')
        
    def get_all_message(
            self,
            who: str,
            wxname: Optional[str] = None
        ) -> APIResponse:
        subwin = get_wechat_subwin(wxname, who)
        if subwin:
            result = subwin.ChatInfo()
            result['msg'] = [msg.info for msg in subwin.GetAllMessage()]
            return APIResponse(success=True, message='', data=result)
        else:
            return APIResponse(success=False, message='找不到该聊天窗口')
        
    def get_new_message(
            self,
            who: str,
            wxname: Optional[str] = None
        ) -> APIResponse:
        subwin = get_wechat_subwin(wxname, who)
        if subwin:
            result = subwin.ChatInfo()
            result['msg'] = [msg.info for msg in subwin.GetNewMessage()]
            return APIResponse(success=True, message='', data=result)
        else:
            return APIResponse(success=False, message='找不到该聊天窗口')
        
    def _get_msg_by_id(
            self,
            msg_id: str,
            who: str,
            wxname: Optional[str] = None
        ) -> APIResponse:
        subwin = get_wechat_subwin(wxname, who)
        if subwin:
            msg = subwin.GetMessageById(msg_id)
            return msg
        else:
            return None
        
    def send_quote_by_id(
            self,
            content: str,
            msg_id: str,
            who: str,
            wxname: Optional[str] = None
        ) -> APIResponse:
        msg = self._get_msg_by_id(msg_id, who, wxname)
        if msg and msg.attr in ('self', 'friend'):
            result = msg.quote(content)
            return APIResponse(success=bool(result), message=result['message'], data=result['data'])
        else:
            return APIResponse(success=False, message='找不到消息')

    def get_chat_info(self, who: str, wxname: Optional[str] = None) -> APIResponse:
        """获取聊天信息"""
        try:
            subwin = get_wechat_subwin(wxname, who)
            result = subwin.ChatInfo()
            return APIResponse(success=True, message='', data=result)
        except Exception as e:
            return APIResponse(success=False, message=str(e))
