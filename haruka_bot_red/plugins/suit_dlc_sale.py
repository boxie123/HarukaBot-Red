import traceback
import httpx

from nonebot.log import logger
from nonebot.rule import to_me

from ..utils import on_command

suit_dlc_sale = on_command("收藏集销量", aliases={"收藏集"}, rule=to_me(), priority=5)
suit_dlc_sale.__doc__ = """收藏集销量"""


@suit_dlc_sale.handle()
async def _():
    message = "获取收藏集销量失败，请联系铂屑"
    try:
        resp = httpx.get("https://api.bilibili.com/x/vas/dlc_act/act/basic?act_id=100434")
        resp.encoding = "utf-8"
        resp_json = resp.json()
        assert resp_json["code"] == 0
        sale_num = resp_json["data"]["lottery_list"][0]["total_sale_amount"]
        message = f"鸽宝收藏集当前已抽数: {sale_num}"
    except Exception:
        logger.error("获取收藏集信息失败，以下为错误日志：")
        logger.error(traceback.format_exc())
    await suit_dlc_sale.finish(message)
