from nonebot import on_command, get_bots
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.typing import T_State  
import nonebot
import random
import time, datetime, pytz
import json
from nonebot_plugin_apscheduler import scheduler




def initialize():
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    today = datetime.datetime(now.year, now.month, now.day)
    with open('src/plugins/mjj/data.json', 'r') as f:
        data = json.load(f)
    if 'time' not in data:
        data['time'] = str(today)
    if data['time'] != str(today):
        data['time'] = str(today)
        for key in data['rank'].keys():
            data['rank'][key] = {}
    with open('src/plugins/mjj/data.json', 'w') as fw:
        json.dump(data, fw, indent=2, separators=(',',': '), ensure_ascii=False)
    return data


mjjall_dic = initialize()


jrmjj = on_command('jrmjj')

@jrmjj.handle()
async def jrmjj_handle(bot: Bot, event: Event, state: T_State):

    global mjjall_dic

    session_id = event.get_session_id()

    if 'group' not in session_id:
        await jrmjj.finish()

    group_id = session_id.split('_')[1]
    user_qq = event.get_user_id()

    # whiteablum
    whiteablum = ['624627458','210839336']
    if group_id not in whiteablum:
        await jrmjj.finish()

    user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_qq, no_cache=True)
    if user_info['card'] != '':
        nickname = user_info['card']
    else:
        nickname = user_info['nickname']


    user_id = str(event.get_user_id())
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    today = datetime.datetime(now.year, now.month, now.day)
    un_time = time.mktime(today.timetuple())

    seed = int(event.get_user_id()) / un_time
    random.seed(seed)
    mjjvalue = random.randint(0, 100)

    msg = '请求JJ神明的旨示中......{}今天的有鸡鸡指数是:{}'.format(nickname, mjjvalue)


    await bot.call_api('send_group_msg', **{
        'group_id':int(group_id),
        'message': msg
    })

    if nickname not in mjjall_dic['rank'][group_id]:
        mjjall_dic['rank'][group_id][nickname] = mjjvalue
    
    with open('src/plugins/mjj/data.json', 'w') as fw:
        json.dump(mjjall_dic, fw, indent=2, separators=(',',': '), ensure_ascii=False)

    await jrmjj.finish()



mjjall = on_command('mjjall')

@mjjall.handle()
async def mjjall_handle(bot: Bot, event: Event, state: T_State):

    global mjjall_dic

    session_id = event.get_session_id()

    if 'group' not in session_id:
        await mjjall.finish()

    group_id = session_id.split('_')[1]
    user_qq = event.get_user_id()

    # whiteablum
    whiteablum = ['624627458','210839336']
    if group_id not in whiteablum:
        await mjjall.finish()
    
    rank_list = mjjall_dic['rank'][group_id]
    sorted_d = sorted(rank_list.items(), key=lambda x:x[1], reverse=True)

    msg = '今日有鸡鸡榜单: '
    cur_rank = 1
    for i in range(0, len(sorted_d)):
        if i!=0 and sorted_d[i][1] != sorted_d[i-1][1]:
            cur_rank = i+1
        tmpMsg = '\n{}. {} {}'.format(cur_rank, sorted_d[i][1], sorted_d[i][0])
        msg += tmpMsg
    
    await bot.call_api('send_group_msg', **{
        'group_id':int(group_id),
        'message': msg
    })

    await mjjall.finish()



@scheduler.scheduled_job("cron", hour="0", minute="0", id="resetmjj")
async def reset():
    global mjjall_dic
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    today = datetime.datetime(now.year, now.month, now.day)
    if 'time' not in mjjall_dic:
        mjjall_dic['time'] = str(today)
    if mjjall_dic['time'] != str(today):
        mjjall_dic['time'] = str(today)
        for key in mjjall_dic['rank'].keys():
            mjjall_dic['rank'][key] = {}
    with open('src/plugins/mjj/data.json', 'w') as fw:
        json.dump(mjjall_dic, fw, indent=2, separators=(',',': '), ensure_ascii=False)
    
    bot, = get_bots().values()
    await bot.call_api('send_group_msg', **{
        'group_id':624627458,
        'message': '新的一天祝大家jj向上'
    })


def is_today(ts):
    now_ts = int(time.time())
    spec_ts = int(ts)

    now_date = datetime.datetime.utcfromtimestamp(now_ts).strftime('%Y%m%d')
    spec_date = datetime.datetime.utcfromtimestamp(spec_ts).strftime('%Y%m%d')
    
    if now_date == spec_date:
        return True
    else:
        return False


@scheduler.scheduled_job("cron", hour="20", minute="0", id="getallmjj")
async def getallmjj():
    global mjjall_dic
    
    bot, = get_bots().values()
    group_id = '624627458'

    user_json = await bot.get_group_member_list(group_id=group_id, no_cache=True)
    for user in user_json:
        # user = await bot.get_group_member_info(group_id=group_id, user_id=user_cache['user_id'], no_cache=True)
        if not is_today(user['last_sent_time']):
            continue
        
        if user['card'] != '':
            nickname = user['card']
        else:
            nickname = user['nickname']
        if nickname in mjjall_dic['rank'][group_id]:
            continue
        user_id = str(user['user_id'])
        now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
        today = datetime.datetime(now.year, now.month, now.day)
        un_time = time.mktime(today.timetuple())

        seed = user['user_id'] / un_time
        random.seed(seed)
        mjjvalue = random.randint(0, 100)

        mjjall_dic['rank'][group_id][nickname] = mjjvalue
        
    with open('src/plugins/mjj/data.json', 'w') as fw:
        json.dump(mjjall_dic, fw, indent=2, separators=(',',': '), ensure_ascii=False)
    
    rank_list = mjjall_dic['rank'][group_id]
    sorted_d = sorted(rank_list.items(), key=lambda x:x[1], reverse=True)

    msg = '天光猛烈，万物显形！时辰已到, 今日有鸡鸡榜单:'
    cur_rank = 1
    average = 0
    for i in range(0, len(sorted_d)):
        if i!=0 and sorted_d[i][1] != sorted_d[i-1][1]:
            cur_rank = i+1
        average += sorted_d[i][1]
        tmpMsg = '\n{}. {} {}'.format(cur_rank, sorted_d[i][1], sorted_d[i][0])
        msg += tmpMsg
    
    average = int(average / len(sorted_d))
    msg += '\n==========\n'
    msg += '群平均鸡鸡值为{}, 今日最没鸡鸡的人是{}, 低于平均水平{}'.format(average, sorted_d[-1][0], average-sorted_d[-1][1])
    
    await bot.call_api('send_group_msg', **{
        'group_id':int(group_id),
        'message': msg
    })


# mjjcheck = on_command('sjmjj', aliases={'烧鸡没鸡鸡'})

# @mjjcheck.handle()
# async def mjjcheck_handle(bot: Bot, event: Event, state: T_State):

#     global mjjall_dic

#     session_id = event.get_session_id()

#     if 'group' not in session_id:
#         await mjjcheck.finish()

#     group_id = session_id.split('_')[1]
#     user_qq = event.get_user_id()

#     # whiteablum
#     whiteablum = ['624627458','210839336']
#     if group_id not in whiteablum:
#         await mjjcheck.finish()

#     user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_qq, no_cache=True)
#     if user_info['card'] != '':
#         nickname = user_info['card']
#     else:
#         nickname = user_info['nickname']

#     if nickname not in mjjall_dic['rank'][group_id]:
#         now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
#         today = datetime.datetime(now.year, now.month, now.day)
#         un_time = time.mktime(today.timetuple())
#         seed = int(event.get_user_id()) - un_time
#         random.seed(seed)
#         mjjvalue = random.randint(0, 100)
#         mjjall_dic['rank'][group_id][nickname] = mjjvalue
#     else:
#         mjjall_dic['rank'][group_id][nickname] = int((mjjall_dic['rank'][group_id][nickname]/10)**2)
    
#     with open('src/plugins/mjj/data.json', 'w') as fw:
#         json.dump(mjjall_dic, fw, indent=2, separators=(',',': '), ensure_ascii=False)

#     await bot.call_api('send_group_msg', **{
#         'group_id':int(group_id),
#         'message': '[CQ:at,qq='+str(user_qq)+'] 今日鸡鸡值已削减'
#     })

#     await mjjcheck.finish()