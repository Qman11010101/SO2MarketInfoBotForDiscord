import configparser
import datetime
import json
import os
import re
import traceback
from json.decoder import JSONDecodeError
from pprint import pprint as pp

import discord
from pytz import timezone

from .Parser import ItemParser

config = configparser.ConfigParser()
config.read("config.ini")

commandMarket = config["command"]["prefix"] + config["command"]["market"]
commandAlias = config["command"]["prefix"] + config["command"]["alias"]

class Client(discord.Client):
    async def on_ready(self):
        # 設定されているチャンネルIDに接続
        self.targetChannel = self.get_channel(int(config["discord"]["channel"]))
        if self.targetChannel == None:
            # 指定チャンネルが見つからない場合はExceptionをraise
            raise Exception("指定されたチャンネルは見つかりませんでした")
        else:
            # await self.targetChannel.send("{0} is Ready!".format(self.user))
            pass
        print("次のユーザーとしてログインしました", self.user)

    async def on_message(self, message):
        if message.author.bot or message.author == self.user or int(config["discord"]["channel"]) != message.channel.id:
            # BOT属性アカウント, 自身のアカウント or 指定したチャンネル以外はスルー
            return

        # 内部処理はここから
        if message.content.startswith(commandMarket):
            msgParse = message.content.split()
            # コマンドを削除
            del msgParse[0]
            print("{0} => {1}".format(message.author, msgParse))
            if len(msgParse) == 0:
                await self.showHelpMarket()
            else:
                if re.match(r"([Hh][Ee][Ll][Pp]|[へヘﾍ][るルﾙ][ぷプﾌﾟ])", msgParse[0]):
                    await self.showHelpMarket()
                else:
                    # 2つ以上指定している場合は弾く
                    if len(msgParse) >= 2:
                        await message.channel.send("商品は1つのみを指定してください。")
                        return
                    
                    # Falseで返ってない場合はそのままチャットへ流す。Falseだった場合は見つからないと表示
                    try:
                        arg = msgParse[0]
                        parseRes = ItemParser(arg)
                        if parseRes != False:
                            await message.channel.send(parseRes)
                        else:
                            await message.channel.send("{0}は見つかりませんでした。".format(arg))
                    except:
                        now = datetime.datetime.now(timezone(config["misc"]["timezone"]))
                        nowFormat = now.strftime("%Y/%m/%d %H:%M:%S%z")
                        nowFileFormat = now.strftime("%Y%m%d")
                        os.makedirs("error-log", exist_ok=True)
                        with open(f"error-log/{nowFileFormat}.txt", "a") as f:
                            f.write(f"--- Datetime: {nowFormat} ---\n")
                            traceback.print_exc(file=f)
                            f.write("\n")
                        traceback.print_exc()
                        await message.channel.send("申し訳ありません。エラーが発生したため、市場情報をチェックできません。\nこのエラーが続く場合はbot管理者へお問い合わせください。")
                    finally:
                        return

        # エイリアス
        if message.content.startswith(commandAlias):
            if os.path.isfile("alias.json"):
                try:                    
                    with open("alias.json", "r", encoding="utf-8_sig") as alf:
                        alias = json.load(alf)
                    
                    parsed = ""

                    for element in alias:
                        parsed += ", ".join(alias[element]) + " → " + element + "\n"
                    
                    outputStr = f"以下のエイリアスが登録されています:\n\n{parsed}"
                    await message.channel.send(outputStr)
                    return
                except JSONDecodeError as exc:
                    print("alias.jsonの構文にエラーがあります\n行: {0} 位置: {1}\n{2}".format(exc.lineno, exc.pos, exc.msg))
                    await message.channel.send("エイリアスは登録されていません。")
                    return
            else:
                await message.channel.send("エイリアスは登録されていません。")
                return

    async def showHelpMarket(self):
        helpMsg = f"""
        SO2市場情報bot
        市場に出ている商品・レシピ品の販売価格や注文価格などを調べることができます。
        使用方法: {commandMarket} [商品名]
        出力情報一覧: 
        ・販売
        　・最安値
        　・最高値
        　・最安TOP5平均
        　・全体平均
        　・市場全体の個数
        ・注文
        　・最高値
        　・最安値
        　・最高TOP5平均
        　・全体平均
        　・市場全体の注文数
        
        {commandMarket} help(ヘルプ等でも可) でこのヘルプを表示することができます。
        """
        await self.targetChannel.send(helpMsg)
