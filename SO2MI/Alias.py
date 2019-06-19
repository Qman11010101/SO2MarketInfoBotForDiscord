import os
import json
from json.decoder import JSONDecodeError

def alias(itemName):
    print("alias.jsonを探しています")
    if os.path.isfile("alias.json"):
        print("alias.jsonが見つかりました")
        try:
            with open("alias.json", "r") as alf:
                alias = json.load(alf)
        except JSONDecodeError as exc:
            print("alias.jsonの構文にエラーがあります\n行: {0} 位置: {1}\n{2}".format(exc.lineno, exc.pos, exc.msg))
            return itemName
    else:
        print("alias.jsonが見つかりませんでした")
        return itemName
    
    # for文で解析
    for element in alias:
        for aliasName in alias[element]: # 第二階層目がエイリアス名なのでその中から照査
            if aliasName == itemName:
                # 名前とエイリアス名が一致した場合はエイリアス名と紐づく名前を返す
                return element
    # エイリアス名が見つからない場合はそのまま返す
    return itemName
