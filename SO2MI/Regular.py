import datetime
import json
import textwrap
import asyncio
import configparser
import calendar
import textwrap

import discord
import pytz

from .getApi import getApi

def chkCost():
    # タイムゾーン指定のためconfig.iniの読み込み
    config = configparser.ConfigParser()
    config.read("config.ini")

    # 現在時刻取得
    timezone = pytz.timezone(config["misc"]["timezone"])
    now = datetime.datetime.now(timezone)

    # 時刻判定
    startHour = int(config["misc"]["RegExcHour"])
    startMin = int(config["misc"]["RegExcMinute"])
    endMin = startMin + int(config["misc"]["RegExcCheckTime"])
    if now.hour == startHour and startMin <= now.minute <= endMin:
        try:
            # 読み込みに失敗したらFalseを返す
            with open("itemreg.json", "r", encoding="utf-8_sig") as itf:
                itemreg = json.load(itf)

            itemList = set(itemreg["items"])
            infoList = []

            # アイテム情報取得
            item = getApi("item", "https://so2-api.mutoys.com/master/item.json")
            recipe = getApi("recipe", "https://so2-api.mutoys.com/json/master/recipe_item.json")
            sale = getApi("sale", "https://so2-api.mutoys.com/json/sale/all.json")

            # アイテムID取得部
            print("アイテムID取得中")
            for col in item:
                if item[str(col)]["name"] in itemList:
                    itemId = int(col)
                    itemName = item[str(col)]["name"]
                    info = [itemName, itemId]
                    infoList.append(info)
    
            for col in recipe:
                if recipe[str(col)]["name"] in itemList:
                    itemId = int(col)
                    itemName = recipe[str(col)]["name"]
                    info = [itemName, itemId]
                    infoList.append(info)
            
            print("アイテム価格取得中")
            priceList = []
            for itemInfo in infoList:
                priceArray = []
                for unit in sale:
                    if int(unit["item_id"]) == int(itemInfo[1]):
                        priceArray.append(unit["price"])
                priceList.append(priceArray)
            
            print("情報整理中")
            priceInfo = []
            for listPr in priceList:
                lpr = []
                if len(listPr) == 0:
                    lpr = ["0", "0", "0"]
                else:
                    listPr.sort()
                    saleLen = len(listPr)
                    saleSum = sum(listPr)

                    # TOP5平均
                    if saleLen < 5: 
                        t5avg = "{:,}".format(saleSum // saleLen)
                    else:
                        t5avg = "{:,}".format((listPr[0] + listPr[1] + listPr[2] + listPr[3] + listPr[4]) // 5)

                    # 中央値
                    if saleLen == 1:
                        med = saleLen
                    else:
                        if saleLen % 2 == 1:
                            med = "{:,}".format(listPr[saleLen // 2 + 1])
                        else:
                            med = "{:,}".format(int((listPr[int(saleLen / 2)] + listPr[int(saleLen / 2 + 1)]) / 2))

                    # 平均値
                    aAvg = "{:,}".format(saleSum // saleLen)

                    lpr = [t5avg, med, aAvg]
                priceInfo.append(lpr)

            text = ""
            for i in range(len(itemList)):
                text += f"{infoList[i][0]}: {priceInfo[i][0]}G/{priceInfo[i][1]}G/{priceInfo[i][2]}G\n"

            message = f"""
【Daily Information】
取得された市場情報は以下の通りです。
価格の並びは左から順にTOP5値/中央値/平均値です。
            　
{text}"""

            return message
        except:
            return False
    else:
        return False

def chkEndOfMonth():
    # タイムゾーン指定のためconfig.iniの読み込み
    config = configparser.ConfigParser()
    config.read("config.ini")

    # 現在時刻取得
    timezone = pytz.timezone(config["misc"]["timezone"])
    now = datetime.datetime.now(timezone)
    """
    # 月末判定
    dayLast = int(calendar.monthrange(now.year, now.month)[1]) # 月の最終日取得
    if now.day != dayLast: # 最終日じゃなければ何もしないようにする
        return False
    """
    # 時刻判定
    startHour = int(config["misc"]["RegExcHour"])
    startMin = int(config["misc"]["RegExcMinute"])
    endMin = startMin + int(config["misc"]["RegExcCheckTime"])
    if now.hour == startHour and startMin <= now.minute <= endMin:
        message = textwrap.dedent("""
        【End-of-Month Information】
        本日は月末です。優待券・優待回数券・優待お試し券をお持ちの方は使用しておくと翌日にスピードポーション30本を取得できます。
        優待券と優待回数券は作業枠が埋まっていても使用可能ですが、優待お試し券は作業枠が空いている必要がありますのでご注意ください。
        """)
        return message
    else:
        return False
