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
            print("READ: {0}-{1}.json".format(apiName, now.strftime('%y%m%d%H')))
            return json.load(ijs)
    else:
        # ない場合は新たにAPI取得する
        newItemRes = requests.get(targetApi)

        # データを保管する
        with open('api-log/{0}/{0}-{1}.json'.format(apiName, now.strftime('%y%m%d%H')), 'w', encoding="utf-8_sig") as ijs:
            print("WRITE: {0}-{1}.json".format(apiName, now.strftime('%y%m%d%H')))
            json.dump(newItemRes.json(), ijs, ensure_ascii=False)

        # dict化させたデータを返す
        return newItemRes.json()
