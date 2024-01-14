from nonebot.matcher import matchers

from ..utils import on_command, to_me, permission_check
from ..version import __version__

help = on_command("帮助", rule=to_me(), priority=5)

help.handle()(permission_check)


@help.handle()
async def _():
    message = "目前支持的功能：\n"
    for matchers_list in matchers.values():
        for matcher in matchers_list:
            if (
                matcher.plugin_name
                and matcher.plugin_name.startswith("haruka_bot")
                and matcher.__doc__
            ):
                message += matcher.__doc__ + "\n"
    message += (
        f"\n当前版本：v{__version__}\n"
    )
    await help.finish(message)
