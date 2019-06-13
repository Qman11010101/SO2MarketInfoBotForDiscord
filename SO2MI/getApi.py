import json
import datetime
import os
import requests

def getApi(apiName, targetApi):
    # 現在時間取得
    now = datetime.datetime.now()
    # ファイルを照査、ある場合はそのjsonデータを取得する
    if os.path.isfile('api-log/{0}/{0}-{1}.json'.format(apiName, now.strftime('%y%m%d%H'))):
        with open('api-log/{0}/{0}-{1}.json'.format(apiName, now.strftime('%y%m%d%H')), 'r', encoding="utf-8_sig") as ijs:
            return json.load(ijs)
    else:
        # フォルダを作成する。ある場合は無視してくれる
        os.makedirs('api-log/{0}/'.format(apiName), exist_ok=True)

        # ない場合は新たにAPI取得する
        newItemRes = requests.get(targetApi)

        # データを保管する
        with open('api-log/{0}/{0}-{1}.json'.format(apiName, now.strftime('%y%m%d%H')), 'w', encoding="utf-8_sig") as ijs:
            json.dump(newItemRes.json(), ijs, ensure_ascii=False)

        # dict化させたデータを返す
        return newItemRes.json()
