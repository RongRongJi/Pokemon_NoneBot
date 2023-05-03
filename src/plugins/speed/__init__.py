from nonebot import on_command, on_keyword
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.typing import T_State  
import nonebot


speed = on_command('速度线', aliases={'speed'}, rule=to_me())


@speed.handle()
async def speed_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    msg = '[CQ:image,file=speed.png] 该速度线来自@b站 Pokemmo-VFU'

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['860189236', '210839336', '523485781']
        if groupNum not in whiteablum:
            await speed.finish()

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+msg
        })
    else:
        await bot.call_api('send_private_msg', 
        **{'user_id':int(user_id), 'message': msg})

    await speed.finish()


