import textwrap
import datetime
import glob
from collections import Counter

from .Alias import alias
from .getApi import getApi
from .Exceptions import NoTownError

def getShelves(townName):
    # API取得部
    town = getApi("town", "https://so2-api.mutoys.com/master/area.json")
    sale = getApi("sale", "https://so2-api.mutoys.com/json/sale/all.json")
    item = getApi("item", "https://so2-api.mutoys.com/master/item.json")
    recipe = getApi("recipe", "https://so2-api.mutoys.com/json/master/recipe_item.json")

    # 街ID取得部
    if townName != "--all":
        townId = 0
        for col in town:
            if town[col]["name"] == townName:
                townId = int(town[col]["area_id"])
                break
        if int(townId) == 0:
            raise NoTownError("such town does not exists")

    # 変数初期化部
    sumShelf = sumShelfBundle = sumShelfNotBundle = 0
    sumPrice = sumPriceBundle = sumPriceNotBundle = 0
    shelfBundlePercent = shelfNotBundlePersent = 0
    priceBundlePercent = priceNotBundlePercent = 0
    itemsIDList = []
    # itemsPriceList = []

    # 棚数・販売額・アイテムID取得部
    if townName != "--all":
        for col in range(len(sale)):
            if sale[col]["area_id"] == townId:
                sumShelf += 1
                sumPrice += int(sale[col]["price"] * sale[col]["unit"])
                itemUnitList = [sale[col]["item_id"]] * sale[col]["unit"]
                itemsIDList.extend(itemUnitList)
                # itemsPriceList.append(sale[col]["price"])
                if sale[col]["bundle_sale"]:
                    sumShelfBundle += 1
                    sumPriceBundle += int(sale[col]["price"] * sale[col]["unit"])
    else:
        for col in range(len(sale)):
            sumShelf += 1
            sumPrice += int(sale[col]["price"] * sale[col]["unit"])
            itemUnitList = [sale[col]["item_id"]] * sale[col]["unit"]
            itemsIDList.extend(itemUnitList)
            # itemsPriceList.append(sale[col]["price"])
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

    # アイテムID最頻値取得
    itemIdTop = Counter(itemsIDList).most_common(3)

    # アイテムIDを名称に変換
    itemAmountInfo = []
    for ids in itemIdTop:
        itemNames = []
        for col in item:
            if item[str(col)]["item_id"] == int(ids[0]):
                itemNames = [item[col]["name"], ids[1], item[col]["scale"]]
                break

        if itemNames == []:
            for col in recipe:
                if recipe[str(col)]["item_id"] == int(ids[0]):
                    itemNames = [recipe[str(col)]["name"], ids[1], recipe[col]["scale"]]
                    break

        itemAmountInfo.append(itemNames)

    if townName == "--all":
        townName = "全体"
        laststr = f"コマンドについてのヘルプを閲覧するには、コマンドに続けて`help`と入力してください。"
    else:
        laststr = ""

    # 同率n位を出せるようにする
    topthree = [1]
    first = topthree[0]
    if itemAmountInfo[0][1] == itemAmountInfo[1][1]:
        topthree.append(first)
    else:
        topthree.append(first + 1)
    second = topthree[1]
    if itemAmountInfo[1][1] == itemAmountInfo[2][1]:
        topthree.append(second)
    else:
        topthree.append(second + 1)


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

    販売数トップ3:
    　{topthree[0]}位: {itemAmountInfo[0][0]} ({str("{:,}".format(itemAmountInfo[0][1]))}{itemAmountInfo[0][2]})
    　{topthree[1]}位: {itemAmountInfo[1][0]} ({str("{:,}".format(itemAmountInfo[1][1]))}{itemAmountInfo[1][2]})
    　{topthree[2]}位: {itemAmountInfo[2][0]} ({str("{:,}".format(itemAmountInfo[2][1]))}{itemAmountInfo[2][2]})

    {laststr}
    """)

    return retStr
