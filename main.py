from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import random
from datetime import datetime
from zoneinfo import ZoneInfo
@register("jrrp", "exusiaiwei", "一个简单的人品插件", "1.2.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.fortune_descriptions = {
            (1, 10): "人品已欠费停机，建议今天就躺平吧！🥲",
            (11, 30): "普通的一天，像白开水一样平淡无奇~",
            (31, 60): "运气不错哦，可以试试抽卡或者告白什么的！✨",
            (61, 80): "今日锦鲤附体！适合做重要决定和冒险！🐟",
            (81, 100): "欧皇降临！今天你就是天选之人，无敌了！👑"
        }

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("jrrp")
    async def jrrp(self, event: AstrMessageEvent):
        '''今日人品值查询，每个用户每天固定，范围1-100'''
        user_name = event.get_sender_name()
        utc_8 = datetime.now(ZoneInfo("Asia/Shanghai"))
        date_str = utc_8.strftime("/%y/%m%d")
        userseed = hash(date_str + user_name)
        random.seed(userseed)

        # 使用加权随机 - 高分概率更大
        weights = [1, 2, 3, 2, 1]  # 越高分权重越大
        ranges = [(1, 20), (21, 40), (41, 60), (61, 80), (81, 100)]

        selected_range = random.choices(ranges, weights=weights, k=1)[0]
        rp = random.randint(selected_range[0], selected_range[1])
        message_str = next(
            (
                desc
                for (low, high), desc in self.fortune_descriptions.items()
                if low <= rp <= high
            ),
            "今天的运势未知，请自行判断！",
        )

        yield event.plain_result(f"{user_name}，你今天的人品是{rp}，{message_str}")

    async def terminate(self):
        '''可选择实现 terminate 函数，当插件被卸载/停用时会调用。'''
