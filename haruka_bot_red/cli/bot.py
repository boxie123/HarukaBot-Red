import sys
from os import path

import nonebot
from nonebot.adapters.red import Adapter
from nonebot.log import default_format, logger


nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(Adapter)
app = nonebot.get_asgi()

# 删除 haruka_bot 导入，否则 nonebot 导入时会忽略
del sys.modules["haruka_bot_red"]
nonebot.load_plugin("haruka_bot_red")

# Modify some config / config depends on loaded configs
#
# config = nonebot.get_driver().config
# do something...

logger.add(
    path.join("log", "error.log"),
    rotation="00:00",
    retention="1 week",
    diagnose=False,
    level="ERROR",
    format=default_format,
    encoding="utf-8",
)


def run():
    nonebot.run(app="haruka_bot_red.cli.bot:app")
