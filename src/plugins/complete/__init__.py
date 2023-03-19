from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Event
import nonebot
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, GroupIncreaseNoticeEvent
from nonebot import on_notice, on_keyword


noticeMsg = '''欢迎您参加AIP公会3.18-3.19举办的PVP OU分级比赛, 进群请修改名片为游戏id! 
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
    whiteablum = ['141778117']
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

        causalablum = ['141778117']
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
【瞻彼淇奥，绿竹猗猗】
欢迎参加AIP公会PVP OU分级比赛, 本次比赛按照天梯OU PVP条款及规则进行, 活动地点定于合众吹寄3频道。

比赛的赛制为分组单败淘汰制(暂定, 根据报名人数可能会出现轮空或者临时修改赛制的情况, 请见谅)。

分组单败淘汰制: 参赛人员将随机分为ABCD四组,每一组分别进行淘汰赛,失败一场即淘汰。不同分组的人只会在四强以上相遇。

活动的具体时间定于3月18日和3月19日晚上8点, 结束时间根据具体情况而定。
------
感谢您使用AIP自助机器人, 您可以at我并发送"帮助"来查看其它功能, 祝您游戏愉快!'''

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['141778117']
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
【瞻彼淇奥，绿竹猗猗】
欢迎参加AIP公会PVP OU分级比赛, 以下是本次活动的奖励:

奖池:(前四名从前往后任选)
1. 6v(攻击0)胆小头目春花闪鬼盆栽质子耿鬼
2. 6v内敛波克基斯
3. 5v爽朗梦特地龙
4. 5v爽朗玛狃拉
5. 5v慎重梦特蘑蘑菇

特别奖励: 使用最多非OU精灵并走到最远的选手将获得50w奖金。
评判标准: 每一轮每使用一只非OU精灵+2分, 使用非OU精灵每晋级一轮+3分, 分数最高者得奖。

参与奖: 2023年红包*5
------
感谢您使用AIP自助机器人, 您可以at我并发送"帮助"来查看其它功能, 祝您游戏愉快!'''

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['141778117']
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
【瞻彼淇奥，绿竹猗猗】
详细赛果如下: [CQ:image,file=match.png]
------
冠军:   hklaasss
亚军:   qqqianx
季军:   Cbco
第四名: TQAAQT
------
特别奖励排名
1. Cbco	22pt
2. TQAAQT 21pt
3. qqqianx 17pt
------
祝贺比赛顺利结束，恭喜以上所有选手，也恭喜所有选手'''

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['141778117']
        if groupNum not in whiteablum:
            await cp_walk.finish()

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+msg
        })

    await cp_walk.finish()

