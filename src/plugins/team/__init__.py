from nonebot import on_command, on_keyword
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.typing import T_State  
import nonebot


def get_image(name):
    image = "[CQ:image,file=team/{}.png]".format(name)
    return image


teams = ["火狒攻","双蛙雨","飞爆破","蜻蜓攻","狃拉受","龙虾空间"]


team = on_keyword({'队伍'}, rule=to_me())


@team.handle()
async def team_handle(bot: Bot, event: Event, state: T_State):

    team_name = str(event.get_message()).strip()
    team_name = team_name.strip('队伍').replace(' ','')
    print(team_name)

    if team_name not in teams:
        msg = '''很高兴为您推荐Pokemmo PVP队伍,请在[队伍]指令后面添加以下队伍名称来查询队伍详细配置!
---新手推荐---
双蛙雨
-----攻队-----
火狒攻/双蛙雨/飞爆破/蜻蜓攻
----空间队----
龙虾空间队
-----受队-----
狃拉受
'''
    else:
        msg = team_name + '配置如下: ' + get_image(team_name)
        msg += '\n*队伍只是参考,适合自己的才是最好的'


    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['860189236', '210839336', '624627458','1078694756']
        if groupNum not in whiteablum:
            await team.finish()

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+msg
        })
    else:
        await bot.call_api('send_private_msg', 
        **{'user_id':int(user_id), 'message': msg})

    await team.finish()


