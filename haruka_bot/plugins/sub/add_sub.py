from bilireq.exceptions import ResponseCodeError
from bilireq.user import get_user_info
from nonebot.adapters.red import Bot
from nonebot.adapters.red.event import MessageEvent
from nonebot.adapters.red.api.model import ChatType
from nonebot.params import ArgPlainText

from ...database import DB as db
from ...utils import (
    PROXIES,
    get_type_id,
    handle_uid,
    on_command,
    permission_check,
    to_me,
    uid_check,
)

add_sub = on_command("关注", aliases={"添加主播"}, rule=to_me(), priority=5)
add_sub.__doc__ = """关注 UID"""

add_sub.handle()(permission_check)

add_sub.handle()(handle_uid)

add_sub.got("uid", prompt="请输入要关注的UID")(uid_check)


@add_sub.handle()
async def _(bot: Bot, event: MessageEvent, uid: str = ArgPlainText("uid")):
    """根据 UID 订阅 UP 主"""
    user = await db.get_user(uid=uid)
    name = user and user.name
    if not name:
        try:
            name = (await get_user_info(uid, reqtype="web", proxies=PROXIES))["name"]
        except ResponseCodeError as e:
            if e.code in [-400, -404]:
                await add_sub.finish("UID不存在，注意UID不是房间号")
            elif e.code == -412:
                await add_sub.finish("操作过于频繁IP暂时被风控，请半小时后再尝试")
            else:
                name = str(uid)
    if event.chatType == ChatType.GROUP:
        message_type = "group"
    else:
        message_type = "private"
    result = await db.add_sub(
        uid=uid,
        type=message_type,
        type_id=await get_type_id(event),
        bot_id=bot.self_id,
        name=name,
        # TODO 自定义默认开关
        live=True,
        dynamic=True,
        at=False,
    )
    if result:
        await add_sub.finish(f"已关注 {name}（{uid}）")
    await add_sub.finish(f"{name}（{uid}）已经关注了")
