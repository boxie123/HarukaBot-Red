from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.rule import to_me

from ...database import DB as db
from ...utils import permission_check, on_command

special_date_add = on_command("添加特殊日期", rule=to_me(), priority=5)
special_date_add.__doc__ = """添加特殊日期 name month day"""

special_date_add.handle()(permission_check)


@special_date_add.handle()
async def handle_date(
        matcher: Matcher,
        command_arg: Message = CommandArg(),
):
    special_day = command_arg.extract_plain_text().split()
    if len(special_day) == 3 and special_day[1].isdecimal() and special_day[2].isdecimal():
        matcher.set_arg("date", command_arg)
    else:
        await special_date_add.finish("month 和 day 应为纯阿拉伯数字")


@special_date_add.got("date", prompt="请输入要添加的特殊日期")
async def _(sp_date: str = ArgPlainText("date")):
    """手动添加特殊日期"""
    special_day = sp_date.split()
    result = await db.add_special(
        name=special_day[0],
        month=special_day[1],
        day=special_day[2],
    )
    if result:
        await special_date_add.finish(f"已添加特殊日期\"{special_day[0]}\"")
    await special_date_add.finish("添加特殊日期失败，请联系铂屑")
