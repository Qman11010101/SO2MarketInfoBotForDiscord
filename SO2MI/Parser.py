from .Alias import alias
import json
import datetime
import os
import requests

def ItemParser(itemName):
    now = datetime.datetime.now()
    if os.path.isfile('api-log/item/item-{}.json'.format(now.strftime('%y%m%d%H'))):
        with open('api-log/item/item-{}.json'.format(now.strftime('%y%m%d%H')), 'r', encoding="utf-8_sig") as ijs:
            print("READ: item-{}.json".format(now.strftime('%y%m%d%H')))
            item = json.load(ijs)
    else:
        newItemRes = requests.get("https://so2-api.mutoys.com/master/item.json")
        item = newItemRes.json()
        with open('api-log/item/item-{}.json'.format(now.strftime('%y%m%d%H')), 'w', encoding="utf-8_sig") as ijs:
            print("WRITE: item-{}.json".format(now.strftime('%y%m%d%H')))
            json.dump(item, ijs, ensure_ascii=False)

    #略称などの変換
    itemName = alias(itemName)
    #アイテムID取得部
    itemId = 0
    for col in item:
        if item[str(col)]["name"] == itemName:
            itemId = col
            break

    print(itemId)
    if int(itemId) == 0:
        return False
    else:
        return "# TODO 返ってきた情報を基にごにょごにょと（途中）"
