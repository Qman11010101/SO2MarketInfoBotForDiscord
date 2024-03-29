import datetime
import glob
import textwrap

from .Alias import alias
from .Exceptions import InvalidURLError, NoTownError
from .getApi import getApi


def itemParser(itemName, argument, townName, beta):
    if beta != "-b":
        item = getApi("item", "https://so2-api.mutoys.com/master/item.json")
        recipe = getApi("recipe", "https://so2-api.mutoys.com/json/master/recipe_item.json")
        sale = getApi("sale", "https://so2-api.mutoys.com/json/sale/all.json")
        req = getApi("request", "https://so2-api.mutoys.com/json/request/all.json")
        town = getApi("town", "https://so2-api.mutoys.com/master/area.json")
    else:
        item = getApi("item_beta", "https://so2-beta.mutoys.com/master/item.json")
        recipe = getApi("recipe_beta", "https://so2-beta.mutoys.com/json/master/recipe_item.json")
        sale = getApi("sale_beta", "https://so2-beta.mutoys.com/json/sale/all.json")
        req = getApi("request_beta", "https://so2-beta.mutoys.com/json/request/all.json")
        town = getApi("town_beta", "https://so2-beta.mutoys.com/master/area.json")

    itemName = alias(itemName)

    # 街名称取得部
    townId = 0
    townstr = ""
    if townName != "none":
        for col in town:
            if town[col]["name"] == townName:
                townId = town[col]["area_id"]
                townstr = f"{townName}における"
                break
        if int(townId) == 0:
            raise NoTownError("such town does not exists")

    # アイテムID取得部
    itemId = 0
    itemScaleName = ""
    for col in item:
        if item[str(col)]["name"] == itemName:
            itemId = col
            itemScaleName = item[str(col)]["scale"]
            break

    if int(itemId) == 0:
        for col in recipe:
            if recipe[str(col)]["name"] == itemName:
                itemId = col
                itemScaleName = recipe[str(col)]["scale"]
                break
        if int(itemId) == 0:
            # 見つからない扱い
            return False

    priceSaleArray = []
    unitSaleArray = []
    shopSaleArray = []
    if int(townId) == 0:
        for saleUnit in sale:
            if int(saleUnit["item_id"]) == int(itemId):
                priceSaleArray.append(saleUnit["price"])
                unitSaleArray.append(saleUnit["unit"])
                shopSaleArray.append(saleUnit["shop_id"])
    else:
        for saleUnit in sale:
            if int(saleUnit["item_id"]) == int(itemId) and int(saleUnit["area_id"]) == int(townId):
                priceSaleArray.append(saleUnit["price"])
                unitSaleArray.append(saleUnit["unit"])
                shopSaleArray.append(saleUnit["shop_id"])
    priceSaleArray.sort() # 金額ソート
    shopSaleAmount = "{:,}".format(len(set(shopSaleArray))) # 販売店舗数(店舗IDの重複を削除)

    saleLen = len(priceSaleArray)
    saleSum = sum(priceSaleArray)

    if saleLen > 0:
        saleCheapest = "{:,}".format(priceSaleArray[0]) # 最安値
        saleMostExpensive = "{:,}".format(priceSaleArray[-1]) # 最高値

        if saleLen < 5: # TOP5平均
            saleMarketPrice = "{:,}".format(saleSum // saleLen)
        else:
            saleMarketPrice = "{:,}".format((priceSaleArray[0] + priceSaleArray[1] + priceSaleArray[2] + priceSaleArray[3] + priceSaleArray[4]) // 5)

        saleAverage = "{:,}".format(saleSum // saleLen) # 平均値

        if saleLen == 1:
            saleMedian = priceSaleArray[0]
        else:
            if saleLen % 2 == 1: # 中央値
                saleMedian = "{:,}".format(priceSaleArray[saleLen // 2 + 1])
            else:
                saleMedian = "{:,}".format(int((priceSaleArray[int(saleLen / 2) - 1] + priceSaleArray[int(saleLen / 2)]) / 2))

        saleUnitSum = "{:,}".format(sum(unitSaleArray)) # 販売数

        saleStr = f"""
        最安値: {saleCheapest}G
        最高値: {saleMostExpensive}G
        最安TOP5平均: {saleMarketPrice}G
        全体平均: {saleAverage}G
        中央値: {saleMedian}G
        市場全体の販売数: {saleUnitSum}{itemScaleName}
        販売店舗数: {shopSaleAmount}店舗
        """
    else:
        saleStr = "\n        現在販売されていません。\n"

    priceReqArray = []
    unitReqArray = []
    shopReqArray = []
    if int(townId) == 0:
        for reqUnit in req:
            if int(reqUnit["item_id"]) == int(itemId):
                priceReqArray.append(reqUnit["price"])
                unitReqArray.append(reqUnit["buy_unit"])
                shopReqArray.append(reqUnit["shop_id"])
    else:
        for reqUnit in req:
            if int(reqUnit["item_id"]) == int(itemId) and int(reqUnit["area_id"]) == int(townId):
                priceReqArray.append(reqUnit["price"])
                unitReqArray.append(reqUnit["buy_unit"])
                shopReqArray.append(reqUnit["shop_id"])

    priceReqArray.sort(reverse=True) # 金額逆順ソート
    shopReqAmount = "{:,}".format(len(set(shopReqArray))) # 注文店舗数(店舗IDの重複を削除)

    reqLen = len(priceReqArray)
    reqSum = sum(priceReqArray)

    if reqLen > 0:
        reqMostExpensive = "{:,}".format(priceReqArray[0]) # 最高値
        reqCheapest = "{:,}".format(priceReqArray[-1]) # 最安値

        if reqLen < 5: # TOP5平均
            reqMarketPrice = "{:,}".format(reqSum // reqLen)
        else:
            reqMarketPrice = "{:,}".format((priceReqArray[0] + priceReqArray[1] + priceReqArray[2] + priceReqArray[3] + priceReqArray[4]) // 5)

        reqAverage = "{:,}".format(reqSum // reqLen) # 平均

        if reqLen == 1:
            reqMedian = priceReqArray[0]
        else:
            if reqLen % 2 == 1: # 中央値
                reqMedian = "{:,}".format(priceReqArray[reqLen // 2 + 1])
            else:
                reqMedian = "{:,}".format(int((priceReqArray[int(reqLen / 2) - 1] + priceReqArray[int(reqLen / 2)]) / 2))

        reqUnitSum = "{:,}".format(sum(unitReqArray)) # 注文数

        reqStr = f"""
        最高値: {reqMostExpensive}G
        最安値: {reqCheapest}G
        最高TOP5平均: {reqMarketPrice}G
        全体平均: {reqAverage}G
        中央値: {reqMedian}G
        市場全体の注文数: {reqUnitSum}{itemScaleName}
        注文店舗数: {shopReqAmount}店舗
        """
    else:
        reqStr = "\n        現在注文はありません。\n"

    # 時刻をsale-*.jsonから推測
    target = glob.glob("api-log/sale-*.json")
    jsonTime = datetime.datetime.strptime(target[0].replace("\\", "/"), "api-log/sale-%y%m%d%H%M.json")

    # 引数による販売品・注文品の分岐
    if argument == "-n":
        summary = textwrap.dedent(f"""
        {jsonTime.strftime("%Y{0}%m{1}%d{2} %H{3}%M{4}").format("年", "月", "日", "時", "分")}現在の{itemName}の{townstr}状況は以下の通りです。

        **販売：**
        {saleStr}

        **注文：**
        {reqStr}

        時間経過により市場がこの通りでない可能性があります。
        """)
    elif argument == "-s":
        summary = textwrap.dedent(f"""
        {jsonTime.strftime("%Y{0}%m{1}%d{2} %H{3}%M{4}").format("年", "月", "日", "時", "分")}現在の{itemName}の{townstr}状況は以下の通りです。

        **販売：**
        {saleStr}

        時間経過により市場がこの通りでない可能性があります。
        """)
    elif argument == "-r":
        summary = textwrap.dedent(f"""
        {jsonTime.strftime("%Y{0}%m{1}%d{2} %H{3}%M{4}").format("年", "月", "日", "時", "分")}現在の{itemName}の{townstr}状況は以下の通りです。

        **注文：**
        {reqStr}

        時間経過により市場がこの通りでない可能性があります。
        """)

    return summary
