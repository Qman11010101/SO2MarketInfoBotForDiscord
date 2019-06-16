import datetime

from .Alias import alias
from .getApi import getApi, getApiShort

def ItemParser(itemName):
    now = datetime.datetime.now()
    # API取得部
    item = getApi("item", "https://so2-api.mutoys.com/master/item.json")
    recipe = getApi("recipe", "https://so2-api.mutoys.com/json/master/recipe_item.json")
    sale = getApiShort("sale", "https://so2-api.mutoys.com/json/sale/all.json")
    req = getApiShort("req", "https://so2-api.mutoys.com/json/request/all.json")

    # 略称などの変換
    itemName = alias(itemName)
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
                itemScaleName = item[str(col)]["scale"]
                break
        if int(itemId) == 0:
            # 見つからない扱い
            return False

    priceSaleArray = []
    unitSaleArray = []
    for saleUnit in sale:
        if int(saleUnit["item_id"]) == int(itemId):
            priceSaleArray.append(saleUnit["price"])
            unitSaleArray.append(saleUnit["unit"])
    priceSaleArray.sort() # 金額ソート

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
        市場全体の販売数: {str(saleUnitSum)}{itemScaleName}"""
    else:
        saleStr = "*　現在販売されていません。*"

    priceReqArray = []
    unitReqArray = []
    for reqUnit in req:
        if int(reqUnit["item_id"]) == int(itemId):
            priceReqArray.append(reqUnit["price"])
            unitReqArray.append(reqUnit["buy_unit"])
    priceReqArray.sort(reverse=True)

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
        """
    else:
        reqStr = "*　現在注文はありません。*"

    # まとめ
    parsedTime = now.strftime("%Y年%m月%d日%H時")
    summary = f"""{parsedTime}現在の{itemName}の状況は以下のとおりです。

    **販売：**
    {saleStr}

    **注文：**
    {reqStr}

    *時間経過により市場がこの通りでない可能性があります。*
    """
    return summary
