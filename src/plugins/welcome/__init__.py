from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, GroupIncreaseNoticeEvent
from nonebot import on_notice


welcome = on_notice()

@welcome.handle()
async def welcome_handle(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):
    user = event.get_user_id()
    at_ = '[CQ:at,qq={}]'.format(user)
    msg = at_ + '欢迎您加入AIP大家庭! 我是AIP公会自助机器人, 您可以根据at我, 并跟上以下指令来呼唤我, 希望可以给您更好的游戏体验!\n'

    helpmsg = '/帮助 /help  : 查看自助机器人的详细指令 \n'
    luckmsg = '/今日运势 /jrys  :  查看您的今日运势 \n' 
    tjmsg = '#图鉴 xxx : 查询宝可梦图鉴 \n'
    calmsg = '.计算器 .cal  :  宝可梦伤害计算器 \n'
    spdmsg = '.速度线 .speed : pokemmo速度线查询 \n'
    dicemsg = '.骰子 .dice  : 投骰子 \n'
    rollmsg = '.投掷 .roll : 0-100随机数字 \n'
    tail = '\n自助机器人仍在开发中,如您有任何好的建议,欢迎私聊留言!'
    msg = msg + helpmsg + luckmsg + tjmsg + calmsg + spdmsg + dicemsg + rollmsg + tail


    # whiteablum
    whiteablum = ['860189236', '210839336']
    groupNum = str(event.group_id)
    if groupNum not in whiteablum:
        await welcome.finish()

    await bot.call_api('send_group_msg', **{
        'group_id':int(groupNum),
        'message': msg
    })

    await welcome.finish()

