from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import random
from datetime import datetime
from zoneinfo import ZoneInfo

@register("jrrp", "exusiaiwei", "一个简单的人品插件", "1.1.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.fortune_descriptions = {
            (1, 10): "今天是不太顺利的一天，建议多加小心！",
            (11, 30): "今天的运势一般，适合做一些小事情！",
            (31, 60): "今天的运势不错，可以尝试一些新的事物！",
            (61, 80): "今天的运势很好，适合做一些大事情！",
            (81, 100): "今天的运势非常好，万事如意！"
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
        rp = random.randint(1, 100)
        message_str = next((desc for (low, high), desc in self.fortune_descriptions.items() if low <= rp <= high), "今天的运势未知，请自行判断！")


        yield event.plain_result(f"{user_name}，你今天的人品是{rp}，{message_str}")

    async def terminate(self):
        '''可选择实现 terminate 函数，当插件被卸载/停用时会调用。'''
