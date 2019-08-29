import datetime
import json
import textwrap
import asyncio

import discord
from pytz import timezone

from .getApi import getApi

def chkCost():
    # 0:00から数えて朝7:00を過ぎているかチェック、過ぎていなければ「""」を返す
    # アイテムが登録されたjsonを読み込む
    # forで回す(できれば何度もループするのは避けたい、アイテム名 in 辞書型とか使ったら一発で行けたりしないだろうか？)
    # あわせてアイテムの存在判定もなんとかしたい
    # 文章を整えてreturn
    return "in dev"

def chkDate():
    # 月末かどうかチェック、違えば「""」を返す
    # 優待券等の案内をする
    return "in dev"