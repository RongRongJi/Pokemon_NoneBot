import json
import os.path
import pprint
import re
import time

import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import aiohttp

from plottable import ColDef, Table
from plottable import ColumnDefinition, Table
from plottable.cmap import normed_cmap
from plottable.formatters import decimal_to_percent
from plottable.plots import circled_image # image
from plottable.plots import image
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import LinearSegmentedColormap
import datetime

from snapshot_selenium import snapshot as driver
from pyecharts.render import make_snapshot
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.globals import ThemeType

# 图表
# https://pokemmoprices.com/api/v2/items/graph/min/1310

# item描述
# https://pokemmoprices.com/api/v2/items/1310

# 物品最低价
# https://proxy.pokemmoprices.com/items/entries/779/1310

# --------------------------

# 最后快照
# https://proxy.pokemmoprices.com/items/snapshots/last

# 所有物品最低价
# https://proxy.pokemmoprices.com/items/entries/lowest/779

# 对比
# https://proxy.pokemmoprices.com/items/snapshots/compare/779/752

async def get_data(url):
    async with aiohttp.ClientSession() as session:
        c = await session.get(url=url)
        ret = await c.json()
    return ret


# 获取当前快照
async def current_snapshot():
    url = f'https://proxy.pokemmoprices.com/items/snapshots/last'
    resp_json = await get_data(url)
    snapshot = resp_json['data']['id']
    createdAtEpoch = resp_json['data']['createdAtEpoch']
    timelocal = time.localtime(createdAtEpoch)
    createdAt = time.strftime("%Y-%m-%d %H:%M", timelocal)
    return snapshot, createdAt


# item
async def graph_item(title, itemid, save_path, tmp_path):
    url = f'https://pokemmoprices.com/api/v2/items/graph/min/{itemid}'
    resp_json = await get_data(url)
    prices = resp_json['data']
    all_datas = []
    _min, _max = 99999999999, 0
    now = time.time()
    for price in prices:
        if price['x'] < now - 7776000:
            continue
        timelocal = time.localtime(price['x'])
        curdate = time.strftime("%Y-%m-%d", timelocal)
        all_datas.append([curdate, price['y']])
        if price['y'] > _max:
            _max = price['y']
        if price['y'] < _min:
            _min = price['y']

    line = (
        Line()
        .add_xaxis(xaxis_data=[item[0] for item in all_datas])
        .add_yaxis(
            series_name="price",
            y_axis=[item[1] for item in all_datas],
            yaxis_index=0,
            is_smooth=False,
            is_symbol_show=False,
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            visualmap_opts=opts.VisualMapOpts(type_="color", 
                pos_top="10",
                pos_right="10",
                min_=_min,
                max_=_max,
                is_show=False
                ),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value", 
                min_=_min,
                max_=_max,
                axistick_opts=opts.AxisTickOpts(is_inside=False)),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    make_snapshot(driver, line.render(tmp_path), save_path)

# low price
async def price_item(name, itemid, save_path):
    snapshot, createdAt = await current_snapshot()
    url = f'https://proxy.pokemmoprices.com/items/entries/{snapshot}/{itemid}'
    resp_json = await get_data(url)
    items = resp_json['data']
    price_arr = []
    for item in items:
        price_arr.append({
            'name': name,
            'price': item['price'],
            'num': item['quantity'],
            'startedAt': time.strftime("%Y-%m-%d %H:%M", time.localtime(item['startedAt'])),
            'endedAt': time.strftime("%Y-%m-%d %H:%M", time.localtime(item['endedAt'])) 
        })
    price_arr = sorted(price_arr, key=lambda x:x['price'])[:10]

    df = pd.DataFrame(price_arr, columns=['name','price','num','startedAt','endedAt'])
    print(df)
    table_col_defs = [
        ColDef("name", width=0.5, title="", textprops={'ha':'left', 'weight':'bold'}),
        ColDef("price", width=0.3, title="价格",  formatter=format_coma),
        ColDef("num", width=0.3, title="当前个数"),
        ColDef("startedAt", width=0.3, title="上架时间"),
        ColDef("endedAt", width=0.3, title="预计下架时间"),
    ]

    fig, ax = plt.subplots(figsize=(12, len(price_arr)/2))
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams["savefig.bbox"] = "tight"
    plt.rcParams['axes.unicode_minus']=False

    table = Table(
        df,
        column_definitions=table_col_defs,
        row_dividers=True,
        col_label_divider=False,
        footer_divider=True,
        ax=ax,
        index_col="name",
        columns=['price','num','startedAt','endedAt'],
        row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))},
        col_label_divider_kw={"linewidth": 1, "linestyle": "-"},
        column_border_kw={"linewidth": 1, "linestyle": "-"},
    )

    fig.savefig(save_path, facecolor=fig.get_facecolor())

    

# 获取当前物品与n天之前的对比
async def compare_all_items(early, img_title, save_path, up_rate, up_total):
    snapshot, createdAt = await current_snapshot()
    time.sleep(5)
    url = 'https://proxy.pokemmoprices.com/items/snapshots/compare/{}/{}'.format(snapshot, snapshot-early)
    resp_json = await get_data(url)
    items = resp_json['data']['items']
    increase, decrease = [], []
    for item in items:
        if item['prices']['lowestChangePercentage'] == 0:
            continue
        if item['prices']['lowestChangePercentage'] > up_rate and item['prices']['lowestChange'] > up_total:
            increase.append(item)
        elif item['prices']['lowestChangePercentage'] < -up_rate and item['prices']['lowestChange'] < -up_total:
            decrease.append(item)
    increase = sorted(increase, key=lambda x: x['prices']['lowestChangePercentage'], reverse=True)
    decrease = sorted(decrease, key=lambda x: x['prices']['lowestChangePercentage'], reverse=True)

    increase_handle = []
    for item in increase:
        increase_handle.append({
            'name': item['item']['cn_name'],
            'currentListingCount': item['currentListingCount'],
            'listingsChange': item['listingsChange'],
            'lowestChange': item['prices']['lowestChange'],
            'lowestChangePercentage': item['prices']['lowestChangePercentage'],
            'total':int(float(item['prices']['lowestChange']) / (float(item['prices']['lowestChangePercentage'])*0.01)) + item['prices']['lowestChange']
        })
    for item in decrease:
        increase_handle.append({
            'name': item['item']['cn_name'],
            'currentListingCount': item['currentListingCount'],
            'listingsChange': item['listingsChange'],
            'lowestChange': item['prices']['lowestChange'],
            'lowestChangePercentage': item['prices']['lowestChangePercentage'],
            'total':int(float(item['prices']['lowestChange']) / (float(item['prices']['lowestChangePercentage'])*0.01)) + item['prices']['lowestChange']
        })
    # print(increase_handle)

    df = pd.DataFrame(increase_handle, columns=['name','currentListingCount','listingsChange','lowestChange','lowestChangePercentage','total'])

    # print(df)

    group = '{}({})'.format(img_title, createdAt)
    table_col_defs = [
        ColDef("name", width=0.5, title="", textprops={'ha':'left', 'weight':'bold'}),
        ColDef("currentListingCount", width=0.3, title="交易行总数", textprops={'ha':'center'}, group=group),
        ColDef("listingsChange", width=0.3, title="库存变化",textprops={"ha": "center"},
            cmap=normed_cmap(df["listingsChange"], cmap=matplotlib.cm.PiYG, num_stds=2.5),group=group),
        ColDef("lowestChange", width=0.3, formatter=format_plus, title="最低价变化", 
            cmap=normed_cmap(df["lowestChange"], cmap=matplotlib.cm.PiYG,num_stds=0.8),group=group),
        ColDef("lowestChangePercentage", width=0.3, formatter=format_percent, title="最低价变化率",
            cmap=normed_cmap(df["lowestChangePercentage"], cmap=matplotlib.cm.PRGn,num_stds=2),group=group),
        ColDef("total", width=0.3, title="当前价格", formatter=format_coma,
            cmap=normed_cmap(df["total"], cmap=matplotlib.cm.coolwarm,num_stds=0.8),group=group)
    ]

    fig, ax = plt.subplots(figsize=(15, len(increase_handle)/2))
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams["savefig.bbox"] = "tight"
    plt.rcParams['axes.unicode_minus']=False

    table = Table(
        df,
        column_definitions=table_col_defs,
        row_dividers=True,
        col_label_divider=False,
        footer_divider=True,
        ax=ax,
        index_col="name",
        columns=['currentListingCount','listingsChange','lowestChange','lowestChangePercentage','total'],
        row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))},
        col_label_divider_kw={"linewidth": 1, "linestyle": "-"},
        column_border_kw={"linewidth": 1, "linestyle": "-"},
    ).autoset_fontcolors(colnames=["listingsChange","lowestChange", "lowestChangePercentage","total"])

    fig.savefig(save_path, facecolor=fig.get_facecolor())



def format_percent(val):
    return str(val)+"%"

def format_plus(val):
    if val > 0:
        return "+"+format(val,",")
    else:
        return format(val, ",")

def format_coma(val):
    return format(val,",")

