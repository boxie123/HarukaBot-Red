from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.rule import to_me

from ...database import DB as db
from ...utils import permission_check, on_command

special_date_delete = on_command("删除特殊日期", rule=to_me(), priority=5)
special_date_delete.__doc__ = """删除特殊日期 name"""

special_date_delete.handle()(permission_check)


@special_date_delete.handle()
async def handle_month(
        matcher: Matcher,
        command_arg: Message = CommandArg(),
):
    special_day = command_arg.extract_plain_text().strip()
    if special_day:
        matcher.set_arg("name", command_arg)


@special_date_delete.got("name", prompt="请输入要删除的特殊日期名称")
async def _(name: str = ArgPlainText("name")):
    """手动删除特殊日期"""
    name = name.strip()
    result = await db.delete_special(
        name=name,
    )
    if result:
        await special_date_delete.finish(f"已删除特殊日期\"{name}\"")
    await special_date_delete.finish("特殊日期不存在")
