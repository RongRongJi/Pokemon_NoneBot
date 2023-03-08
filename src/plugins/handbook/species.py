import json
import os



def make_species_dict():
    with open('src/plugins/handbook/data1.json', 'r') as f:
        data = json.load(f)
    return data


def lookup_species_by_name(name, table):
    if name not in table:
        return '您好, 请按照格式 #图鉴 ,后面添加正确的宝可梦名字进行查询哦~'
    
    monster = table[name]

    # image = "[CQ:image,file=/home/sr/project/test/src/plugins/handbook/images/1.png]"
    image = "[CQ:image,file=origin/{}.png]".format(int(table[name]['id']))

    intro = '\n' + table[name]['id'] + ' ' + name + ' ' + table[name]['japan_name'] + ' ' + table[name]['english_name']
    detail = '\n属性: ' + table[name]['attribute'] + '\n特性: ' + table[name]['character']
    detail = detail + '\n身高: ' + table[name]['height'] + '\n体重: ' + table[name]['weight']
    detail = detail + '\n种族值(hp/攻击/防御/特攻/特防/速度): ' + table[name]['species']


    msg = image + intro + detail

    return msg