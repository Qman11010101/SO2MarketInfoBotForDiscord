import re
import textwrap
import json

from .getApi import getApi
from .Exceptions import NoCategoryError

def itemSearch(string, argument, category, beta):
    # API取得部
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

    # 正規表現のコンパイル
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

    # 表示文字列生成部
    if len(listItem) + len(listRecipe) == 0:
        msgReturn = f"{catStr}正規表現「{string}」に合致するアイテムは見つかりませんでした。"
    else:
        if len(listItem) == 0:
            liststrItem = ""
        else:
            liststrItem = "\n\n**アイテム:**\n" + "\n".join(listItem)
        if len(listRecipe) == 0:
            liststrRecipe = ""
        else:
            liststrRecipe = "\n\n**レシピ品:**\n" + "\n".join(listRecipe)
        msgReturn = f"{catStr}正規表現「{string}」に合致する以下のアイテムが見つかりました:{liststrItem}{liststrRecipe}"
    
    return msgReturn
