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


subprocess.Popen([sys.executable, "src/plugins/records/task_server.py"])


record_dict = {}

with open('src/plugins/records/record.json', 'r') as fr:
    record_dict = json.load(fr)


 # 语录库
record = on_command("开始上传", aliases={"上传", '上传开始'}, priority=10, block=True, rule=to_me())
end_conversation = ['stop', '结束', '上传截图', '结束上传']

# 配置
cqhttp_path = '/home/sr/go-cqhttp/'


@record.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    if isinstance(event, PrivateMessageEvent):
        await record.finish()

    plain_text = args.extract_plain_text()
    if plain_text:
        record.set_arg("prompt", message=args)


def img_to_base64(img_path):
    with open(img_path, 'rb')as read:
        b64 = base64.b64encode(read.read())
    return b64

@record.got("prompt", prompt="请上传语录(图片形式)")
async def record_upload(bot: Bot, event: MessageEvent, prompt: Message = Arg(), msg: Message = Arg("prompt")):

    session_id = event.get_session_id()
    message_id = event.message_id

    if str(msg) in end_conversation:
        await record.finish('上传会话已结束')

    rt = r"\[CQ:image,file=(.*?),subType=[\S]*,url=[\S]*\]"

    files = re.findall(rt, str(msg))

    if len(files) == 0:
        resp = "请上传图片"
        await record.reject_arg('prompt', MessageSegment.reply(message_id) + resp)

    resp =  await bot.call_api('get_image',  **{'file':files[0]})

    # 下载图片
    url_model = r"\[CQ:image,file=[\S]*,subType=[\S]*,url=(.*?)\]"
    url = re.findall(url_model, str(msg))[0]
    path = 'src/plugins/records/images/' + files[0] + '.jpg'
    with open(path, 'wb') as f:
        img = requests.get(url).content
        f.write(img)
    # 转base64
    img_b64 = img_to_base64(path)
    # 删除图片
    os.remove(path)


    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        resp['file'] = resp['file'].replace('data/','../')

        res = requests.post(url='http://127.0.0.1:5555/offer', 
                data={'group_id': groupNum,
                    'img_file': resp['file'],
                    'content': img_b64})  

        if groupNum not in record_dict:
            record_dict[groupNum] = [resp['file']]
        else:
            if resp['file'] not in record_dict[groupNum]:
                record_dict[groupNum].append(resp['file'])


        with open('src/plugins/records/record.json', 'w') as f:
            json.dump(record_dict, f,indent=2,separators=(',', ': '),ensure_ascii=False)

    # await record.reject_arg('prompt', MessageSegment.reply(message_id) + '上传成功')
    await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': MessageSegment.reply(message_id) + '上传成功'
        })
    await record.finish('上传会话已结束')



record_pool = on_startswith('语录', priority=2, block=True, rule=to_me())

@record_pool.handle()
async def record_pool_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    if 'group' in session_id:

        search_info = str(event.get_message()).strip()
        search_info = search_info.replace('语录','').replace(' ','')

        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        if search_info == '':
            if groupNum not in record_dict:
                msg = '当前无语录库'
            else:
                length = len(record_dict[groupNum])
                idx = random.randint(0, length-1)
                msg = '[CQ:image,file={}]'.format(record_dict[groupNum][idx])
        else:
            r = requests.get('http://127.0.0.1:5555/query', 
                {'group_id':groupNum, 'sentence': search_info})

            ret = r.json()


            if ret['status'] == -1:
                msg = '当前无语录库'
            elif ret['status'] == 2:
                length = len(record_dict[groupNum])
                idx = random.randint(0, length-1)
                msg = '当前查询无结果, 为您随机发送。\n[CQ:image,file={}]'.format(record_dict[groupNum][idx])
            elif ret['status'] == 1:
                msg = '[CQ:image,file={}]'.format(ret['msg'])
            else:
                msg = ret.text

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': msg
        })

    await record_pool.finish()


record_help = on_keyword({"语录"}, priority=10, rule=to_me())

@record_help.handle()
async def record_help_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    msg = '''您可以通过at我+上传, 开启上传语录通道; 再发送图片上传语录。您也可以通过at我+语录, 我将随机返回一条语录。'''

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']' + msg
        })

    await record_help.finish()