from wxautox import WeChat, Chat, WxParam, get_wx_clients
from wxautox.param import WxResponse
from wxautox.logger import wxlog
from pythoncom import CoInitialize
from typing import Optional, Union, List
from app.models.response import APIResponse
from app.services.file_service import FileService
import os


CoInitialize()
wxlog.set_debug(True)
WxParam.MESSAGE_HASH = True
WxParam.ENABLE_FILE_LOGGER = False
WxClient = {i.nickname: i for i in get_wx_clients()}
WxClientChat = ...

def get_wechat(wxname: str) -> WeChat:
    if (not wxname) and WxClient:
        wx = list(WxClient.values())[0]
    elif wxname in WxClient:
        wx = WxClient[wxname]
    else:
        wx = WeChat(nickname=wxname)
    return wx

def get_wechat_subwin(wxname: str, who: str) -> Chat:
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
        """发送文件
        
        Args:
            file_id: 文件ID，对应上传的文件
            who: 发送对象，不指定则发送给当前聊天对象
            exact: 搜索who好友时是否精确匹配
            wxname: 微信客户端名称
            
        Returns:
            APIResponse: 发送结果
        """
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
        try:
            wx = get_wechat(wxname)
            result = wx.ChatWith(who=who, exact=exact)
            if result:
                return APIResponse(success=True, message='主窗口聊天切换成功', data={'chatname': result})
            else:
                return APIResponse(success=False, message='主窗口聊天切换失败')
        except Exception as e:
            return APIResponse(success=False, message=str(e))

    def send_url_card(
            self,
            url: str,
            friends: Union[str, List[str]],
            timeout: int = 10,
            wxname: Optional[str] = None
        ) -> APIResponse:
        try:
            wx = get_wechat(wxname)
            result = wx.SendUrlCard(url=url, friends=friends, timeout=timeout)
            return APIResponse(success=bool(result), message=result['message'], data=result['data'])
        except Exception as e:
            return APIResponse(success=False, message=str(e))
        
    def get_all_sub_window(
            self,
            wxname: Optional[str] = None
        ) -> APIResponse:
        try:
            wx = get_wechat(wxname)
            result = wx.GetAllSubWindow()
            data = [{'name': i.who, 'type': i.chat_type} for i in result]
            return APIResponse(success=True, message='', data=data)
        except Exception as e:
            return APIResponse(success=False, message=str(e))
        
    def add_listen_chat(
            self,
            who: str,
            wxname: Optional[str] = None
        ) -> APIResponse:
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
        
    def get_all_message(
            self,
            who: str,
            wxname: Optional[str] = None
        ) -> APIResponse:
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

    def get_next_new_message(
            self,
            filter_mute: bool = False,
            wxname: Optional[str] = None
        ) -> APIResponse:
        try:
            wx = get_wechat(wxname)
            result = wx.GetNextNewMessage(filter_mute=filter_mute)
            if result:
                result['msg'] = [msg.info for msg in result['msg']]
            return APIResponse(success=True, message='', data=result)
        except Exception as e:
            return APIResponse(success=False, message=str(e))

    def _get_msg_by_id(
            self,
            msg_id: str,
            wxname: Optional[str] = None
        ) -> APIResponse:
        wx = get_wechat(wxname)
        msg = wx.GetMessageById(msg_id)
        return msg
    
    def send_quote_by_id(
            self,
            content: str,
            msg_id: str,
            wxname: Optional[str] = None
        ) -> APIResponse:
        msg = self._get_msg_by_id(msg_id, wxname)
        if msg and msg.attr in ('self', 'friend'):
            result = msg.quote(content)
            return APIResponse(success=bool(result), message=result['message'], data=result['data'])
        else:
            return APIResponse(success=False, message='找不到消息')
        
    def get_new_friends(
            self,
            acceptable: bool = True,
            wxname: Optional[str] = None
        ) -> APIResponse:
        try:
            wx = get_wechat(wxname)
            result = [i.info for i in wx.GetNewFriends(acceptable=acceptable)]
            return APIResponse(success=True, message='', data=result)
        except Exception as e:
            return APIResponse(success=False, message=str(e))

    def _get_new_friend_by_id(
            self,
            new_friend_id: str,
            wxname: Optional[str] = None
        ) -> APIResponse:
        wx = get_wechat(wxname)
        if result := [i for i in wx.GetNewFriends() if i.id == new_friend_id]:
            return result[0]
        else:
            return None
        
    def accept_new_friend(
            self,
            new_friend_id: str,
            remark: str = '',
            tags: List[str] = [],
            wxname: Optional[str] = None
        ) -> APIResponse:
        new_friend = self._get_new_friend_by_id(new_friend_id, wxname)
        try:
            if new_friend:
                result = new_friend.accept(remark=remark, tags=tags)
                return APIResponse(success=bool(result), message=result['message'], data=result['data'])
            else:
                return APIResponse(success=False, message='找不到新朋友')
        except Exception as e:
            return APIResponse(success=False, message=str(e))

    def switch_to_chat_page(
            self,
            wxname: Optional[str] = None
        ) -> APIResponse:
        try:
            wx = get_wechat(wxname)
            result = wx.SwitchToChatPage()
            return APIResponse(success=bool(result), message='切换到聊天页面成功' if result else '切换到聊天页面失败')
        except Exception as e:
            return APIResponse(success=False, message=str(e))

    def switch_to_contact_page(
            self,
            wxname: Optional[str] = None
        ) -> APIResponse:
        try:
            wx = get_wechat(wxname)
            result = wx.SwitchToContactPage()
            return APIResponse(success=bool(result), message='切换到联系人页面成功' if result else '切换到联系人页面失败')
        except Exception as e:
            return APIResponse(success=False, message=str(e))