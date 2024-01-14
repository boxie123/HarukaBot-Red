from nonebot.adapters.red.event import MessageEvent

from ...database import DB as db
from ...utils import get_type_id, permission_check, to_me, on_command

special_date_on = on_command("开启节假日提醒", rule=to_me(), priority=5)
special_date_on.__doc__ = """开启节假日提醒"""

special_date_on.handle()(permission_check)


@special_date_on.handle()
async def _(event: MessageEvent):
    """订阅节假日提醒"""
    if event.chatType == 2:
        message_type = "group"
    else:
        message_type = "private"
    result = await db.add_date(
        type=message_type,
        type_id=get_type_id(event),
        bot_id=event.peerUid,
    )
    if result:
        await special_date_on.finish("已订阅节假日提醒")
    await special_date_on.finish("已经订阅过了")
