from pydantic import BaseModel
from typing import Optional, List, Union

# 基础请求
class BaseRequest(BaseModel):
    wxname: Union[None, str] = ''

# 基础聊天请求
class BaseChatRelevantRequest(BaseRequest):
    who: str = '文件传输助手'
    exact: bool = False

# 发送消息请求
class SendMessageRequest(BaseChatRelevantRequest):
    msg: str
    clear: bool = True
    at: Union[str, List[str]] = ''

# 切换聊天窗口
class ChatWithRequest(BaseChatRelevantRequest):
    pass

# 发送文件请求
class SendFileRequest(BaseChatRelevantRequest):
    file_id: str  # 文件ID，对应上传的文件

# 发送url卡片请求
class SendUrlCardRequest(BaseRequest):
    url: str = 'https://plus.wxauto.org'
    friends: Union[str, List[str]] = '文件传输助手'
    timeout: int = 10

# 获取子窗口请求
class GetAllSubWindowRequest(BaseRequest):
    pass

# 添加监听聊天请求
class AddListenChatRequest(BaseRequest):
    who: str = '文件传输助手'

# 获取下一个新消息请求
class GetNextNewMessageRequest(BaseRequest):
    filter_mute: bool = False

# 获取所有消息请求
class GetAllMessageRequest(BaseRequest):
    who: str = '文件传输助手'

# 根据id发送引用消息
class SendQuoteByIdRequest(BaseRequest):
    msg_id: str
    content: str

# 获取新朋友请求
class GetNewFriendsRequest(BaseRequest):
    acceptable: bool = True

# 接受新朋友请求
class AcceptNewFriendRequest(BaseRequest):
    new_friend_id: str
    remark: str = None
    tags: Union[List[str], str, None] = None

# 切换到聊天页面请求
class SwitchToChatPageRequest(BaseRequest):
    pass

# 切换到联系人页面请求
class SwitchToContactPageRequest(BaseRequest):
    pass