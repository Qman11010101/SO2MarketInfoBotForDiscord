import json
import datetime
import os
import requests
import glob

# 現在時間取得
now = datetime.datetime.now()

def getApi(apiName, targetApi):
    # ファイルを照査、ある場合はそのjsonデータを取得する
    if os.path.isfile('api-log/{0}-{1}.json'.format(apiName, now.strftime('%y%m%d%H'))):
        with open('api-log/{0}-{1}.json'.format(apiName, now.strftime('%y%m%d%H')), 'r', encoding="utf-8_sig") as ijs:
            return json.load(ijs)
    else:
        # フォルダを作成する。ある場合は無視してくれる
        os.makedirs('api-log/', exist_ok=True)

        # 前の時間に取得したAPIデータを削除(ある場合は)
        for deletePrevious in glob.glob('api-log/{0}-*.json'.format(apiName)):
            try:
                os.remove(deletePrevious)
                print('Purge: {0}'.format(deletePrevious))
            except FileNotFoundError: # もしファイルがなくてもエラーでスクリプトを止めないようにする（無視）
                pass

        # ない場合は新たにAPI取得する
        print("Getting datas from " + targetApi)
        newItemRes = requests.get(targetApi)

        # データを保管する
        with open('api-log/{0}-{1}.json'.format(apiName, now.strftime('%y%m%d%H')), 'w', encoding="utf-8_sig") as ijs:
            print('Insert: {0}-{1}'.format(apiName, now.strftime('%y%m%d%H')))
            json.dump(newItemRes.json(), ijs, ensure_ascii=False)

        # dict化させたデータを返す
        return newItemRes.json()

def getApiShort(apiName, targetApi):
    # ファイルを照査、ある場合はそのjsonデータを取得する(10分以内のもの)
    target = glob.glob('api-log/{0}-*.json'.format(apiName))
    if len(target) != 0:
        target = target[0]
        # JSONの名前から取得時間帯を推測
        latestDate = datetime.datetime.strptime(target, 'api-log/{0}-%y%m%d%H%M.json'.format(apiName))

        # 取得可能時間
        shouldGetTime = latestDate + datetime.timedelta(minutes=10)

        # 現在時刻が取得可能時間を超えているか
        if shouldGetTime < now:
            doRead = False
        else:
            doRead = True
    else:
        doRead = False
    
    if doRead:
        with open('api-log/{0}-{1}.json'.format(apiName, latestDate.strftime('%y%m%d%H%M')), 'r', encoding="utf-8_sig") as ijs:
            return json.load(ijs)
    else:
        # フォルダを作成する。ある場合は無視してくれる
        os.makedirs('api-log/', exist_ok=True)

        # 前の時間に取得したAPIデータを削除(ある場合は)
        for deletePrevious in glob.glob('api-log/{0}-*.json'.format(apiName)):
            try:
                os.remove(deletePrevious)
                print('Purge: {0}'.format(deletePrevious))
            except FileNotFoundError: # もしファイルがなくてもエラーでスクリプトを止めないようにする（無視）
                pass

        # ない場合は新たにAPI取得する
        print("Getting datas from " + targetApi)
        newItemRes = requests.get(targetApi)

        # データを保管する
        with open('api-log/{0}-{1}.json'.format(apiName, now.strftime('%y%m%d%H%M')), 'w', encoding="utf-8_sig") as ijs:
            print('Insert: {0}-{1}'.format(apiName, now.strftime('%y%m%d%H%M')))
            json.dump(newItemRes.json(), ijs, ensure_ascii=False)

        # dict化させたデータを返す
        return newItemRes.json()
