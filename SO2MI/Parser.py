from .Alias import alias
from .getApi import getApi

def ItemParser(itemName):
    item = getApi('item', "https://so2-api.mutoys.com/master/item.json")
    recipe = getApi('recipe', "https://so2-api.mutoys.com/json/master/recipe_item.json")

    # 略称などの変換
    itemName = alias(itemName)
    # アイテムID取得部
    itemId = 0
    for col in item:
        if item[str(col)]["name"] == itemName:
            itemId = col
            break
    
    if int(itemId) == 0:
        for col in recipe:
            if recipe[col]["name"] == itemName:
                itemId = col
                break
        if int(itemId) == 0:
            # 見つからない扱い
            return False
    
    # 此処から先をこれから
    return "# TODO 返ってきた情報を基にごにょごにょと（途中）"
