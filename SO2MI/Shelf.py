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
    sumShelf = sumShelfBundle = sumShelfNotBundle = 0
    sumPrice = sumPriceBundle = sumPriceNotBundle = 0
    shelfBundlePercent = shelfNotBundlePersent = 0
    priceBundlePercent = priceNotBundlePercent = 0
    for col in range(len(sale)):
        if sale[col]["area_id"] == townId:
            sumShelf += 1
            sumPrice += int(sale[col]["price"] * sale[col]["unit"])
            if sale[col]["bundle_sale"]:
                sumShelfBundle += 1
                sumPriceBundle += int(sale[col]["price"] * sale[col]["unit"])

    # 非まとめ売り算出
    sumShelfNotBundle = sumShelf - sumShelfBundle
    sumPriceNotBundle = sumPrice - sumPriceBundle

    # まとめ売り百分率
    shelfBundlePercent = float("{:.2f}".format((sumShelfBundle / sumShelf) * 100))
    priceBundlePercent = float("{:.2f}".format((sumPriceBundle / sumPrice) * 100))

    # 非まとめ売り百分率
    shelfNotBundlePersent = 100 - shelfBundlePercent
    priceNotBundlePercent = 100 - priceBundlePercent

    # 時刻をsale-*.jsonから推測
    target = glob.glob("api-log/sale-*.json")
    jsonTime = datetime.datetime.strptime(target[0].replace("\\", "/"), "api-log/sale-%y%m%d%H%M.json")

    retStr = textwrap.dedent(f"""
    {jsonTime.strftime("%Y{0}%m{1}%d{2} %H{3}%M{4}").format("年", "月", "日", "時", "分")}現在の{townName}の合計販売額・販売棚数は以下の通りです。

    合計販売額: {str("{:,}".format(sumPrice))}G
    　まとめ売り: {str("{:,}".format(sumPriceBundle))}G ({priceBundlePercent}%)
    　ばら売り: {str("{:,}".format(sumPriceNotBundle))}G ({priceNotBundlePercent}%)

    販売棚数: {str("{:,}".format(sumShelf))}個
    　まとめ売り: {str("{:,}".format(sumShelfBundle))}個 ({shelfBundlePercent}%)
    　ばら売り: {str("{:,}".format(sumShelfNotBundle))}個 ({shelfNotBundlePersent}%)
    """)

    return retStr
