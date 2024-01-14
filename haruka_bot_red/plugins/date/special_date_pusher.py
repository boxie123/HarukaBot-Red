import traceback

from ...database import DB as db
from ...utils import safe_send, scheduler, get_special_date

from nonebot.log import logger


async def sd_sched(mode: str = "week"):
    message = "获取节假日失败，请联系铂屑"
    try:
        message = await get_special_date(mode)
    except Exception:
        logger.error("获取节假日信息失败，以下为错误日志：")
        logger.error(traceback.format_exc())

    if not message:
        logger.success("今日无特殊日期")
        return

    push_list = await db.get_date_list()
    for sets in push_list:
        await safe_send(
            bot_id=sets.bot_id,
            send_type=sets.type,
            type_id=sets.type_id,
            message="定时温馨提醒：\n" + message,
            at=False
        )
        logger.success(f"向 {sets.type} {sets.type_id} 发送节假日定时提醒")

scheduler.add_job(
    sd_sched, "cron", args=("week",), day_of_week=0, hour=0, minute=3, second=0, id="special_date_sched_week",
    # sd_sched, "cron", args=(True,), day_of_week=4, hour=19, minute=52, second=30, id="special_date_sched_week",
)
scheduler.add_job(
    sd_sched, "cron", args=("month",), day=1, hour=0, minute=3, second=0, id="special_date_sched_month",
    # sd_sched, "cron", args=(False,), day=10, hour=1, minute=39, second=30, id="special_date_sched_month",
)
# scheduler.add_job(
#     sd_sched, "cron", args=("day",), hour=0, minute=3, second=0, id="special_date_sched_day",
#     # sd_sched, "cron", args=("day",), hour=1, minute=39, second=30, id="special_date_sched_day",
# )
