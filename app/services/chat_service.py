from wxautox import WeChat, Chat, get_wx_clients
from wxautox.param import WxResponse
from pythoncom import CoInitialize
from typing import Optional, Union, List
from app.models.response import APIResponse
from .wechat_service import WxClient, get_wechat, get_wechat_subwin

class ChatService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatService, cls).__new__(cls)
        return cls._instance

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
