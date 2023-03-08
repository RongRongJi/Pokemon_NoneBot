from nonebot import on_command, on_keyword
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.typing import T_State  
import nonebot
from .species import make_species_dict, lookup_species_by_name


species_table = make_species_dict()

query = on_keyword({'#图鉴'}, rule=to_me())


@query.handle()
async def query_handle(bot: Bot, event: Event, state: T_State):

    get_poke_name = str(event.get_message()).strip()
    get_poke_name = get_poke_name.strip('#图鉴').replace(' ','')

    msg = lookup_species_by_name(get_poke_name, species_table)

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['860189236', '210839336']
        if groupNum not in whiteablum:
            await query.finish()

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+msg
        })
    else:
        await bot.call_api('send_private_msg', 
        **{'user_id':int(user_id), 'message': msg})

    await query.finish()


