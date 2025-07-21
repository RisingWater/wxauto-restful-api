from app.utils.wx_package_manager import get_wx_class, has_feature, is_wxautox
from pythoncom import CoInitialize
from typing import Optional, List
from app.models.response import APIResponse

# 动态导入wx包
WeChat = get_wx_class("WeChat")

# 初始化COM
CoInitialize()

def get_wechat(wxname: str) -> WeChat:
    """获取微信实例"""
    return WeChat(nickname=wxname)

class AcceptNewFriendService:
    """接受新朋友服务（wxautox特有）"""
    
    def __init__(self):
        if not has_feature("accept_new_friend"):
            raise RuntimeError("此功能需要wxautox版本支持")
    
    def accept_new_friend(
            self,
            new_friend_id: str,
            remark: str = '',
            tags: List[str] = [],
            wxname: Optional[str] = None
        ) -> APIResponse:
        """接受新朋友"""
        try:
            wx = get_wechat(wxname)
            result = wx.AcceptNewFriend(new_friend_id=new_friend_id, remark=remark, tags=tags)
            return APIResponse(success=bool(result), message=result['message'], data=result['data'])
        except Exception as e:
            return APIResponse(success=False, message=str(e))