from wxautox import WeChat
from typing import List
from datetime import datetime
from app.models.response import APIResponse

def now_time(fmt='%Y%m%d%H%M%S'):
    return datetime.now().strftime(fmt)

def accept_new_friend(
        wx: WeChat,
        keywords: str,
        remark: str = '',
        tags: str = ''
):
    # 此处是因为dify当前有bug，无法设置array类型参数，所以str类型参数用\n分割
    keywords = keywords.split('\n')  
    tags = tags.split('\n')
    result = []
    try:
        new_friends = wx.GetNewFriends()
        for friend in new_friends:
            for keyword in keywords:
                if keyword in friend.msg:
                    remark_name = f"{remark}_{now_time()}"
                    friend.accept(remark_name, tags)
                    info = friend.info
                    info['remark'] = remark_name
                    info['wxid'] = friend.get_account()
                    result.append(info)
        return APIResponse(success=True, message='success', data=result)
    except Exception as e:
        return APIResponse(success=False, message=str(e), data=None)
    finally:
        wx.SwitchToChat()