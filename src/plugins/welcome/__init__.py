from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, GroupIncreaseNoticeEvent
from nonebot import on_notice


welcome = on_notice()

@welcome.handle()
async def welcome_handle(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):
    user = event.get_user_id()
    at_ = '[CQ:at,qq={}]'.format(user)

    msg = at_ + '''欢迎您加入AIP大家庭! 我是AIP公会自助机器人, 您可以根据at我, 并跟上以下指令来呼唤我, 希望可以给您更好的游戏体验!
帮助 help  : 查看自助机器人的详细指令
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
gpt3 +语句 : 和机器人聊天
自助机器人仍在开发中,如您有任何好的建议,欢迎私聊留言!'''



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

