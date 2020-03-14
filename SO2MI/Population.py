import json
import textwrap

from .getApi import getApi
from .Exceptions import NoTownError

def getPopulation(townName):
    population = getApi("population", "https://so2-api.mutoys.com/json/people/all.json")
    town = getApi("town", "https://so2-api.mutoys.com/master/area.json")

    # 名称/ID変換
    townId = 0
    for col in town:
        if town[col]["name"] == townName:
            townId = int(town[col]["area_id"])
            break
    if int(townId) == 0:
        raise NoTownError("such town does not exists")

    # 情報取得
    poplist = []
    for col in population:
        if col["area_id"] == townId:
            poplist.append(col["unit"])
            for name in range(1,13):
                poplist.append(col["persons"][str(name)]["unit"])
            break
    
    # 文字列生成
    al = poplist[0]

    msg = textwrap.dedent(f"""
    現時点での{townName}の人口情報は以下の通りです:
    
    全人口: {"{:,}".format(poplist[0])}人
    　おぼっちゃん: {"{:,}".format(poplist[1])}人 ({"{:.2f}".format((poplist[1] / al) * 100)}%)
    　おじょうちゃん: {"{:,}".format(poplist[2])}人 ({"{:.2f}".format((poplist[2] / al) * 100)}%)
    　しょうねん: {"{:,}".format(poplist[3])}人 ({"{:.2f}".format((poplist[3] / al) * 100)}%)
    　しょうじょ: {"{:,}".format(poplist[4])}人 ({"{:.2f}".format((poplist[4] / al) * 100)}%)
    　おにいさん: {"{:,}".format(poplist[5])}人 ({"{:.2f}".format((poplist[5] / al) * 100)}%)
    　おねえさん: {"{:,}".format(poplist[6])}人 ({"{:.2f}".format((poplist[6] / al) * 100)}%)
    　おじさん: {"{:,}".format(poplist[7])}人 ({"{:.2f}".format((poplist[7] / al) * 100)}%)
    　おばさん: {"{:,}".format(poplist[8])}人 ({"{:.2f}".format((poplist[8] / al) * 100)}%)
    　おじいさん: {"{:,}".format(poplist[9])}人 ({"{:.2f}".format((poplist[9] / al) * 100)}%)
    　おばあさん: {"{:,}".format(poplist[10])}人 ({"{:.2f}".format((poplist[10] / al) * 100)}%)
    　買い付け人: {"{:,}".format(poplist[11])}人 ({"{:.2f}".format((poplist[11] / al) * 100)}%)
    　旅人: {"{:,}".format(poplist[12])}人 ({"{:.2f}".format((poplist[12] / al) * 100)}%)
    """)

    return msg
