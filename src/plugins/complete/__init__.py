from nonebot import on_command, get_bots
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Event
import nonebot
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, GroupIncreaseNoticeEvent
from nonebot import on_notice, on_keyword
from nonebot_plugin_apscheduler import scheduler


noticeMsg = '''欢迎您参加樱落&AIP公会5.1举办的PVP OU分级比赛, 进群请修改名片为游戏id! 
我是AIP公会自助机器人, 您可以根据at我, 并跟上以下指令来呼唤我, 希望可以给您更好的活动体验!
----通用----
帮助 help  : 查看自助机器人的详细指令
今日运势 jrys : 查看您的今日运势
---比赛相关---
赛制 : 查看比赛赛制
奖品 : 查看比赛奖品
赛程 : 查看赛程与分组
-----PVP-----
计算器 cal  :  宝可梦伤害计算器
速度线 speed : pokemmo速度线查询
自助机器人仍在开发中,如您有任何好的建议,欢迎私聊留言!'''


cp_notice = on_notice()

@cp_notice.handle()
async def cp_notice_handle(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):
    user = event.get_user_id()
    at_ = '[CQ:at,qq={}]'.format(user)

    msg = at_ + noticeMsg

    # whiteablum
    whiteablum = ['523485781']
    groupNum = str(event.group_id)
    if groupNum not in whiteablum:
        await cp_notice.finish()

    await bot.call_api('send_group_msg', **{
        'group_id':int(groupNum),
        'message': msg
    })

    await cp_notice.finish()


cp_help = on_command('帮助', priority=1, aliases={'help'}, rule=to_me())

@cp_help.handle()
async def cp_help_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        causalablum = ['523485781']
        if groupNum in causalablum:
            await bot.call_api('send_group_msg', **{
                'group_id':int(groupNum),
                'message': '[CQ:at,qq='+user_id+']' + '\n' +noticeMsg
            })
        else:
            await cp_help.finish()

    await cp_help.finish()


cp_rule = on_keyword({'赛制','规则','比赛'}, rule=to_me())

@cp_rule.handle()
async def cp_rule_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    msg = '''
【唐草之战！樱落武斗祭！】
欢迎参加樱落&AIP公会PVP OU分级比赛, 本次比赛按照天梯OU PVP条款及规则进行, 活动地点定于合众唐草2频道。

比赛的赛制为分组单败淘汰制。

分组单败淘汰制: 参赛人员将随机分为ABCD四组,每一组分别进行淘汰赛,失败一场即淘汰。不同分组的人只会在四强以上相遇。

活动的具体时间定于5月1日晚上8点, 结束时间根据具体情况而定。
------
感谢您使用AIP自助机器人, 您可以at我并发送"帮助"来查看其它功能, 祝您游戏愉快!'''

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['523485781']
        if groupNum not in whiteablum:
            await cp_rule.finish()

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+msg
        })

    await cp_rule.finish()


cp_ward = on_keyword({'奖品','奖励','等奖'}, rule=to_me())

@cp_ward.handle()
async def cp_ward_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    msg = '''
【唐草之战！樱落武斗祭！】
欢迎参加樱落&AIP公会PVP OU分级比赛, 以下是本次活动的奖励:

一轮胜者:随机礼袋x1。
二轮胜者:随机礼袋x3。
三轮胜者:随机礼袋x5。
四轮胜者:随机礼袋x10。
五轮胜者:随机礼袋x20。

名次奖励:
第一名:闪光宝可梦(或帝陨+鬼盆栽双质子百变怪x2)
第二名:5V对性宝可梦(或帝陨+鬼盆栽双质子百变怪)
第三名:3v2u对性班基拉斯(或同价值礼袋)
第四名:精灵球x300(或同价值礼袋)+2V宝可梦

特别奖励: 使用最多非OU精灵并走到最远的选手将获得50w奖金（或相同价值礼袋）。
评判标准: 每一轮每使用一只非OU精灵+2分, 使用非OU精灵每晋级一轮+3分, 分数最高者得奖。

------
感谢您使用AIP自助机器人, 您可以at我并发送"帮助"来查看其它功能, 祝您游戏愉快!'''

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['523485781']
        if groupNum not in whiteablum:
            await cp_ward.finish()

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+msg
        })

    await cp_ward.finish()


cp_walk = on_keyword({'赛程','赛果','结果'}, rule=to_me())

@cp_walk.handle()
async def cp_walk_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    msg = '''
【唐草之战！樱落武斗祭！】
第一名: SHXU
第二名: oseisei
第三名: qqqianx
第四名: FKisSB
特别奖励:
SHXU & oseisei 22分
恭喜以上选手！
====
[CQ:image,file=match.png]'''

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['523485781']
        if groupNum not in whiteablum:
            await cp_walk.finish()

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+msg
        })

    await cp_walk.finish()


# # 发送比赛信息
# @scheduler.scheduled_job("cron", hour="10", minute="0", id="noticecompete")
# async def trade_section():
#     bot, = get_bots().values()
#     msg = '''【唐草之战！樱落武斗祭！】
# 活动内容：劳动节在唐草镇举办OU分级PVP对战，胜者晋级，败者拿奖励，在报名时间内群内私聊rong报名。
# rong QQ:1150289431。
# 对战条例条例全开。
# 对战位置：合众 唐草镇 频道2
# 比赛时间：2023年5月1日20：00。
# 报名时间：即日起~4月27日20:00。
# 活动奖励:
# 一轮胜者:随机礼袋x1。
# 二轮胜者:随机礼袋x3。
# 三轮胜者:随机礼袋x5。
# 四轮胜者:随机礼袋x10。
# 五轮胜者:随机礼袋x20。

# 名次奖励:
# 第一名:闪光宝可梦(或帝陨+鬼盆栽双质子百变怪x2)
# 第二名:5V对性宝可梦(或帝陨+鬼盆栽双质子百变怪)
# 第三名:3v2u对性班基拉斯(或同价值礼袋)
# 第四名:精灵球x300(或同价值礼袋)+2V宝可梦

# 特别奖:使用最多非OU精灵并走到最远的选手将获得50w奖金（或相同价值礼袋）
# 评判标准:每一轮每使用一只非OU精灵+2分，使用非OU精灵每晋级一轮+3分，分数最高者得奖[CQ:at,qq=all]

# '''
#     await bot.call_api('send_group_msg', **{
#         'group_id':860189236,
#         'message': msg
#     })
