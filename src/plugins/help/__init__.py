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

    
    helpmsg = '帮助 help  : 查看自助机器人的详细指令 \n'
    tjmsg = '图鉴+精灵名称 : 查询宝可梦图鉴 \n'

    mmomsg = '''帮助 help  : 查看自助机器人的详细指令
今日运势 jrys  :  查看您的今日运势
---PVP---
图鉴+精灵名称 : 查询宝可梦图鉴
配置+精灵名称 : 查询mmo PVP中常见配置
计算器 cal  :  宝可梦伤害计算器
速度线 speed : pokemmo速度线查询
队伍+队伍名称: 查询PVP队伍详细配置
---日常---
天王 : 查询mmo中搬天王的配置
捡垃圾 : 捡垃圾地点推荐
努力值 : 查看努力值纯点分布
素材点 : 查看素材纯点分布
技能点+技能名称 : 查询NPC教学地区
'''

    dicemsg = '骰子 dice  : 投骰子 \n'
    rollmsg = '投掷 roll : 0-100随机数字 \n'
    gptmsg = 'gpt3 +语句 : 和机器人聊天 \n'
    # casualmsg = dicemsg + rollmsg + gptmsg
    casualmsg = gptmsg
    
    tail = '\n自助机器人仍在开发中,如您有任何好的建议,欢迎私聊留言!'

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        mmoablum = ['860189236', '210839336']
        causalablum = ['624627458', '1078694756']
        if groupNum in mmoablum:
            msg = mmomsg + casualmsg + tail
            msg = '欢迎使用AIP公会自助机器人, 您可以根据以下的命令使用对应功能:\n命令: \n' + msg
            await bot.call_api('send_group_msg', **{
                'group_id':int(groupNum),
                'message': '[CQ:at,qq='+user_id+']' + '\n' +msg
            })
        elif groupNum in causalablum:
            msg = helpmsg + tjmsg + casualmsg + tail
            msg = '您可以根据以下的命令使用对应功能:\n命令: \n' + msg
            await bot.call_api('send_group_msg', **{
                'group_id':int(groupNum),
                'message': '[CQ:at,qq='+user_id+']' + '\n' +msg
            })
        else:
            await help.finish()
    else:
        msg = helpmsg + tjmsg + casualmsg + tail
        msg = '您可以根据以下的命令使用对应功能:\n命令: \n' + msg
        await bot.call_api('send_private_msg', 
        **{'user_id':int(user_id), 'message': msg})

    await help.finish()


