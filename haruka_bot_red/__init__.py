from nonebot.plugin import PluginMetadata
from nonebot.plugin.manager import PluginLoader

if isinstance(globals()["__loader__"], PluginLoader):
    from .utils import on_startup

    on_startup()

    from . import plugins  # noqa: F401

from .version import VERSION, __version__  # noqa: F401

__plugin_meta__ = PluginMetadata(
    name="haruka_bot_red",
    description="将B站UP主的动态和直播信息推送至QQ，适配red协议",
    usage="https://github.com/boxie123/HarukaBot-Red",
    homepage="https://github.com/boxie123/HarukaBot-Red",
    type="application",
    supported_adapters={"~red"},
    extra={
        "author": "boxie123",
        "version": __version__,
        "priority": 1,
    },
)
