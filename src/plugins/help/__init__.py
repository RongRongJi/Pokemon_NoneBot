from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.typing import T_State  
import nonebot


help = on_command('帮助', aliases={'help'}, rule=to_me())



@help.handle()
async def help_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()

    user_id = str(event.get_user_id())

    
    helpmsg = '.帮助 .help  : 查看自助机器人的详细指令 \n'
    luckmsg = '.今日运势 .jrys  :  查看您的今日运势 \n' 
    tjmsg = '#图鉴 xxx : 查询宝可梦图鉴 \n'
    calmsg = '.计算器 .cal  :  宝可梦伤害计算器 \n'
    spdmsg = '.速度线 .speed : pokemmo速度线查询 \n'
    tail = '\n自助机器人仍在开发中,如您有任何好的建议,欢迎私聊留言!'
    msg = '欢迎使用AIP公会自助机器人, 您可以根据以下的命令使用对应功能:\n命令: \n' + helpmsg + luckmsg + tjmsg + calmsg + spdmsg + tail

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['860189236', '210839336']
        if groupNum not in whiteablum:
            await lucky.finish()

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']' + '\n' +msg
        })
    else:
        await bot.call_api('send_private_msg', 
        **{'user_id':int(user_id), 'message': msg})

    await help.finish()


