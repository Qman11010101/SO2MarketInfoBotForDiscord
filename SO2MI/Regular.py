import datetime
import json
import textwrap
import asyncio
import configparser
import calendar
import textwrap

import discord
import pytz

from .getApi import getApi

def chkCost():
    # タイムゾーン指定のためconfig.iniの読み込み
    config = configparser.ConfigParser()
    config.read("config.ini")

    # 現在時刻取得
    timezone = pytz.timezone(config["misc"]["timezone"])
    now = datetime.datetime.now(timezone)

    # 時刻判定
    startHour = int(config["misc"]["RegExcHour"])
    startMin = int(config["misc"]["RegExcMinute"])
    endMin = startMin + int(config["misc"]["RegExcCheckTime"])
    if now.hour == startHour and startMin <= now.minute <= endMin:
        # アイテムが登録されたjsonを読み込む
        # forで回す(できれば何度もループするのは避けたい、アイテム名 in 辞書型とか使ったら一発で行けたりしないだろうか？)
        # あわせてアイテムの存在判定もなんとかしたい
        # 文章を整えてreturn
        return "in dev"
    else:
        return False

def chkEndOfMonth():
    # タイムゾーン指定のためconfig.iniの読み込み
    config = configparser.ConfigParser()
    config.read("config.ini")

    # 現在時刻取得
    timezone = pytz.timezone(config["misc"]["timezone"])
    now = datetime.datetime.now(timezone)

    # 月末判定
    dayLast = int(calendar.monthrange(now.year, now.month)[1]) # 月の最終日取得
    if now.day != dayLast: # 最終日じゃなければ何もしないようにする
        return False

    # 時刻判定
    startHour = int(config["misc"]["RegExcHour"])
    startMin = int(config["misc"]["RegExcMinute"])
    endMin = startMin + int(config["misc"]["RegExcCheckTime"])
    if now.hour == startHour and startMin <= now.minute <= endMin:
        message = textwrap.dedent("""
         
        【Information】
        本日は月末です。優待券・優待回数券・優待お試し券をお持ちの方は使用しておくと翌日にスピードポーション30本を取得できます。
        優待券と優待回数券は作業枠が埋まっていても使用可能ですが、優待お試し券は作業枠が空いている必要がありますのでご注意ください。
        """)
        return message
    else:
        return False
