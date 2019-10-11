import textwrap
import datetime
import glob

from .Alias import alias
from .getApi import getApi
from .Exceptions import NoTownError

def getShelves(townName):
    # API取得部
    town = getApi("town", "https://so2-api.mutoys.com/master/area.json")
    sale = getApi("sale", "https://so2-api.mutoys.com/json/sale/all.json")
    # TODO: いずれbetaに対応する

    # 街ID取得部
    townId = 0
    for col in town:
        if town[col]["name"] == townName:
            townId = int(town[col]["area_id"])
            break
    if int(townId) == 0:
        raise NoTownError("such town does not exists")

    # 棚数・販売額取得部
    shelf = 0
    sumPrice = 0
    for col in sale:
        if int(sale[col]["area_id"]) == townId:
            shelf += 1
            sumPrice += int(sale[col]["price"] * sale[col]["unit"])

    # 時刻をsale-*.jsonから推測
    target = glob.glob("api-log/sale-*.json")
    jsonTime = datetime.datetime.strptime(target[0].replace("\\", "/"), "api-log/sale-%y%m%d%H%M.json")

    retStr = textwrap.dedent(f"""
    {jsonTime.strftime("%Y{0}%m{1}%d{2} %H{3}%M{4}").format("年", "月", "日", "時", "分")}現在の{townName}の合計販売額・販売棚数は以下の通りです。

    合計販売額: {str("{:,}".format(sumPrice))}G
    販売棚数: {str("{:,}".format(shelf))}個
    """)

    return retStr
