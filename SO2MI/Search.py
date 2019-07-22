import re
import textwrap
import json

from .getApi import getApi

def itemSearch(string, argument, beta):
    # API取得部
    item = getApi("item", "https://so2-api.mutoys.com/master/item.json")
    recipe = getApi("recipe", "https://so2-api.mutoys.com/json/master/recipe_item.json")

    # 正規表現のコンパイル
    reg = re.compile(string)

    itemlist = []
    for col in item:
        if reg.search(item[str(col)]["name"]):
            itemlist.append(item[str(col)]["name"])
    for col in recipe:
        if reg.search(recipe[str(col)]["name"]):
            itemlist.append(recipe[str(col)]["name"])

    if len(itemlist) == 0:
        msgReturn = f"文字列「{string}」を含むアイテムは見つかりませんでした。"
    else:
        liststr = "\n".join(itemlist)
        msgReturn = f"文字列「{string}」に合致する以下のアイテムが見つかりました:\n\n{liststr}"
    
    return msgReturn
    