import json
import datetime
import os
import requests
import glob
import pytz
import configparser

def getApi(apiName, url):
    # タイムゾーン指定のためconfig.iniの読み込み
    config = configparser.ConfigParser()
    config.read("config.ini")

    # 現在時刻取得
    timezone = pytz.timezone(config["misc"]["timezone"])
    now = datetime.datetime.now(timezone)

    # API名に基づいてファイルを選択
    target = glob.glob("api-log/{0}-*.json".format(apiName))

    # ファイルが存在した場合の分岐
    if len(target) != 0:
        target = target[0].replace("\\", "/") # Windowsではパス文字がバックスラッシュ×2なため変換しておく

        # JSONの名前からデータの取得時間を推測する
        jsonDataTime = datetime.datetime.strptime(target, "api-log/{0}-%y%m%d%H%M.json".format(apiName))

        # 販売品と注文品は10分ごとに、それ以外は60分ごとに注文する
        if apiName == "sale" or apiName == "request":
            reqTime = 10
        else:
            reqTime = 60

        # 取得可能な時間を生成する
        timeGettable = jsonDataTime + datetime.timedelta(minutes=reqTime)

        # 現在時刻が取得可能な時間を超えているかを判定する
        readData = False if timeGettable > now else True
    else: # ファイルが存在しなかった場合
        readData = False

    if readData: # APIを叩かず既存ファイルを読み込む
        print("Latest Data Founded: {0}-{1}.json".format(apiName, jsonDataTime.strftime("%y%m%d%H%M")))
        with open("api-log/{0}-{1}.json".format(apiName, jsonDataTime.strftime("%y%m%d%H%M")), "r", encoding="utf-8_sig") as ijs:
            return json.load(ijs)
    else: # 古いデータを削除しAPIを叩いて新たにデータを取得する
        # api-logフォルダを作成する(存在する場合は無視)
        os.makedirs("api-log/", exist_ok=True)

        # 古いデータを削除する
        for delPrev in glob.glob("api-log/{0}-*.json".format(apiName)):
            try:
                os.remove(delPrev)
                print("Deleted: {0}".format(delPrev))
            except FileNotFoundError: # もしファイルがなくても無視する
                pass

        # APIを叩く
        print("Access: " + url)
        newData = requests.get(url)

        # データを保存する
        with open("api-log/{0}-{1}.json".format(apiName, now.strftime("%y%m%d%H%M")), "w", encoding="utf-8_sig") as ijs:
            print("Save {0}-{1}.json".format(apiName, now.strftime("%y%m%d%H%M")))
            json.dump(newData.json(), ijs, ensure_ascii=False)

        # dict化させたデータを返す
        return newData.json()
"""


        # dict化させたデータを返す
        return newItemRes.json()
"""