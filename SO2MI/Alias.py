import os
import json
from json.decoder import JSONDecodeError

from .getApi import getApi
from .Exceptions import NoItemError, NameDuplicationError, SameAliasNameExistError

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
            
            # もしすでにあったらSameAliasNameExistErrorを返す
            if aliasName in allAlias:
                raise SameAliasNameExistError("existent of the same alias name")

            # 正式名称がアイテムに存在しなければNoItemErrorを返す
            item = getApi("item", "https://so2-api.mutoys.com/master/item.json")
            recipe = getApi("recipe", "https://so2-api.mutoys.com/json/master/recipe_item.json")
            itemId = 0
            for col in item:
                if item[str(col)]["name"] == formalName:
                    itemId = col
                    break
    
            if int(itemId) == 0:
                for col in recipe:
                    if recipe[str(col)]["name"] == formalName:
                        itemId = col
                        break
                        
            if int(itemId) == 0:
                raise NoItemError("nonexistent of item")

            # エイリアス名と何かのアイテムの名前が被っていたらnameDuplicationErrorを返す
            itemId = 0
            for col in item:
                if item[str(col)]["name"] == aliasName:
                    itemId = col
                    break
    
            if int(itemId) == 0:
                for col in recipe:
                    if recipe[str(col)]["name"] == aliasName:
                        itemId = col
                        break
            if int(itemId) != 0:
                raise NameDuplicationError("duplication of alias name")

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
        raise OSError("couldn't access to alias.json")

def removeAlias(aliasName):
    if os.access("alias.json", os.W_OK):
        if os.path.isfile("alias.json"):
            with open("alias.json", "r", encoding="utf-8_sig") as alf:
                alias = json.load(alf)
            
            for element in alias:
                for aliasPart in alias[element]:
                    # エイリアス名が合致したら消す
                    if aliasPart == aliasName:
                        alias[element].remove(aliasPart)
                        # エイリアス名がなくなったら項目ごと消す
                        if len(alias[element]) == 0:
                            del alias[element]
                        with open("alias.json", "w", encoding="utf-8_sig") as alf:
                            json.dump(alias, alf, indent=4, ensure_ascii=False)
                        return True
            return False
        else:
            return False
    else:
        raise OSError("couldn't access to alias.json")
