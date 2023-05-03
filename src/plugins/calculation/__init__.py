from nonebot import on_command, on_keyword
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.typing import T_State  
import nonebot


cal = on_command('计算器', aliases={'jsq', 'cal'}, rule=to_me())


@cal.handle()
async def cal_handle(bot: Bot, event: Event, state: T_State):

    msg = '''精灵宝可梦伤害/个体计算器→: http://calc.mypokemon.top/
选择网页最上方的SWSH有较完整的宝可梦数据'''

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['860189236', '210839336','523485781']
        if groupNum not in whiteablum:
            await cal.finish()

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+msg
        })
    else:
        await bot.call_api('send_private_msg', 
        **{'user_id':int(user_id), 'message': +msg})

    await cal.finish()


