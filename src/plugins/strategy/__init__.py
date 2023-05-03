from nonebot import on_command, on_keyword
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.typing import T_State  
import nonebot



#捡垃圾

dust = on_command('捡垃圾', aliases={'rubbish'}, rule=to_me())


@dust.handle()
async def dust_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    msg = '''为您推荐捡垃圾的地点:
1.合众小波湾-水面
优点: 聚宝收益高,垃圾多
---------
2.合众龙螺旋之塔-钓鱼
优点: 聚宝收益较高,垃圾较多,有概率闪迷你龙
缺点: 野蛮鲈鱼非常凶狠
---------
3.合众龙螺旋之塔-水面
优点: 配置需求低,垃圾较多
缺点: 总体收益较低,野蛮鲈鱼非常凶狠
---------
4.合众龙螺旋之塔-外草地
优点: 配置需求低,垃圾多
缺点: 聚宝收益较低
---------
5.合众13号道路-水面
优点: 聚宝收益较高,有概率闪海星星
---------
6.合众古代城堡
优点:聚宝收益高,有概率闪燃烧虫,有古代钱币
缺点:路途远,念力土偶会大爆炸'''

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['860189236', '210839336']
        if groupNum not in whiteablum:
            await dust.finish()

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+msg
        })
    else:
        await bot.call_api('send_private_msg', 
        **{'user_id':int(user_id), 'message': msg})

    await dust.finish()



#素材点
materia = on_command('素材点', aliases={'materia'}, rule=to_me())


@materia.handle()
async def materia_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    msg = '''
陆上组: 合众1号路, 小约克/探探鼠
怪兽组: 丰缘卡绿隧道, 咕妞妞
人形组: 关都灯火山1F, 豪力
不定形组: 合众天堂塔2F, 烛光灵
植物/妖精组: 关都回忆之岛, 毽子草
水1/飞行组: 丰缘104号水面, 长翅鸥
水2/龙组: 关都枯叶市/丰缘琉璃市钓鱼, 鲤鱼王
水1/水3: 丰缘橙华市厉害钓竿, 龙虾小兵
水3: 关都枯叶市, 玛瑙水母
虫组: 月见山2F, 派拉斯'''

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['860189236', '210839336']
        if groupNum not in whiteablum:
            await materia.finish()

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+msg
        })
    else:
        await bot.call_api('send_private_msg', 
        **{'user_id':int(user_id), 'message': msg})

    await materia.finish()


#努力值
effort = on_command('努力值', aliases={'effort'}, rule=to_me())


@effort.handle()
async def effort_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    msg = '''HP努力值
[合众]雪花市泥巴鱼x5=10（垃圾多，可带喵喵卡比，会突袭）
[合众] 10号路深草丛败露球菇x5=10
[丰缘]冠军之路入口铁掌力士x5=10（会看穿）

攻击努力值

[合众]10号道路浅草丛爆炸头水牛x5=10
[合众]12号道路深草丛咕咕鸽×5=10
[合众]7号道路浅色深草丛步哨鼠x5=10
[神奥]冠军之路入口钻角犀牛x5=10
[神奥]211号道路豪力x5=10
[关都]15号路尼多力诺/尼多娜x5=10

防御努力值
[合众]冠军之路左边大滑坡进洞铁蚁x5=10
[合众]13号路大嘴鸥x5=10
[关都]冠军之路嘎啦嘎啦/穿山王x5=10

特攻努力值
[合众] 9号道路浅草丛双卵细胞球x5=10
[合众] 14号道路大宇怪x5=10
[合众] 11号道路哥达鸭x5=10

特防努力值
[丰缘]对战开拓区毒刺水母x5=10
[合众]9号道路深草丛哥德小姐x5=10
[合众]小波镇巨翅飞鱼x5=10

速度努力值
[合众]12号道路浅草丛烈焰马×5=10
'''

    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['860189236', '210839336']
        if groupNum not in whiteablum:
            await effort.finish()

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+msg
        })
    else:
        await bot.call_api('send_private_msg', 
        **{'user_id':int(user_id), 'message': msg})

    await effort.finish()



#技能点
skill = on_keyword({'技能点'}, rule=to_me())


@skill.handle()
async def skill_handle(bot: Bot, event: Event, state: T_State):

    session_id = event.get_session_id()
    user_id = str(event.get_user_id())

    skname = str(event.get_message()).strip()
    skname = skname.strip('技能点').replace(' ','')

    hz = ['催眠术','冰冻之风','恶梦','电网','空气利刃','重力','铁壁','欺诈','突袭','大地之力',
        '巨声','意念头锤','挡路','水流尾','珍藏','电磁悬浮','真空波','蛮力','魔法反射']
    gd = ['吵闹','头锤','自爆','原始之力','弹跳','掷泥','渴望','虫咬','龙卷风','雷电拳','火焰拳',
    '冰冻拳','二连劈','伏特攻击','信号光束','垃圾射击','愤怒门牙','直冲钻','种子炸弹','踢倒','铁头']
    fy = ['奇异之风','怨恨','变圆','吐丝','您先请','火之誓约','水之誓约','草之誓约','烦恼种子',
    '胃液','高速星星','黑夜魔影','奇妙空间','帮助','蛮干','逆鳞','魔法空间','流星群']
    sa = ['打鼾','扮演','拍落','出奇一击','绑紧','分担痛楚','戏法','光合作用','击掌奇袭','治愈铃声',
    '热风','神鸟猛击','顺风','冰球']

    msg = '技能名不对,或不需要教学'
    if skname in hz:
        msg = skname + '可以在合众PC小蓝处使用蓝色碎片教学'
    elif skname in gd:
        msg = skname + '可以在关都PC小红处使用红色碎片教学'
    elif skname in fy:
        msg = skname + '可以在丰缘PC小绿处使用绿色碎片教学'
    elif skname in sa:
        msg = skname + '可以在神奥PC小黄处使用黄色碎片教学'


    if 'group' in session_id:
        tmpList = session_id.split('_')
        groupNum = tmpList[1]

        # whiteablum
        whiteablum = ['860189236', '210839336']
        if groupNum not in whiteablum:
            await skill.finish()

        await bot.call_api('send_group_msg', **{
            'group_id':int(groupNum),
            'message': '[CQ:at,qq='+user_id+']'+msg
        })
    else:
        await bot.call_api('send_private_msg', 
        **{'user_id':int(user_id), 'message': msg})

    await skill.finish()
