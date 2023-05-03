from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.typing import T_State  
import nonebot
from .func import make_rand_arr
import random
import time, datetime, pytz


lucky = on_command('今日运势', aliases={'jrys'}, rule=to_me())

arr = make_rand_arr()
total_arr = []
for ar in arr:
    for i in range(0, ar['rare']):
        total_arr.append(ar['name'])

@lucky.handle()
async def lucky_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    print(session_id)


    user_id = str(event.get_user_id())
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    today = datetime.datetime(now.year, now.month, now.day)
    un_time = time.mktime(today.timetuple())

    # lucky monster
    seed = int(event.get_user_id()) + un_time
    random.seed(seed)
    res = random.randint(0,len(total_arr))
    lucky_pokemon = total_arr[res]

    # shine lucky
    seed = int(event.get_user_id()) - un_time
    random.seed(seed)
    shine = random.randint(0, 100)

    # pvp lucky
    seed = (int(event.get_user_id()) - un_time)*2
    random.seed(seed)
    pvp = random.randint(0, 100)

    # box lucky
    seed = (int(event.get_user_id()) - 2*un_time)
    random.seed(seed)
    box = random.randint(0, 100)

    # message
    shineMsg = '闪光运气值: ' + str(shine)
    pvpMsg = '对战运气值: ' + str(pvp)
    boxMsg = '开盒运气值: ' + str(box)
    luckyMsg = '幸运宝可梦: ' + lucky_pokemon

    addition = ""
    if shine >= 70 and pvp >= 70 and box >= 70:
        addition = '今天的您诸事皆宜！'
    elif shine >= 70:
        addition = '今天的您有可能会遇到闪光宝可梦哦！'
    elif pvp >= 70:
        addition = '今天的您PVP会上大分哦！'
    elif box >= 70:
        addition = '今天该开盒了! '
    elif shine <= 30 and pvp <= 30 and box <= 30:
        addition = '今天的您诸事不宜QAQ,不过'

    msg = pvpMsg + '\n' + shineMsg + '\n' + boxMsg + '\n' + luckyMsg + '\n' + addition + '祝您今天也在Pokemmo中拥有愉快的一天！'

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['860189236', '210839336', '523485781']
        if groupNum not in whiteablum:
            await lucky.finish()

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+
            ' 您好！下面是您今天的运势：\n'+msg
        })
    else:
        await bot.call_api('send_private_msg', 
        **{'user_id':int(user_id), 'message': ' 您好！下面是您今天的运势：\n'+msg})

    await lucky.finish()



daily_draw = on_command('今日抽奖', aliases={'jrcj','抽奖'}, rule=to_me())

@daily_draw.handle()
async def daily_draw_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    print(session_id)

    # 精灵球 随机v素材 随机礼袋 随机药品 随机服装 幸运精灵
    user_id = str(event.get_user_id())
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    today = datetime.datetime(now.year, now.month, now.day)
    un_time = time.mktime(today.timetuple())
    sj = '{}-{}-{}'.format(now.year, now.month, now.day)


    # box lucky
    seed = (int(event.get_user_id()) * un_time)
    random.seed(seed)
    box = random.randint(0, 100)

    if box >=0 and box < 18:
        msg = '精灵球'
    elif box < 36:
        msg = '随机v素材'
    elif box < 54:
        msg = '随机礼袋'
    elif box < 72:
        msg = '随机药品'
    elif box < 90:
        msg = '随机服装'
    else:
        msg = '幸运精灵'


    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['860189236', '210839336']
        if groupNum not in whiteablum:
            await daily_draw.finish()

        if now.hour >= 22 or now.hour < 8:
            await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+
            ' 抽奖的营业时间为每天8:00-22:00~'
            })
            await daily_draw.finish()

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+
            ' 恭喜您训练师！今天(' + sj + ')您的抽奖结果是：'+msg+ '\n请截图并于当天找羽墨(QQ:2090013496)进行兑奖，逾期作废'
        })

    await daily_draw.finish()
