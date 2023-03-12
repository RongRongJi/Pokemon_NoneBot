from nonebot import on_command, on_keyword
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, ArgPlainText, CommandArg, Matcher
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageEvent, PrivateMessageEvent, MessageSegment, GroupMessageEvent
from nonebot.typing import T_State  
import nonebot
import re
import json
import random


record_dict = {}

with open('src/plugins/remember/record.json', 'r') as fr:
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


@record.got("prompt", prompt="请上传语录(图片形式)")
async def record_upload(bot: Bot, event: MessageEvent, prompt: Message = Arg(), msg: Message = Arg("prompt")):

    session_id = event.get_session_id()
    message_id = event.message_id

    if str(msg) in end_conversation:
        await record.finish('上传会话已结束')

    rt = r"\[CQ:image,file=(.*?),subType=[\S]*,url=[\S]*\]"

    msg = re.findall(rt, str(msg))

    if len(msg) == 0:
        resp = "请上传图片"
        await record.reject_arg('prompt', MessageSegment.reply(message_id) + resp)


    # resp = await get_user_session(session_id).get_chat_response(msg, checker(event))
    # resp = await handle_msg(resp)
    resp =  await bot.call_api('get_image',  **{'file':msg[0]})

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        resp['file'] = resp['file'].replace('data/','../')

        if groupNum not in record_dict:
            record_dict[groupNum] = [resp['file']]
        else:
            if resp['file'] not in record_dict[groupNum]:
                record_dict[groupNum].append(resp['file'])

        with open('src/plugins/remember/record.json', 'w') as f:
            json.dump(record_dict, f)

    # await record.reject_arg('prompt', MessageSegment.reply(message_id) + '上传成功')
    await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': MessageSegment.reply(message_id) + '上传成功'
        })
    await record.finish('上传会话已结束')



record_pool = on_command('语录库',  rule=to_me())


@record_pool.handle()
async def record_pool_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    msg = '[CQ:image,file=speed.png] 该速度线来自@b站 Pokemmo-VFU'

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        if groupNum in record_dict:
            length = len(record_dict[groupNum])
            idx = random.randint(0, length-1)
            msg = '[CQ:image,file={}]'.format(record_dict[groupNum][idx])
        else:
            msg = '当前无语录库'

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': msg
        })

    await record_pool.finish()