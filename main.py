from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import random
import datetime

@register("jrrp", "exusiaiwei", "一个简单的人品插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("jrrp")
    async def jrrp(self, event: AstrMessageEvent):
        '''这是一个 hello world 指令''' # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        utc_8 = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        date_str = utc_8.strftime("/%y/%m%d")
        seed = hash(date_str + user_name)
        random.seed(seed)
        rp = random.randint(1, 100)
        if rp <= 50:
            message_str = "人品不佳，今天的运势不太好哦！"
        elif rp <= 80:
            message_str = "人品一般，今天的运势还不错！"
        elif rp <= 95:
            message_str = "人品不错，今天的运势很好哦！"
        else:
            message_str = "人品爆发，今天的运势非常好！"
        yield event.plain_result(f"{user_name}，你今天的人品是{rp}，{message_str}")

    async def terminate(self):
        '''可选择实现 terminate 函数，当插件被卸载/停用时会调用。'''
