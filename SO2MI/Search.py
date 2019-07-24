import re
import textwrap
import json

from .getApi import getApi

def itemSearch(string, argument, beta):
    # API取得部
    if beta == "--release":
        item = getApi("item", "https://so2-api.mutoys.com/master/item.json")
        recipe = getApi("recipe", "https://so2-api.mutoys.com/json/master/recipe_item.json")
    else:
        item = getApi("item_beta", "https://so2-beta.mutoys.com/master/item.json")
        recipe = getApi("recipe_beta", "https://so2-beta.mutoys.com/json/master/recipe_item.json")

    # 正規表現のコンパイル
    reg = re.compile(string)

    listItem = []
    listRecipe = []
    if argument in ("-i", "-n"):
        for col in item:
            if reg.search(item[str(col)]["name"]):
                listItem.append(item[str(col)]["name"])
    if argument in ("-r", "-n"):
        for col in recipe:
            if reg.search(recipe[str(col)]["name"]):
                listRecipe.append(recipe[str(col)]["name"])

    if len(listItem) + len(listRecipe) == 0:
        msgReturn = f"文字列「{string}」を含むアイテムは見つかりませんでした。"
    else:
        if len(listItem) == 0:
            liststrItem = ""
        else:
            liststrItem = "\n\n**アイテム:**\n" + "\n".join(listItem)
        if len(listRecipe) == 0:
            liststrRecipe = ""
        else:
            liststrRecipe = "\n\n**レシピ品:**\n" + "\n".join(listRecipe)
        msgReturn = f"文字列「{string}」に合致する以下のアイテムが見つかりました:{liststrItem}{liststrRecipe}"
    
    return msgReturn
