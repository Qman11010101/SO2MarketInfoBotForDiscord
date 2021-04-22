import json
import re
import textwrap

from .Exceptions import NoCategoryError
from .getApi import getApi


def itemSearch(string, argument, category, beta):
    if beta == "--release":
        item = getApi("item", "https://so2-api.mutoys.com/master/item.json")
        recipe = getApi("recipe", "https://so2-api.mutoys.com/json/master/recipe_item.json")
    else:
        item = getApi("item_beta", "https://so2-beta.mutoys.com/master/item.json")
        recipe = getApi("recipe_beta", "https://so2-beta.mutoys.com/json/master/recipe_item.json")

    # カテゴリ指定がされていればカテゴリのリスト(set)を生成
    catStr = ""
    if category != "none":
        catSet = set()
        for col in item:
            catSet.add(item[str(col)]["category"])
        if category not in catSet:
            raise NoCategoryError("such category doesn't exist")
        catStr = f"{category}カテゴリの中で"

    reg = re.compile(string)

    # 合致するアイテムの取得
    listItem = []
    listRecipe = []
    if argument in ("-i", "-n"):
        for col in item:
            if reg.search(item[str(col)]["name"]):
                if category == "none":
                    listItem.append(item[str(col)]["name"])
                else:
                    if item[str(col)]["category"] == category:
                        listItem.append(item[str(col)]["name"])
    if argument in ("-r", "-n"):
        for col in recipe:
            if reg.search(recipe[str(col)]["name"]):
                if category == "none":
                    listRecipe.append(recipe[str(col)]["name"])
                else:
                    if recipe[str(col)]["category"] == category:
                        listRecipe.append(recipe[str(col)]["name"])

    if len(listItem) + len(listRecipe) == 0:
        msgReturn = [f"{catStr}正規表現「{string}」に合致するアイテムは見つかりませんでした。"]
    else:
        mR = 0
        msgReturn = [f"{catStr}正規表現「{string}」に合致する以下のアイテムが見つかりました:"]
        if len(listItem) != 0:
            msgReturn[mR] += "\n\n**アイテム:**\n"
            for iName in listItem:
                if len(msgReturn[mR]) > 1750:
                    msgReturn.append("")
                    mR += 1
                msgReturn[mR] += f"{iName}\n"
        if len(listRecipe) != 0:
            msgReturn[mR] += "\n**レシピ品:**\n"
            for rName in listRecipe:
                if len(msgReturn[mR]) > 1750:
                    msgReturn.append("")
                    mR += 1
                msgReturn[mR] += f"{rName}\n"
    
    return msgReturn
