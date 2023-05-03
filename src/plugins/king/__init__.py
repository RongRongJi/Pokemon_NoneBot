from nonebot import on_command, on_keyword
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.typing import T_State  
import nonebot


king = on_command('天王', aliases={'king'}, rule=to_me())


@king.handle()
async def king_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    msg = '''天王表格辅助网站: http://m.caizhy.cn/
蛋蝎队白嫖码： 
5BF05372BD40DAAC9E9C614856374757 
业海嫖码: 
D1258C03AABF88C710D1D62AFA513C1D 
勇敢牛队白嫖码： 
31A40436E03D869E3A19A9C415D35B1C 
鱼鱼队白嫖码： 
0157A6FE080E14D0606B7721615FE7A7 
笨蛋龙白嫖码： 
01119190970EFC07C028146FCAF7A682 
定天鬼队白嫖码： 
B4AA2CAE12D48E3B95FC0E3AD15C55D1 
莽夫队白嫖码：(更新中) 
E34591E1873AAF298999A112E9DD4F68 
天蝉队白嫖码: 
F29170059077262738A0AB8E1665D932 
虫虫队白嫖码： 
6258A32D8B904B9E4E813B385A9985A3 
真蝎队白嫖码： 
17E5BE35894C3764BB26BFB3871A2AB5 
鬼舞队白嫖码： 
旧码(有天王基础会联防用):FBADCBD67510DA00BCD331D9C3EBEEA2 
新码(无基础萌新用):13F5D25C84FB11CF9095455422B388C9'''

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['860189236', '210839336']
        if groupNum not in whiteablum:
            await king.finish()

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+msg
        })
    else:
        await bot.call_api('send_private_msg', 
        **{'user_id':int(user_id), 'message': msg})

    await king.finish()


