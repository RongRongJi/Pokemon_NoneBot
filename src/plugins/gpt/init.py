from nonebot import on_command, on_keyword
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.typing import T_State  
import nonebot
from .chat import chat


gpt = on_keyword({'gpt'}, rule=to_me())


@gpt.handle()
async def gpt_handle(bot: Bot, event: Event, state: T_State):

    content = str(event.get_message()).strip()
    content = content.strip('gpt')

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['860189236', '210839336', '624627458']
        if groupNum not in whiteablum:
            await gpt.finish()

        msg = chat(content)
        if msg == '':
            await gpt.finish()
        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+msg
        })
    else:

        msg = chat(content)
        if msg == '':
            await gpt.finish()
        await bot.call_api('send_private_msg', 
        **{'user_id':int(user_id), 'message': msg})

    await gpt.finish()


