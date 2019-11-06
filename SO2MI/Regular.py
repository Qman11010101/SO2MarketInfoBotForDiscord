import datetime
import json
import textwrap
import asyncio
import configparser
import calendar
import textwrap
import traceback
import os
import json
import re
import datetime

import discord
import pytz
import requests
from bs4 import BeautifulSoup

from .getApi import getApi

config = configparser.ConfigParser()
config.read("config.ini")

def chkCost():
    try:
        # 読み込みに失敗したらFalseを返す
        with open("itemreg.json", "r", encoding="utf-8_sig") as itf:
            itemreg = json.load(itf)

        itemList = set(itemreg["items"])
        infoList = []

        # 日付文字列生成
        dateYesterday = datetime.date.today() - datetime.timedelta(days=1)

        # アイテム情報取得
        item = getApi("item", "https://so2-api.mutoys.com/master/item.json")
        recipe = getApi("recipe", "https://so2-api.mutoys.com/json/master/recipe_item.json")
        sale = getApi("sale", "https://so2-api.mutoys.com/json/sale/all.json")
        report = getApi("report", f"https://so2-api.mutoys.com/json/report/buy{dateYesterday.strftime('%Y%m%d')}.json")

        # アイテムID取得部
        for col in item:
            if item[str(col)]["name"] in itemList:
                itemId = int(col)
                itemName = item[str(col)]["name"]
                itemScale = item[str(col)]["scale"]
                info = [itemName, itemId, itemScale]
                infoList.append(info)

        for col in recipe:
            if recipe[str(col)]["name"] in itemList:
                itemId = int(col)
                itemName = recipe[str(col)]["name"]
                itemScale = recipe[str(col)]["scale"]
                info = [itemName, itemId, itemScale]
                infoList.append(info)

        priceList = []
        unitList = []
        for itemInfo in infoList:
            priceArray = []
            unitArray = []
            for unit in sale:
                if int(unit["item_id"]) == int(itemInfo[1]):
                    priceArray.append(unit["price"])
                    unitArray.append(unit["unit"])
            priceList.append(priceArray)
            unitList.append(unitArray)

        priceInfo = []
        count = 0
        for listPr in priceList:
            lpr = []
            if len(listPr) == 0:
                lpr = [0, 0, 0]
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
                    med = listPr[0]
                else:
                    if saleLen % 2 == 1:
                        med = "{:,}".format(listPr[saleLen // 2 + 1])
                    else:
                        med = "{:,}".format(int((listPr[int(saleLen / 2) - 1] + listPr[int(saleLen / 2 )]) / 2))

                # 平均値
                aAvg = "{:,}".format(saleSum // saleLen)

                lpr = [t5avg, med, aAvg]

            # レポートから平均取引価格を取得
            try: # 住民取引
                yesAvgSystem = report["system"]["item"][f"{infoList[count][1]}"]["price"]
            except KeyError:
                yesAvgSystem = 0
            
            try: # 業者取引
                yesAvgUser = report["user"]["item"][f"{infoList[count][1]}"]["price"]
            except KeyError:
                yesAvgUser = 0

            try:
                yesAvg = (yesAvgSystem + yesAvgUser) // 2
            except ZeroDivisionError:
                yesAvg = 0

            lpr.append("{:,}".format(yesAvg))
            priceInfo.append(lpr)
            
            count += 1

        text = ""
        for i in range(len(itemList)):
            if priceInfo[i][0] == 0:
                text += f"**{infoList[i][0]}**:\n　現在販売されていません。\n"
            else:
                text += f"**{infoList[i][0]}**:\n　販売数: {sum(unitList[i])}{infoList[i][2]}\n　Top5平均値: {priceInfo[i][0]}G\n　中央値: {priceInfo[i][1]}G\n　全体平均値: {priceInfo[i][2]}G\n"
            if priceInfo[i][3] != "0":
                text += f"　昨日の平均取引価格: {priceInfo[i][3]}G\n　\n"
            else:
                text += "　昨日の平均取引価格: 取引なし\n　\n"

        message = f"**【Daily Market Information】**\n取得された市場情報は以下の通りです:\n　\n{text}時間経過により市場がこの通りでない可能性があります。\n͏​‌" # ゼロ幅スペースで改行維持

        # 情報をJSONとして保存
        rej = {}
        for i in range(len(itemList)):
            name = infoList[i][0]
            rej[name] = {}
            rej[name]["saleunit"] = sum(unitList[i])
            rej[name]["scale"] = infoList[i][2]
            rej[name]["top5avg"] = int(str(priceInfo[i][0]).replace(",", ""))
            rej[name]["median"] = int(str(priceInfo[i][1]).replace(",", ""))
            rej[name]["average"] = int(str(priceInfo[i][2]).replace(",", ""))
            rej[name]["yesterday"] = int(str(priceInfo[i][3]).replace(",", ""))

        with open("api-log/reportdump.json", "w", encoding="utf-8_sig") as rp:
            json.dump(rej, rp, indent=4, ensure_ascii=False)

        return message
    except:
        traceback.print_exc()
        return False

def chkEndOfMonth():
    # 現在時刻取得
    timezone = pytz.timezone(config["misc"]["timezone"])
    now = datetime.datetime.now(timezone)

    # 月末判定
    dayLast = int(calendar.monthrange(now.year, now.month)[1]) # 月の最終日取得
    if now.day != dayLast: # 最終日じゃなければ何もしないようにする
        return False

    message = "**【End-of-Month Information】**\n本日は月末です。優待券・優待回数券・優待お試し券をお持ちの方は使用しておくと翌日にスピードポーション30本を取得できます。\n優待券と優待回数券は作業枠が埋まっていても使用可能ですが、優待お試し券は作業枠が空いている必要がありますのでご注意ください。\n͏​‌"
    return message

def chkEvent():
    try:
        # ページダウンロード
        pseudoUserAgent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        source = requests.get("https://so2-bbs.mutoys.com/agenda", headers=pseudoUserAgent)
        bsobj = BeautifulSoup(source.text, "html.parser")

        # preloadデータのあるdivを拾う
        preloadDiv = bsobj.find_all(id="data-preloaded")

        # 各イベント告知ページへのリンクを取得する
        linksTag = bsobj.find_all("meta", itemprop="url")

        linkurls = []
        for tag in linksTag:
            linkurls.append(tag["content"])

        # 文字列操作
        convQuot = str(preloadDiv[0]).replace(r"\&quot;", '"').replace("&quot;", '"') # 特殊文字をダブルクォーテーションに置換
        rugueux = convQuot[convQuot.find('"topic_list_agenda":'):] # 誤動作防止のため大まかに切り取る
        topicsRug = "{" + rugueux[rugueux.find('"topics":'):rugueux.find("}}")] + "}" # JSONの形で切り取り、足りない括弧をつける
        topicsRug2 = re.sub(r'"fancy_title":.*?",', "", topicsRug)
        topicsJson = re.sub(r'"excerpt":.*?",', "", topicsRug2)
        with open("agenda.json", "w", encoding="utf-8_sig") as agw: # 一旦保存してJSONとして扱えるようにする
            agw.write(topicsJson)
        with open("agenda.json", "r", encoding="utf-8_sig") as agr: # 保存したJSONを読み込む
            agenda = json.load(agr)

        topiclist = agenda["topics"] # 必要な情報が入ったリストを生成する

        iCount = 0
        timezone = pytz.timezone(config["misc"]["timezone"])
        now = datetime.datetime.now(timezone)
        eventHeld = [] # 開催中
        eventCome = [] # 近日
        for col in topiclist:
            # タイトル取得
            title = col["title"]

            # リンク取得
            link = linkurls[iCount]

            # 開始時刻取得
            startTimeutc = datetime.datetime.strptime(col["event"]["start"], "%Y-%m-%dT%H:%M:%S%z")
            startTimejst = startTimeutc.astimezone(timezone)
            startTime = f"{startTimejst.month}/{startTimejst.day} {startTimejst.hour}:{startTimejst:%M}"

            # 終了時刻取得
            if "end" in col["event"]: # 終了時刻明記
                endTimeutc = datetime.datetime.strptime(col["event"]["end"], "%Y-%m-%dT%H:%M:%S%z")
                endTimejst = endTimeutc.astimezone(timezone)
                endTime = f"{endTimejst.month}/{endTimejst.day} {endTimejst.hour}:{endTimejst:%M}"
            else: # 終了時刻がない場合は終日開催と見做す
                endTimejst = startTimejst + datetime.timedelta(hours=24)
                endTime = f"{endTimejst.month}/{endTimejst.day} {endTimejst.hour}:{endTimejst:%M}"

            if now <= endTimejst: # 終了済みイベントは表示しない
                if now >= startTimejst: # 開催中
                    event = f"{endTime}終了"
                    eventInfo = [event, title, link]
                    eventHeld.append(eventInfo)
                elif startTimejst.timestamp() - now.timestamp() < (int(config["misc"]["RegEventDay"]) * 86400):
                    event = f"{startTime} ～ {endTime}"
                    eventInfo = [event, title, link]
                    eventCome.append(eventInfo)

            iCount += 1

        # イベントごとの文章構築
        eventHeldText = []
        eventComeText = []
        if len(eventHeld) != 0:
            for ev in eventHeld:
                evtxt = textwrap.dedent(f"""
                {ev[0]}: {ev[1]}
                Topic: {ev[2]}""")
                eventHeldText.append(evtxt)
        if len(eventCome) != 0:
            for ev in eventCome:
                evtxt = textwrap.dedent(f"""
                {ev[0]}: {ev[1]}
                Topic: {ev[2]}""")
                eventComeText.append(evtxt)

        # 結合
        htx = "\n".join(eventHeldText)
        ctx = "\n".join(eventComeText)

        han = "現在開催中のイベントは以下の通りです:" if len(eventHeldText) != 0 else ""
        can = "近日開催されるイベントは以下の通りです:" if len(eventComeText) != 0 else ""

        if len(eventHeldText) != 0:
            current = f"{han}\n{htx}\n\n"
        else:
            current = ""

        if len(eventComeText) != 0:
            future = f"{can}\n{ctx}"
        else:
            future = ""

        # 文章完成
        if current == "" and future != "":
            res = f"**【Event Information】**\n{future}\n͏​‌"
        elif current != "" and future == "":
            res = f"**【Event Information】**\n{current}\n͏​‌"
        else:
            res = f"**【Event Information】**\n{current}\n{future}\n͏​‌"
        if current == "" and future == "":
            return False
        else:
            return res
    except:
        traceback.print_exc()
        return False
