import json
import os
from json.decoder import JSONDecodeError

from .Alias import alias
from .getApi import getApi
from .Exceptions import SameItemExistError, NoItemError

def addRegister(itemName):
    if os.access("itemreg.json", os.W_OK):
        if os.path.isfile("itemreg.json"):
            with open("itemreg.json", "r", encoding="utf-8_sig") as itf:
                itemreg = json.load(itf)
            
            # 登録済みアイテム読み込み・アイテム名エイリアス変換
            itemList = itemreg["items"]
            itemName = alias(itemName)
            
            # もしすでにあったらSameItemExistErrorを返す
            if itemName in itemList:
                raise SameItemExistError("existent of the same item")

            # 登録されるアイテムが存在しなければNoItemErrorを返す
            item = getApi("item", "https://so2-api.mutoys.com/master/item.json")
            recipe = getApi("recipe", "https://so2-api.mutoys.com/json/master/recipe_item.json")
            itemId = 0
            for col in item:
                if item[str(col)]["name"] == itemName:
                    itemId = col
                    break
    
            if int(itemId) == 0:
                for col in recipe:
                    if recipe[str(col)]["name"] == itemName:
                        itemId = col
                        break

            if int(itemId) == 0:
                raise NoItemError("nonexistent of item")

            # アイテム名を追加
            itemreg["items"].append(itemName)
            
            # jsonを保存
            with open("itemreg.json", "w", encoding="utf-8_sig") as itf:
                json.dump(itemreg, itf, indent=4, ensure_ascii=False)
            
            return True
        else:
            itemreg = {}

            itemreg["items"] = [itemName]

            with open("itemreg.json", "w", encoding="utf-8_sig") as itf:
                json.dump(itemreg, itf, indent=4, ensure_ascii=False)

            return True
    else:
        itemreg = {}

        itemreg["items"] = [itemName]

        with open("itemreg.json", "w", encoding="utf-8_sig") as itf:
            json.dump(itemreg, itf, indent=4, ensure_ascii=False)

        return True

def removeRegister(itemName):
    if os.access("itemreg.json", os.W_OK):
        if os.path.isfile("itemreg.json"):
            with open("itemreg.json", "r", encoding="utf-8_sig") as itf:
                itemreg = json.load(itf)
            
            # 登録済みアイテム読み込み・アイテム名エイリアス変換
            itemList = itemreg["items"]
            itemName = alias(itemName)

            for items in itemList:
                if itemName == items:
                    itemList.remove(items)
                    with open("itemreg.json", "w", encoding="utf-8_sig") as itf:
                        json.dump(itemreg, itf, indent=4, ensure_ascii=False)
                    return True
            return False
        else:
            return False
    else:
        raise OSError("couldn't access to itemreg.json")

def showRegister():
    if os.path.isfile("itemreg.json"):
        try:
            with open("itemreg.json", "r", encoding="utf-8_sig") as itf:
                itemreg = json.load(itf)
            
            itemList = itemreg["items"]
            parsed = ""

            # 表示するアイテムを1行ずつ代入
            for items in itemList:
                parsed += items + "\n"
            
            outputStr = f"以下のアイテムが登録されています:\n\n{parsed}"
            return outputStr
        except JSONDecodeError as exc:
            print("itemreg.jsonの構文にエラーがあります\n行: {0} 位置: {1}\n{2}".format(exc.lineno, exc.pos, exc.msg))
            return False
    else:
        return False
