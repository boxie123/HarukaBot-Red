import datetime
import random

from httpx import AsyncClient

from ..database import DB as db

special_dates = {}
special_dates: dict[int, dict[int, set[str]]]


async def special_dates_update():
    empty_dict = {i: {} for i in range(1, 13)}
    special_dates.update(empty_dict)
    special_dates.update(
        {
            5: {12: {"汶川大地震纪念日"}},
            6: {4: {"服务器维护"}},
            7: {7: {"七七事变"}},
            9: {
                3: {"抗日战争胜利纪念日"},
                7: {"鸽宝生日"},
                18: {"九一八事变"},
                30: {"烈士纪念日"},
            },
            12: {
                9: {"鸽宝周年"},
                13: {"南京大屠杀公祭日"},
            },
        }
    )
    special_list = await db.get_special_list()
    for special_day in special_list:
        month = special_day.month
        day = special_day.day
        name = special_day.name
        if month in special_dates and day in special_dates[month]:
            special_dates[month][day].add(name)
        elif month in special_dates:
            special_dates[month][day] = {
                name,
            }
        else:
            special_dates[month] = {
                day: {
                    name,
                }
            }


def get_user_agents():
    """随机获取一个认证头"""
    agent = [
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 "
        "Safari/537.36",
    ]
    return random.choice(agent)


async def get_params(
    is_holiday: bool,
    mode: str,
    month: str,
):
    """生成 params"""
    today = datetime.date.today()
    params = {
        "order_by": 1,
        "holiday" if is_holiday else "holiday_overtime": 99,
        "cn": 1,
        "size": 31,
    }
    if mode == "week":
        params["yearweek"] = today.strftime("%Y%W")
    elif mode == "month":
        params["month"] = month
    else:
        params["date"] = today.strftime("%Y%m%d")
        # params["date"] = datetime.date(2022, 9, 10).strftime("%Y%m%d")

    return params


async def get_params_(
    mode: str,
    month: str,
):
    """生成假期和调休两种 params"""
    rest_params = await get_params(is_holiday=True, mode=mode, month=month)
    work_params = await get_params(is_holiday=False, mode=mode, month=month)
    return rest_params, work_params


async def get_raw_resp(
    client: AsyncClient,
    params: dict,
):
    """根据参数返回信息列表"""
    url = "https://api.apihubs.cn/holiday/get"
    headers = {"User-Agent": get_user_agents(), "Referer": "https://www.baidu.com/"}
    resp = await client.request(method="get", url=url, params=params, headers=headers)
    resp.encoding = "utf-8"
    rest_info = resp.json()
    assert rest_info["code"] == 0

    return rest_info["data"]["list"]


async def get_raw_list(
    mode: str,
    month: str,
):
    """获取假期列表和调休列表"""
    params = await get_params_(mode, month)
    async with AsyncClient() as client:
        rest_list = await get_raw_resp(client, params[0])
        work_list = await get_raw_resp(client, params[1])

    return rest_list, work_list


class Week:
    """按周查询"""

    @classmethod
    async def add_special_date(
        cls, result: dict, start: datetime.date, end: datetime.date
    ) -> dict:
        """加入 api 没有的特殊日期"""
        days_num = (end - start).days
        for i in range(days_num + 1):
            day = start + datetime.timedelta(i)
            if (day.month in special_dates) and (day.day in special_dates[day.month]):
                week = day.weekday() + 1  # +1因为monday为0
                for day_name in special_dates[day.month][day.day]:
                    result[week].append(f"{day_name}，不放假")

        return result

    @classmethod
    async def raw_list_to_dict(cls, raw_holidays_info, raw_workday_info) -> dict:
        """处理一周的信息列表"""
        result = {i: [] for i in range(1, 8)}
        today = datetime.date.today()
        start = today - datetime.timedelta(today.weekday())  # 本周周一日期
        end = start + datetime.timedelta(6)  # 本周周日日期
        # 获取放假信息
        for day in raw_holidays_info:
            name = day["holiday_cn"]
            or_name = day["holiday_or_cn"]
            week = day["week"]
            rest = day["holiday_recess"] == 1
            if or_name != name:
                name += "，" + or_name

            result[week].append("{}，{}".format(name, ("放假" if rest else "不放假")))

        # 获取调休信息
        for day in raw_workday_info:
            name = day["holiday_overtime_cn"][:-2]
            week = day["week"]
            result[week].append(f"{name}调休")

        result = await cls.add_special_date(result, start, end)

        return result

    @classmethod
    async def output_str(cls, result: dict) -> str:
        """生成每周的消息 str"""
        today = datetime.date.today()
        week_num_to_str = {
            1: "周一",
            2: "周二",
            3: "周三",
            4: "周四",
            5: "周五",
            6: "周六",
            7: "周日",
        }
        monday = today - datetime.timedelta(today.weekday())
        output = ""
        for week in result:
            if result[week]:
                info = "、".join(result[week])
                output += "{}：{}\n".format(week_num_to_str[week], info)

        if not output:
            return "本周无重要日期\n"
        else:
            output = (
                "本周（从{}月{}号周一开始）重要日期提醒:\n".format(monday.month, monday.day) + output
            )

        return output


class Month:
    """按月查询"""

    @classmethod
    async def add_special_date(
        cls, result: dict, start: datetime.date, end: datetime.date
    ) -> dict:
        """加入 api 没有的特殊日期"""
        days_num = (end - start).days
        for i in range(days_num + 1):
            day = start + datetime.timedelta(i)
            if (day.month in special_dates) and (day.day in special_dates[day.month]):
                for name in special_dates[day.month][day.day]:
                    result[name] = {
                        "rest": False,
                        "date": [day.day],
                        "overtime_date": [],
                    }

        return result

    @classmethod
    async def raw_list_to_dict(cls, raw_holidays_info, raw_workday_info, month) -> dict:
        """处理一个月的信息列表"""
        result = {}
        for day in raw_holidays_info:
            name = day["holiday_cn"]
            or_name = day["holiday_or_cn"]
            date = day["date"] % 100
            rest = day["holiday_recess"] == 1

            if name not in result:
                result[name] = {"rest": rest, "date": [date], "overtime_date": []}
            else:
                result[name]["date"].append(date)

            if or_name != name:
                if or_name not in result:
                    result[or_name] = {
                        "rest": rest,
                        "date": [date],
                        "overtime_date": [],
                    }
                else:
                    result[or_name]["date"].append(date)

        for day in raw_workday_info:
            name = day["holiday_overtime_cn"][:-2]
            date = day["date"] % 100

            if name not in result:
                result[name] = {"rest": True, "date": [], "overtime_date": [date]}
            else:
                result[name]["overtime_date"].append(date)

        start = datetime.date(int(month[:4]), int(month[4:]), 1)
        next_month = start.replace(day=28) + datetime.timedelta(days=4)
        end = next_month - datetime.timedelta(days=next_month.day)

        result = await cls.add_special_date(result, start, end)

        return result

    @classmethod
    async def output_str(cls, result: dict) -> str:
        """生成每月的消息 str"""
        result = sorted(
            result.items(),
            key=lambda x: x[1]["date"][0]
            if len(x[1]["date"]) > 0
            else x[1]["overtime_date"][0],
        )
        output = "本月节假日为：\n"
        if len(result) == 0:
            return "本月无重要日期\n"
        for name, day in result:
            output += "#{}\n".format(name)
            if len(day["date"]) == 0:
                output += "本节日放假日期不在查询范围中\n"
            else:
                if not day["rest"]:
                    output += "本节日不放假，日期："
                else:
                    output += "放假日期："
                for date in day["date"]:
                    output += f"{date}号，"
                output = output[:-1] + "\n"

            if len(day["overtime_date"]) != 0:
                output += "调休工作日："
                for date in day["overtime_date"]:
                    output += f"{date}号，"
                output = output[:-1] + "\n"
            output += "\n"

        return output


class Day:
    """按日查询"""

    @classmethod
    async def add_special_date(
        cls, result: dict[int, list[str]]
    ) -> dict[int, list[str]]:
        """加入 api 没有的特殊日期"""
        day = datetime.date.today()
        if (day.month in special_dates) and (day.day in special_dates[day.month]):
            week = day.weekday() + 1  # +1因为monday为0
            for day_name in special_dates[day.month][day.day]:
                result[week].append(f"{day_name}，不放假")

        return result

    @classmethod
    async def raw_list_to_dict(
        cls, raw_holidays_info, raw_workday_info
    ) -> dict[int, list[str]]:
        """处理当天的信息列表"""
        result = {i: [] for i in range(1, 8)}
        # 获取放假信息
        for day in raw_holidays_info:
            name = day["holiday_cn"]
            or_name = day["holiday_or_cn"]
            week = day["week"]
            rest = day["holiday_recess"] == 1
            if or_name != name:
                name += "，" + or_name

            result[week].append("{}，{}".format(name, ("放假" if rest else "不放假")))

        # 获取调休信息
        for day in raw_workday_info:
            name = day["holiday_overtime_cn"][:-2]
            week = day["week"]
            result[week].append(f"{name}调休")

        result = await cls.add_special_date(result)

        return result

    @classmethod
    async def output_str(cls, result: dict[int, list[str]]) -> str:
        """生成每日的消息 str"""
        today = datetime.date.today()
        week_num_to_str = {
            1: "周一",
            2: "周二",
            3: "周三",
            4: "周四",
            5: "周五",
            6: "周六",
            7: "周日",
        }
        output = ""
        for week in result:
            if result[week]:
                info = "、".join(result[week])
                output += "{}：{}\n".format(week_num_to_str[week], info)

        if not output:
            return None
        else:
            output = "今日（{}月{}日）重要日期提醒:\n".format(today.month, today.day) + output

        return output


async def get_special_date(mode: str, **kwargs):
    """main 函数，生成节假日提醒消息"""
    if "month" in kwargs:
        month = kwargs["month"]
    else:
        month = datetime.date.today().strftime("%Y%m")
    await special_dates_update()
    if mode == "week":
        result = await Week.raw_list_to_dict(*await get_raw_list(mode, month))
        return await Week.output_str(result)
    elif mode == "month":
        result = await Month.raw_list_to_dict(*await get_raw_list(mode, month), month)
        return await Month.output_str(result)
    else:
        result = await Day.raw_list_to_dict(*await get_raw_list(mode, month))
        return await Day.output_str(result)
