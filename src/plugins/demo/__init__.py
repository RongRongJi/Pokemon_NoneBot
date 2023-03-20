from nonebot import on_command, on_keyword, on_startswith
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, ArgPlainText, CommandArg, Matcher
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageEvent, PrivateMessageEvent, MessageSegment, GroupMessageEvent
from nonebot.typing import T_State  
import nonebot
import re
import json
import base64
import requests
import random
import subprocess
import sys
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

    resp = await bot.ocr_image(image=img_name[0])

    msg = ''
    for text in resp['texts']:
        msg += text['text'] + '\n'

    resp = await bot.call_api('.get_word_slices', **{
            'content': msg
        })
    msg = ''
    for text in resp['slices']:
        msg += text + '/'

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']' + msg
        })

    await demo.finish()