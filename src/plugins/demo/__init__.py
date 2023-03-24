from nonebot import on_command, on_keyword, on_startswith, on_notice
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, ArgPlainText, CommandArg, Matcher
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageEvent, PrivateMessageEvent, MessageSegment, GroupMessageEvent, exception
from nonebot.typing import T_State  
from nonebot.adapters.cqhttp import PokeNotifyEvent
import nonebot
import re
import json
import base64
import requests
import random
import subprocess
import sys
import jieba
import os


demo = on_keyword({"demo"}, priority=10, rule=to_me())

@demo.handle()
async def demo_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    message_id = event.message_id
    user_id = str(event.get_user_id())
    raw_message = str(event)

    # rt = r"\[reply:id=(.*?)]"
    # ids = re.findall(rt, str(raw_message))

    # resp = await bot.get_msg(message_id=ids[0])

    # img_msg = str(resp['message'])

    rt = r"\[CQ:image,file=(.*?),subType=[\S]*,url=[\S]*\]"
    img_name = re.findall(rt, str(event.get_message()))
    # msg = img_name[0]

    try:
        resp = await bot.ocr_image(image=img_name[0])

        msg = handle_ocr_text(resp['texts'])
        print(msg)

    except exception.ActionFailed:
        msg = ''


    cut_words = cut_sentence(msg)

    msg = str(cut_words)

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']' + msg
        })

    await demo.finish()



demo_c = on_keyword({"分词"}, priority=10, rule=to_me())

@demo_c.handle()
async def demo_c_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    message_id = event.message_id
    user_id = str(event.get_user_id())

    msg = str(event.get_message())
    msg = msg.replace('分词','')

    cut_words = jieba.lcut_for_search(msg)
    msg = ''
    for text in cut_words:
        msg += text + '/'


    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']' + msg
        })

    await demo_c.finish()


def handle_ocr_text(texts):
    '''
    texts['text']  : str
    texts['coordinates'] : vector2[]
    '''
    _len_ = len(texts)
    if _len_ == 0:
        return ''
    ret = texts[0]['text']
    for i in range(1, _len_):
        _last_vectors = texts[i-1]['coordinates']
        _cur_vectors = texts[i]['coordinates']
        _last_width = _last_vectors[1]['x'] - _last_vectors[0]['x']
        _cur_width = _cur_vectors[1]['x'] - _cur_vectors[0]['x']
        _last_start = _last_vectors[0]['x']
        _cur_start = _cur_vectors[0]['x']

        _last_end = _last_vectors[1]['x']
        _cur_end = _cur_vectors[1]['x']
        print(_last_end, _cur_end, _last_width, _cur_width)
        # 起始点判断 误差在15以内 
        # 长度判断 上一句比下一句长 误差在5以内
        if abs(_cur_start - _last_start) <= 15 and _last_width + 5 > _cur_width:
            # 判定为长句换行了
            ret += texts[i]['text']
        # 终点判断 误差在15以内
        # 长度判断 上一句比下一句短 误差在5以内
        elif abs(_cur_end - _last_end) <= 15 and _cur_width + 5 > _last_width:
            # 判定为长句换行了
            ret += texts[i]['text']
        else:
            ret += '\n' + texts[i]['text']
    
    return ret


def cut_sentence(sentence):
    cut_words = jieba.lcut_for_search(sentence)
    cut_words = list(set(cut_words))
    remove_set = set(['.',',','!','?',':',';','。','，','！','？','：','；','%','$','\n',' ','[',']'])
    new_words = [word for word in cut_words if word not in remove_set]

    print(new_words)
    return new_words