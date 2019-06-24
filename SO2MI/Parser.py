import datetime
import os
import glob
import textwrap

from .Alias import alias
from .getApi import getApi

def ItemParser(itemName, argument, townName):
    # API取得部
    item = getApi("item", "https://so2-api.mutoys.com/master/item.json")
    recipe = getApi("recipe", "https://so2-api.mutoys.com/json/master/recipe_item.json")
    sale = getApi("sale", "https://so2-api.mutoys.com/json/sale/all.json")
    req = getApi("request", "https://so2-api.mutoys.com/json/request/all.json")
    town = getApi("town", "https://so2-api.mutoys.com/master/area.json")

    # 略称などの変換
    itemName = alias(itemName)

    # 街名称取得部
    townId = 0
    townstr = ""
    if townName != "--none":
        for col in town:
            if town[col]["name"] == townName:
                townId = town[col]["area_id"]
                townstr = "{}における".format(townName)
                break
        if int(townId) == 0:
            return "nte"

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
    shopSaleAmount = len(set(shopSaleArray)) # 販売店舗数(店舗IDの重複を削除)

    if len(priceSaleArray) > 0:
        saleCheapest = priceSaleArray[0] # 最安値
        saleMostExpensive = priceSaleArray[-1] # 高額値

        if len(priceSaleArray) < 5:
            saleMarketPrice = sum(priceSaleArray) // len(priceSaleArray)
        else:
            saleMarketPrice = (priceSaleArray[0] + priceSaleArray[1] + priceSaleArray[2] + priceSaleArray[3] + priceSaleArray[4]) // 5
        
        saleAverage = sum(priceSaleArray) // len(priceSaleArray)
        saleUnitSum = sum(unitSaleArray)

        saleStr = f"""
        最安値: {str(saleCheapest)}G
        最高値: {str(saleMostExpensive)}G
        最安TOP5平均: {str(saleMarketPrice)}G
        全体平均: {str(saleAverage)}G
        市場全体の販売数: {str(saleUnitSum)}{itemScaleName}
        販売店舗数: {shopSaleAmount}店舗
        """
    else:
        saleStr = "\n現在販売されていません。\n"

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
    shopReqAmount = len(set(shopReqArray)) # 注文店舗数(店舗IDの重複を削除)

    if len(priceReqArray) > 0:
        reqMostExpensive = priceReqArray[0] # 最高値
        reqCheapest = priceReqArray[-1] # 最安値

        if len(priceReqArray) < 5:
            reqMarketPrice = sum(priceReqArray) // len(priceReqArray)
        else:
            reqMarketPrice = (priceReqArray[0] + priceReqArray[1] + priceReqArray[2] + priceReqArray[3] + priceReqArray[4]) // 5
        
        reqAverage = sum(priceReqArray) // len(priceReqArray)
        reqUnitSum = sum(unitReqArray)

        reqStr = f"""
        最高値: {str(reqMostExpensive)}G
        最安値: {str(reqCheapest)}G
        最高TOP5平均: {str(reqMarketPrice)}G
        全体平均: {str(reqAverage)}G
        市場全体の注文数: {str(reqUnitSum)}{itemScaleName}
        注文店舗数: {shopReqAmount}店舗
        """
    else:
        reqStr = "\n現在注文はありません。\n"

    # まとめ
    # 時刻をsale-*.jsonから推測
    target = glob.glob("api-log/sale-*.json")
    jsonTime = datetime.datetime.strptime(target[0].replace("\\", "/"), "api-log/sale-%y%m%d%H%M.json")

    # 引数による販売品・注文品の分岐
    if argument == "--normal" or argument == "-t":
        summary = textwrap.dedent(f"""\
        {jsonTime.strftime("%Y{0}%m{1}%d{2} %H{3}%M{4}").format("年", "月", "日", "時", "分")}現在の{itemName}の{townstr}状況は以下の通りです。

        **販売：**
            {saleStr}

        **注文：**
            {reqStr}

        時間経過により市場がこの通りでない可能性があります。
        """)
    elif argument == "-s":
        summary = textwrap.dedent(f"""\
        {jsonTime.strftime("%Y{0}%m{1}%d{2} %H{3}%M{4}").format("年", "月", "日", "時", "分")}現在の{itemName}の{townstr}状況は以下の通りです。

        **販売：**
        {saleStr}

        時間経過により市場がこの通りでない可能性があります。
        """)
    elif argument == "-r":
        summary = textwrap.dedent(f"""\
        {jsonTime.strftime("%Y{0}%m{1}%d{2} %H{3}%M{4}").format("年", "月", "日", "時", "分")}現在の{itemName}の{townstr}状況は以下の通りです。

        **注文：**
        {reqStr}

        時間経過により市場がこの通りでない可能性があります。
        """)
        
    return summary
