import textwrap

from .Alias import alias
from .Exceptions import NoItemError
from .getApi import getApi


def wikiLinkGen(itemName):
    item = getApi("item", "https://so2-api.mutoys.com/master/item.json")

    itemName = alias(itemName)

    itemId = 0
    for col in item:
        if item[str(col)]["name"] == itemName:
            itemId = col
            category = item[str(col)]["category"]
            break
    if int(itemId) == 0:
        raise NoItemError("nonexistent of item")
    
    wikiurl = f"https://wikiwiki.jp/sold2/アイテム/{category}/{itemName}"
    msg = textwrap.dedent(f"""
    以下のURLから{itemName}のWikiページに行くことができます:
    {wikiurl}

    ページは存在しない場合があります。
    """)

    return msg
