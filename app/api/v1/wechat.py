from fastapi import APIRouter, Request, Depends
from app.services.wechat_service import WeChatService
from app.models.request.wechat import *
from app.models.response import APIResponse
from app.utils.route_condition import (
    require_wxautox, 
    require_feature, 
    conditional_route, 
    has_url_card_feature, 
    has_listen_chat_feature, 
    has_new_message_feature, 
    has_quote_message_feature, 
    has_friend_management_feature, 
    has_page_switch_feature
)
from typing import Dict, Any
import asyncio

router = APIRouter()

@router.post(
    "/send", 
    operation_id="[wx]发送消息", 
    response_model=APIResponse,
    summary="发送文字消息"
)
async def send_message(
    request: SendMessageRequest, 
    service: WeChatService = Depends()
):
    """微信主窗口发送消息"""
    return service.send_message(
        msg=request.msg,
        who=request.who,
        clear=request.clear,
        at=request.at,
        exact=request.exact,
        wxname=request.wxname
    )

@router.post(
    "/sendfile", 
    operation_id="[wx]发送文件", 
    response_model=APIResponse,
    summary="发送文件、图片、视频等（请先调用上传文件接口）"
)
async def send_file(
    request: SendFileRequest,
    service: WeChatService = Depends()
):
    """微信主窗口发送文件"""
    return service.send_file(
        file_id=request.file_id,
        who=request.who,
        exact=request.exact,
        wxname=request.wxname
    )

@router.post(
    "/chatwith", 
    operation_id="[wx]切换聊天窗口", 
    response_model=APIResponse,
    summary="切换聊天窗口"
)
async def chat_with(
    request: ChatWithRequest,
    service: WeChatService = Depends()
):
    """微信主窗口切换聊天窗口"""
    result = service.chat_with(
        who=request.who,
        exact=request.exact,
        wxname=request.wxname
    )
    return result

@router.post(
    "/getallsubwindow", 
    operation_id="[wx]获取所有子窗口", 
    response_model=APIResponse,
    summary="获取所有子窗口信息"
)
async def get_all_sub_window(
    request: GetAllSubWindowRequest,
    service: WeChatService = Depends()
):
    """获取微信所有子窗口信息"""
    return service.get_all_sub_window(wxname=request.wxname)

@router.post(
    "/getallmessage", 
    operation_id="[wx]获取当前窗口加载的消息", 
    response_model=APIResponse,
    summary='获取当前窗口加载的消息'
)
async def get_all_message(
    request: GetAllMessageRequest,
    service: WeChatService = Depends()
):
    """获取当前窗口加载的消息"""
    print('xxxxxxxxxxxxxxxxxxxx')
    return service.get_all_message(who=request.who, wxname=request.wxname)

@router.post(
    "/sendurlcard", 
    operation_id="[wx]发送url卡片", 
    response_model=APIResponse, 
    summary='✨发送url卡片'
)
@conditional_route(has_url_card_feature)
async def send_url_card(
    request: SendUrlCardRequest,
    service: WeChatService = Depends()
):
    """微信发送url卡片（wxautox特有）"""
    return service.send_url_card(
        url=request.url,
        friends=request.friends,
        timeout=request.timeout,
        wxname=request.wxname
    )

@router.post(
    "/addlistenchat", 
    operation_id="[wx]添加监听", 
    response_model=APIResponse,
    summary="添加监听（需和配合/chat/getnewmessage来获取新消息）"
)
async def add_listen_chat(
    request: AddListenChatRequest,
    service: WeChatService = Depends()
):
    """添加微信子窗口监听"""
    return service.add_listen_chat(
        who=request.who,
        wxname=request.wxname
    )

@router.post(
    "/getnextnewmessage", 
    operation_id="[wx]获取下一个新消息", 
    response_model=APIResponse,
    summary="获取一个未读消息窗口的新消息"
)
async def get_next_new_message(
    request: GetNextNewMessageRequest,
    service: WeChatService = Depends()
):
    """获取微信下一个新消息"""
    return service.get_next_new_message(
        filter_mute=request.filter_mute, 
        wxname=request.wxname
    )

@router.post(
    "/msg/quote", 
    operation_id="[wx]发送引用消息", 
    response_model=APIResponse,
    summary="根据消息id发送引用消息"
)
# @conditional_route(has_quote_message_feature)
async def send_quote_by_id(
    request: SendQuoteByIdRequest,
    service: WeChatService = Depends()
):
    """根据id发送引用消息"""
    return service.send_quote_by_id(
        msg_id=request.msg_id,
        content=request.content,
        wxname=request.wxname
    )

@router.post(
    "/getnewfriends", 
    operation_id="[wx]获取好友申请", 
    response_model=APIResponse,
    summary='✨获取好友申请列表'
)
@conditional_route(has_friend_management_feature)
async def get_new_friends(
    request: GetNewFriendsRequest,
    service: WeChatService = Depends()
):
    """获取微信新朋友（wxautox特有）"""
    return service.get_new_friends(
        acceptable=request.acceptable,
        wxname=request.wxname
    )

@router.post(
    "/newfriend/accept", 
    operation_id="[wx]接受好友申请", 
    response_model=APIResponse,
    summary='✨接受好友申请'
)
@conditional_route(has_friend_management_feature)
async def accept_new_friend(
    request: AcceptNewFriendRequest,
    service: WeChatService = Depends()
):
    """接受微信新朋友（wxautox特有）"""
    if isinstance(request.tags, str):
        tags = [request.tags]
    else:
        tags = request.tags
    return service.accept_new_friend(
        new_friend_id=request.new_friend_id, 
        remark=request.remark, 
        tags=tags, 
        wxname=request.wxname
    )

@router.post("/switch/chat", operation_id="[wx]切换到聊天页面", response_model=APIResponse)
async def switch_to_chat_page(
    request: SwitchToChatPageRequest,
    service: WeChatService = Depends()
):
    """切换到聊天页面（wxautox特有）"""
    return service.switch_to_chat_page(wxname=request.wxname)

# @router.post("/switch/contact", operation_id="[wx]切换到联系人页面", response_model=APIResponse)
# @conditional_route(has_page_switch_feature)
# async def switch_to_contact_page(
#     request: SwitchToContactPageRequest,
#     service: WeChatService = Depends()
# ):
#     """切换到联系人页面（wxautox特有）"""
#     return service.switch_to_contact_page(wxname=request.wxname)