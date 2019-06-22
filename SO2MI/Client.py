import configparser
import datetime
import json
import os
import re
import traceback
from json.decoder import JSONDecodeError
from pprint import pprint as pp
import textwrap

import discord
from pytz import timezone

from .Parser import ItemParser
from .Alias import showAlias, addAlias, removeAlias

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
        print("次のユーザーとしてログインしました:", self.user)

    async def on_message(self, message):
        if message.author.bot or message.author == self.user or int(config["discord"]["channel"]) != message.channel.id:
            # BOT属性アカウント, 自身のアカウント or 指定したチャンネル以外はスルー
            return

        # コマンド受取部
        # 市場情報コマンド
        if message.content.startswith(commandMarket):
            msgParse = message.content.split()
            # コマンドを削除
            del msgParse[0]
            if len(msgParse) == 0:
                await self.showHelpMarket()
            else:
                if re.match(r"([Hh][Ee][Ll][Pp]|[へヘﾍ][るルﾙ][ぷプﾌﾟ])", msgParse[0]):
                    await self.showHelpMarket()
                    return
                elif len(msgParse) == 1:
                    argMarket = "--normal"
                    townName = "--none"
                else:
                    # 商品名が1つになっていない場合引数かどうかを確認する
                    if len(msgParse) >= 2 and not re.match(r"^(-[a-zA-Z]|--[a-zA-Z]+)$", msgParse[1]): # 引数の形になっていない場合
                        await message.channel.send("同時に複数の商品を指定することはできません。")
                        return
                    else: # 引数の形だった場合
                        argMarket = msgParse[1]
                        if argMarket == "-s" or argMarket == "-r":
                            if len(msgParse) == 2: #[商品名] [引数]
                                print("引数は{}でした".format(argMarket))
                                townName = "--none"
                            else:
                                if msgParse[2] == "-t":
                                    if len(msgParse) == 3: # [商品名] [引数] -t
                                        print("街の名前が指定されていません")
                                        await message.channel.send("引数-tに対して街が指定されていません。")
                                        return
                                    elif len(msgParse) >= 5: # [商品名] [引数] -t OO XX
                                        print("街の名前が複数指定されています")
                                        await message.channel.send("引数-tに対して街を複数指定することはできません。")
                                        return
                                    else:
                                        townName = msgParse[3]
                        elif argMarket == "-t":
                            print("引数は-tでした")
                            if len(msgParse) == 2: # [商品名] -t
                                print("街の名前が指定されていません")
                                await message.channel.send("引数-tに対して街が指定されていません。")
                                return
                            elif len(msgParse) >= 4: # [商品名] -t OO XX
                                print("街の名前が複数指定されています")
                                await message.channel.send("引数-tに対して街を複数指定することはできません。")
                                return
                            else:
                                townName = msgParse[2]
                        elif argMarket == "--normal":
                            print("通常のリクエストです")
                        else:
                            print("引数{}は予約されていません".format(argMarket))
                            await message.channel.send("無効な引数です: " + argMarket)
                            return

                # Falseで返ってない場合はそのままチャットへ流す。Falseだった場合は見つからないと表示
                try:
                    print("{0} が {1} をリクエストしました".format(message.author, msgParse[0]))
                    print("引数は{}でした".format(argMarket))
                    itemName = msgParse[0]
                    parseRes = ItemParser(itemName, argMarket, townName)
                    if parseRes != False:
                        if parseRes == "nte":
                            await message.channel.send("{}という街は見つかりませんでした。".format(townName))
                        else:
                            await message.channel.send(parseRes)
                    else:
                        await message.channel.send("{}は見つかりませんでした。".format(itemName))
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

        # エイリアスコマンド
        if message.content.startswith(commandAlias):
            msgParse = message.content.split()
            del msgParse[0]
            if len(msgParse) == 0:
                helpMsg = textwrap.dedent(f"""
                {commandMarket}で商品を指定したときに、登録されたエイリアスを正式名称に変換します。
                ・add
                　エイリアスを追加します。
                　使用方法: {commandAlias} add <エイリアス名> <正式名称>
                ・help
                　このヘルプを表示します。
                ・show
                　エイリアス一覧を表示します。
                """)
                await message.channel.send(helpMsg)
                return
            else:
                if msgParse[0] == "add":
                    if len(msgParse) != 3:
                        helpMsg = textwrap.dedent(f"""
                        エイリアスを追加します。
                        使用方法: {commandAlias} add <エイリアス名> <正式名称>
                        """)
                        await message.channel.send(helpMsg)
                        return
                    
                    res = addAlias(msgParse[1], msgParse[2])
                    if res == None:
                        await message.channel.send("申し訳ありません。書き込みができません。")
                        return
                    elif res == False:
                        await message.channel.send("既に登録されています。")
                        return
                    else:
                        await message.channel.send(f"エイリアスを追加しました。\n{msgParse[1]} → {msgParse[2]}")
                        return

                elif msgParse[0] == "remove":
                    if len(msgParse) != 2:
                        helpMsg = textwrap.dedent(f"""
                        エイリアスを追加します。
                        使用方法: {commandAlias} remove <エイリアス名>
                        """)
                        await message.channel.send(helpMsg)
                        return

                    res = removeAlias(msgParse[1])
                    if res == None:
                        await message.channel.send("申し訳ありません。書き込みができません。")
                        return
                    elif res == False:
                        await message.channel.send(f"{msgParse[1]}というエイリアス名は存在しません。")
                        return
                    else:
                        await message.channel.send("エイリアスを削除しました。")
                        return

                elif re.match(r"([Hh][Ee][Ll][Pp]|[へヘﾍ][るルﾙ][ぷプﾌﾟ])", msgParse[0]):
                    helpMsg = textwrap.dedent(f"""
                    {commandMarket}で商品を指定したときに、登録されたエイリアスを正式名称に変換します。
                    ・add
                    　エイリアスを追加します。
                    　使用方法: {commandAlias} add <エイリアス名> <正式名称>
                    ・help
                    　このヘルプを表示します。
                    ・show
                    　エイリアス一覧を表示します。
                    """)
                    await message.channel.send(helpMsg)
                    return

                elif msgParse[0] == "show":
                    res = showAlias()
                    if res == False:
                        await message.channel.send("エイリアスは登録されていません。")
                        return
                    else:
                        await message.channel.send(res)
                        return

                else:
                    await message.channel.send("コマンドが無効です。")
                    return

    async def showHelpMarket(self):
        helpMsg = textwrap.dedent(f"""
        市場に出ている商品・レシピ品の販売価格や注文価格などを調べることができます。
        使用方法: {commandMarket} [商品名] [-s|-r] [-t 街名]
        出力情報一覧: 
        ・販売
        　・最安値
        　・最高値
        　・最安TOP5平均
        　・全体平均
        　・市場全体の個数
        　・販売店舗数
        ・注文
        　・最高値
        　・最安値
        　・最高TOP5平均
        　・全体平均
        　・市場全体の注文数
        　・注文店舗数

        引数:
        -s: 販売品の情報のみを表示することができます。
        -r: 注文品の情報のみを表示することができます。
        -t 街名: 指定した街の情報のみを表示することができます。-s、-tとは併用可能です。
        
        {commandMarket} help(ヘルプ等でも可) でこのヘルプを表示することができます。
        """)
        await self.targetChannel.send(helpMsg)
