import json
import datetime
import os
import glob
import configparser

import pytz
import requests

def getApi(apiName, url):
    """保存されているデータが古い、またはデータが存在しない場合、指定されたURL(エンドポイント)にアクセスし、api-logフォルダにJSON形式で保存し、読み込みます。
    データが存在する場合はすでにあるデータを読み込みます。
    いずれの場合もJSONの内容がdict化されて返されます。
    引数`apiName`に`sale`、`sale_beta`、`request`、`request_beta`を指定した場合のファイルの寿命は10分、それ以外は60分(1時間)に指定されています。
    ファイル名は`apiName-yymmddHHMM.json`となります。

    引数:\n
        apiName(str): ファイルとして保存される際の名前の一部です。
        url(str): エンドポイントのURLです。

    返り値:\n
        dict: エンドポイントから取得したデータを辞書形式にしたものです。
    
    例外:\n
        この関数は例外を発生させません。
    
    """

    # タイムゾーン指定のためconfig.iniの読み込み
    config = configparser.ConfigParser()
    config.read("config.ini")

    # 現在時刻取得
    timezone = pytz.timezone(config["misc"]["timezone"])
    now = datetime.datetime.now(timezone)

    # API名に基づいてファイルを選択
    target = glob.glob(f"api-log/{apiName}-*.json")

    # ファイルが存在した場合の分岐
    if len(target) != 0:
        target = target[0].replace("\\", "/") # Windowsではパス文字がバックスラッシュ×2なため変換しておく

        # JSONの名前からデータの取得時間を推測する
        jsonDataTime = datetime.datetime.strptime(target, f"api-log/{apiName}-%y%m%d%H%M.json")

        # 販売品と注文品は10分ごとに、それ以外は60分ごとに注文する
        if apiName in ("sale", "request", "sale_beta", "request_beta"):
            reqTime = 10
        else:
            reqTime = 60

        # 取得可能な時間を生成する
        timeGettableNaive = jsonDataTime + datetime.timedelta(minutes=reqTime)
        timeGettable = timezone.localize(timeGettableNaive)

        # 現在時刻が取得可能な時間を超えているかを判定する
        if timeGettable > now:
            readData = True
            print("最新のデータが存在します")
        else:
            readData = False
            print("データが古くなっています")
    else: # ファイルが存在しなかった場合
        readData = False
        print("データがありません")

    if readData: # APIを叩かず既存ファイルを読み込む
        print("既存のデータを読み込みます: {0}-{1}.json".format(apiName, jsonDataTime.strftime("%y%m%d%H%M")))
        with open("api-log/{0}-{1}.json".format(apiName, jsonDataTime.strftime("%y%m%d%H%M")), "r", encoding="utf-8_sig") as ijs:
            return json.load(ijs)
    else: # 古いデータを削除しAPIを叩いて新たにデータを取得する
        # api-logフォルダを作成する(存在する場合は無視)
        os.makedirs("api-log/", exist_ok=True)

        # 古いデータを削除する
        for delPrev in glob.glob(f"api-log/{apiName}-*.json"):
            try:
                os.remove(delPrev)
                print(f"次のファイルを削除しました: {delPrev}")
            except FileNotFoundError: # もしファイルがなくても無視する
                pass

        # APIを叩く
        print("次のエンドポイントにアクセスしています: " + url)
        newData = requests.get(url)

        # データを保存する
        with open("api-log/{0}-{1}.json".format(apiName, now.strftime("%y%m%d%H%M")), "w", encoding="utf-8_sig") as ijs:
            print("次の名称でデータを保存しました: {0}-{1}.json".format(apiName, now.strftime("%y%m%d%H%M")))
            json.dump(newData.json(), ijs, ensure_ascii=False)

        # dict化させたデータを返す
        return newData.json()
