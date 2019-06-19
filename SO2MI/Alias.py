import os
import json
from json.decoder import JSONDecodeError

def alias(itemName):
    if os.path.isfile('alias.json'):
        try:
            with open('alias.json', 'r') as alf:
                alias = json.load(alf)
        except JSONDecodeError as exc:
            print('alias.jsonの構文にエラーがあります。\n行: {0} 位置: {1}\n{2}\n\nそのまま返します。'.format(exc.lineno, exc.pos, exc.msg))
            return itemName
    else:
        print('alias.jsonが見つかりません。そのまま返します。')
        return itemName
    
    # for文で解析
    for alia in alias:
        for aliasName in alias[alia]: # 第二階層目がエイリアス名なのでその中から照査
            if aliasName == itemName:
                # 名前とエイリアス名が一致した場合はそれを使用
                return alia
    # エイリアス名がない場合はそのまま返す
    return itemName
