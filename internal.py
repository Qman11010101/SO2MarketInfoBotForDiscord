import json

from SO2MI import alias

#jsonファイルの読み込み
with open("data/sale.json", "r", encoding="utf-8_sig") as s: #販売品
    sale = json.load(s)
with open("data/req.json", "r", encoding="utf-8_sig") as r: #注文品
    req = json.load(r)
with open("data/item.json", "r", encoding="utf-8_sig") as i: #アイテム定義
    item = json.load(i)
with open("data/rec.json", "r", encoding="utf-8_sig") as c:
    rec = json.load(c)

#商品名取得部
itemName = "" #itemNameにアイテム名を代入

#略称などの変換
itemName = alias(itemName)

#アイテムID取得部
itemId = 0
for colomn in item:
    itemName_json = item[colomn]["name"]
    if itemName_json == itemName:
        itemId = item[colomn]["item_id"]

#もしアイテム名がなかったら終了
if itemId == 0:
    print(itemName + "は存在しないようです。")
    sys.exit()

#販売品分析部
#アイテムIDが合致したら配列priceSaleAllayとunitSaleAllayにappend
priceSaleAllay = []
unitSaleArray = []
store = 0
for storeCount in sale:
    price = sale[store]["price"] #販売価格
    unit = sale[store]["unit"] #販売個数
    if sale[store]["item_id"] == itemId:
        priceSaleAllay.append(price)
        unitSaleArray.append(unit)
    store += 1
priceSaleAllay.sort() #金額はソート

#注文品分析部
#アイテムIDが合致したら配列priceReqAllayとunitReqArrayにappend
priceReqAllay = []
unitReqArray = []
store = 0
for storeCount in req:
    price = req[store]["price"] #注文価格
    unit = req[store]["buy_unit"] #注文個数
    if req[store]["item_id"] == itemId:
        priceReqAllay.append(price)
        unitReqArray.append(unit)
    store += 1
priceReqAllay.sort(reverse = True) #金額は逆ソート

#販売品の有無で分岐
if priceSaleAllay != []:
    #販売品計算部
    saleCheapest = priceSaleAllay[0] #最安値
    saleMostExpensive = priceSaleAllay[-1] #最高値

    #一箇所だけ処分的に安く出している店への対策として最安TOP5の平均値を出す。5店舗以上なければ全部足して割る
    if len(priceSaleAllay) < 5:
        saleMarketPrice = sum(priceSaleAllay) // len(priceSaleAllay)
    else:
        saleMarketPrice = (priceSaleAllay[0] + priceSaleAllay[1] + priceSaleAllay[2] + priceSaleAllay[3] + priceSaleAllay[4]) // 5

    saleAverage = sum(priceSaleAllay) // len(priceSaleAllay) #全体平均
    saleUnitSum = sum(unitSaleArray) #市場全体の個数

    #販売品表示部
    saleLine = "最安値: " + str(saleCheapest) + "G\n最高値: " + str(saleMostExpensive) + "G\n最安TOP5平均: " + str(saleMarketPrice) + "G\n全体平均: " + str(saleAverage) + "G\n市場全体の個数: " + str(saleUnitSum) + "個"
else:
    saleLine = "現在この商品は市場で販売されていません。"

#注文品の有無で分岐
if priceReqAllay != []:

    #注文品計算部　リストは降順でソートされていることに注意
    reqMostExpensive = priceReqAllay[0] #最高値
    reqCheapest = priceReqAllay[-1] #最安値

    #最高TOP5の平均値を出す。5店舗以上なければ全部足して割る
    if len(priceReqAllay) < 5:
        reqMarketPrice = sum(priceReqAllay) // len(priceReqAllay)
    else:
        reqMarketPrice = (priceReqAllay[0] + priceReqAllay[1] + priceReqAllay[2] + priceReqAllay[3] + priceReqAllay[4]) // 5
    
    reqAverage = sum(priceReqAllay) // len(priceReqAllay) #全体平均
    reqUnitSum = sum(unitReqArray) #市場全体の注文数

    #販売品表示部
    reqLine = "最高値: " + str(reqMostExpensive) + "G\n最安値: " + str(reqCheapest) + "G\n最高TOP5平均: " + str(reqMarketPrice) + "G\n全体平均: " + str(reqAverage) + "G\n市場全体の注文数: " + str(reqUnitSum) + "個"
else:
    reqLine = "現在この商品は市場で注文されていません。"

#表示部1行を変数に入れたもの
displayLine = "直近の" + itemName + "の状況は以下のとおりです。\n\n販売\n\n" + saleLine + "\n\n注文\n\n" + reqLine + "\n\n時間経過により市場がこの通りでない可能性があります。"
