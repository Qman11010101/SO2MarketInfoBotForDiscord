import os
import json
from json.decoder import JSONDecodeError

def alias(itemName):
    print("alias.jsonを探しています")
    if os.path.isfile("alias.json"):
        print("alias.jsonが見つかりました")
        try:
            with open("alias.json", "r", encoding="utf-8_sig") as alf:
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

def showAlias():
    if os.path.isfile("alias.json"):
        try:
            with open("alias.json", "r", encoding="utf-8_sig") as alf:
                alias = json.load(alf)
            
            parsed = ""

            # 表示するエイリアスと正式名称を1行ずつ代入
            for element in alias:
                parsed += ", ".join(alias[element]) + " → " + element + "\n"
            
            outputStr = f"以下のエイリアスが登録されています:\n\n{parsed}"
            return outputStr
        except JSONDecodeError as exc:
            print("alias.jsonの構文にエラーがあります\n行: {0} 位置: {1}\n{2}".format(exc.lineno, exc.pos, exc.msg))
            return False
    else:
        return False

def addAlias(aliasName, formalName):
    if os.access("alias.json", os.W_OK):
        if os.path.isfile("alias.json"):
            with open("alias.json", "r", encoding="utf-8_sig") as alf:
                alias = json.load(alf)
            
            # エイリアス名を(正式名称を含まず)全部リストにする
            allAlias = []
            for aliasPart in alias:
                allAlias += alias[aliasPart]
            
            # もしすでにあったらFalseを返す
            if aliasName in allAlias:
                return False

            # 正式名称がすでにalias.jsonにあればそこのエイリアスに追加、なければ新規登録
            if formalName in alias:
                alias[formalName].append(aliasName)
            else:
                alias[formalName] = [aliasName]
            
            # jsonを保存
            with open("alias.json", "w", encoding="utf-8_sig") as alf:
                json.dump(alias, alf, indent=4, ensure_ascii=False)
            
            return True
        else:
            alias = {}

            alias[formalName] = [aliasName]

            with open("alias.json", "w", encoding="utf-8_sig") as alf:
                json.dump(alias, alf, indent=4, ensure_ascii=False)

            return True
    else:
        return None

def removeAlias(aliasName):
    if os.access("alias.json", os.W_OK):
        if os.path.isfile("alias.json"):
            with open("alias.json", "r", encoding="utf-8_sig") as alf:
                alias = json.load(alf)
            
            for element in alias:
                for aliasPart in alias[element]:
                    if aliasPart == aliasName:
                        alias[element].remove(aliasPart)
                        if len(alias[element]) == 0:
                            del alias[element]
                        with open("alias.json", "w", encoding="utf-8_sig") as alf:
                            json.dump(alias, alf, indent=4, ensure_ascii=False)
                        return True
            return False
        else:
            return False
    else:
        return None
