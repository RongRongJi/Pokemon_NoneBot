import aiohttp
import nonebot
from nonebot.plugin import on_regex
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment, GroupMessageEvent,PrivateMessageEvent
import re
import os
from bs4 import BeautifulSoup
from lxml import html
from nonebot.rule import to_me
import math



wiki = on_regex(pattern="^{}\ ".format('查询'))


@wiki.handle()
async def _(bot: Bot, event: Event):
    raw_msg = str(event.message)
    info = raw_msg.split(' ')
    if len(info) != 2:
        wiki.finish(MessageSegment.reply(event.message_id) +'参数过多')

    key = info[1]
    msg = await main(key)
    if msg is None:
        await wiki.finish(MessageSegment.reply(event.message_id) +'请输入正确的名称')
    else:
        await wiki.finish(MessageSegment.reply(event.message_id) + msg)
    
    await wiki.finish()



async def main(name):
    url = "https://wiki.52poke.com/wiki/" + name
    async with aiohttp.ClientSession() as session:
        c = await session.get(url=url)
        resp_html = await c.text()
        soup = BeautifulSoup(resp_html, features='lxml')
        title = soup.find('span', class_='mw-page-title-main').text
        if '招式' in title:
            div = soup.find('div', class_="mw-parser-output").find('table', class_="roundy").find('tbody')
            desc = div.find('td', class_="roundy").text # 技能描述

            arr = div.find_all('td', class_="roundyright")
            attr = arr[0].text.strip() # 属性
            sort = arr[1].text.strip() # 分类
            pp = div.find('td', class_="roundytr").text.strip() #pp

            arr = div.find_all('td', class_="at-l")
            dmg = arr[3].text.strip() # 伤害
            hit = arr[4].text.strip() # 命中

            detail = div.find('td', class_="roundybottom").find('ul').text.strip() # 详细描述
            detail = detail.replace('\n', ',')

            h2 = soup.find('h2')
            eff = '' # 招式效果
            h2_next = h2.find_next('h2')
            h2 = h2.next.next
            while h2.next != h2_next:
                if h2.name == 'p':
                    eff += h2.text
                h2 = h2.next
            eff = eff.replace('\n', '')
            msg = '''{}
{}
属性: {}  分类: {}  
PP: {}  威力: {}  命中: {}
招式附加效果:
{}
招式详细说明:
{}'''.format(title, desc, attr, sort, pp, dmg, hit, eff, detail)
        elif '道具' in title:
            h2 = soup.find('h2')
            eff = '' # 效果
            detail = '' # 详细
            h2_next = h2.find_next('h2')
            h2 = h2.next.next
            while h2.next != h2_next:
                if h2.name == 'p':
                    eff += h2.text
                elif h2.name == 'ul' and h2.parent.name == 'div':
                    detail += '\n· ' + h2.text
                h2 = h2.next
            msg = '''{}
{}
详细说明:{}'''.format(title, eff, detail)
        elif '状态' in title or '特性' in title:
            h2 = soup.find('h2')
            eff = ''
            h2_next = h2.find_next('h2')
            h2 = h2.next.next
            while h2.next != h2_next:
                if h2.parent.name == 'div':
                    eff += h2.text
                h2 = h2.next
            msg = '''{}
{}'''.format(title, eff)

        return msg
        

