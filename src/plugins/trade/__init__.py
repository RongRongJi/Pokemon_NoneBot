from nonebot import on_command, get_bots, on_keyword
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
from .utils import compare_all_items, graph_item, price_item
import jieba


item2id = {}
with open('/home/sr/project/test/src/plugins/trade/items.json', 'r', encoding='UTF-8') as fr:
    item2id = json.load(fr)



price_query = on_keyword({"价格"}, rule=to_me())

@price_query.handle()
async def price_query_handle(bot: Bot, event: Event, state: T_State):

    global item2id

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())
    raw_msg = str(event.get_message())
    search_info = raw_msg.replace("价格","").replace(" ","")

    if 'group' not in session_id:
        await price_query.finish('私聊暂不提供此功能')
    
    group_id = int(session_id.split('_')[1])
    if group_id not in [860189236, 210839336]:
        await price_query.finish()

    # 查找对应id
    itemid = -1
    item_name = ''
    search_words = set(jieba.cut(search_info, cut_all=False))
    for key,value in item2id.items():
        isThis = True
        for word in search_words:
            # print(word, key)
            if word not in key:
                isThis = False
        if isThis == True:
            itemid = value['id']
            item_name = key
            break
    print(itemid, item_name)

    # 没找到
    if itemid == -1:
        await bot.call_api('send_group_msg', **{
            'group_id':group_id,
            'message': '[CQ:at,qq='+user_id+']' + '没有找到该物品的数据'
        })
        await price_query.finish()

    await bot.call_api('send_group_msg', **{
            'group_id':group_id,
            'message': '[CQ:at,qq='+user_id+']' + f'正在生成{item_name}统计数据，请稍后'
        })
    # 生成统计图
    await graph_item(
        f'3个月内{item_name}价格趋势', 
        itemid, 
        f'/home/sr/newgocq/data/images/{user_id}.png', 
        f'/home/sr/project/spider/tmp/{user_id}.html')
    # 生成低价图
    try:
        await price_item(item_name, itemid, f'/home/sr/newgocq/data/images/{user_id}price.png')      
        msgs = [f'交易行{item_name}数据一览', f'[CQ:image,file={user_id}.png]', f'[CQ:image,file={user_id}price.png]']
    except IndexError:
        msgs = [f'交易行{item_name}数据一览', f'[CQ:image,file={user_id}.png]', '交易行无库存']

    def to_json(msg):
        return {"type": "node", "data": {"name": 'AIP bot', "uin": bot.self_id, "content": msg}}

    messages = [to_json(msg) for msg in msgs]
    await bot.call_api(
        "send_group_forward_msg", group_id=event.group_id, messages=messages
    )
    await price_query.finish()


# 发送交易行信息
@scheduler.scheduled_job("cron", hour="0/6", minute="40", id="tradesection")
async def trade_section():
    await compare_all_items(2, '12小时内交易行波动情况', '/home/sr/newgocq/data/images/hour.png', 10, 9999)
    bot, = get_bots().values()
    await bot.call_api('send_group_msg', **{
        'group_id':860189236,
        'message': '以下是12小时内交易行波动情况(已过滤单价较低和波动较小的物品)'
    })

    await bot.call_api('send_group_msg', **{
        'group_id':860189236,
        'message': '[CQ:image,file=hour.png]'
    })



trade_now = on_command('行情', rule=to_me())

@trade_now.handle()
async def trade_now_handle(bot: Bot, event: Event, state: T_State):

    if event.group_id not in [860189236, 210839336]:
        await trade_now.finish()

    await bot.call_api('send_group_msg', **{
        'group_id':event.group_id,
        'message': '[CQ:image,file=hour.png]'
    })