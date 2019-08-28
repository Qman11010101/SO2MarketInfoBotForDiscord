import configparser
import datetime
import json
import os
import re
import traceback
from json.decoder import JSONDecodeError
from pprint import pprint as pp
import textwrap
import sys

import discord
from pytz import timezone

from .Parser import itemParser
from .Alias import showAlias, addAlias, removeAlias
from .Search import itemSearch
from .Exceptions import NameDuplicationError, NoItemError, SameAliasNameExistError, NoTownError, NoCategoryError
from .Wiki import wikiLinkGen

config = configparser.ConfigParser()
config.read("config.ini")

prefix = config["command"]["prefix"]

commandMarket = prefix + config["command"]["market"]
commandAlias = prefix + config["command"]["alias"]
commandShutdown = prefix + config["command"]["shutdown"]
commandVersion = prefix + config["command"]["version"]
commandSearch = prefix + config["command"]["search"]
commandHelp = prefix + config["command"]["help"]
commandWiki = prefix + config["command"]["wiki"]

adminID = config["misc"]["administrator"]

DEFINE_VERSION = "DEV-EXTRA-8"

class Client(discord.Client):
    async def on_ready(self):
        # 設定されているチャンネルIDに接続
        self.targetChannel = self.get_channel(int(config["discord"]["channel"]))
        if self.targetChannel == None:
            # 指定チャンネルが見つからない場合はExceptionをraise
            raise Exception("指定されたチャンネルは見つかりませんでした")
        else:
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
            # コマンド単体だった場合
            if len(msgParse) == 0:
                await self.showHelpMarket()
                return
            else:
                # ヘルプ表示の場合
                if re.match(r"([Hh][Ee][Ll][Pp]|[へヘﾍ][るルﾙ][ぷプﾌﾟ])", msgParse[0]):
                    await self.showHelpMarket()
                    return
                # 商品名が1つの場合
                elif len(msgParse) == 1:
                    msgParse.extend(["-n", "-t", "none", "--release", "--end"]) # 「[商品名] -n -t none --release --end」というコマンド文字列を生成する
                else:
                    if msgParse[-1] != "--end":
                        msgParse.append("--end") # 終端引数を追加する
                    # 商品名が1つになっていない場合引数かどうかを確認する
                    if len(msgParse) >= 2 and not re.match(r"^(-[a-zA-Z]|--[a-zA-Z]+)$", msgParse[1]): # 引数の形になっていない場合
                        await message.channel.send("エラー: 同時に複数の商品を指定することはできません。")
                        return
                    else: # 引数の形だった場合
                        # 引数が正しいか判定する(変な引数は全部ここで弾かれる)
                        for arg in msgParse:
                            # 引数の形をしているが予約されていないものがあったらエラー
                            if re.match(r"^(-[a-zA-Z]|--[a-zA-Z]+)$", arg):
                                if arg not in ("-s", "-r", "-t", "-b", "--end"): # ここに最初の引数になる可能性のあるものを追加していく
                                    print(f"エラー: 引数{arg}は予約されていません")
                                    await message.channel.send("エラー: 無効な引数です: " + arg)
                                    return
                        # 第1引数[-s|-r|-n]
                        if msgParse[1] != "-s" and msgParse[1] != "-r":
                            msgParse.insert(1, "-n")
                        # 第2引数/第3引数[-t ***]
                        if msgParse[2] != "-t":
                            msgParse.insert(2, "-t")
                            msgParse.insert(3, "none")
                        else: # [-t]のときの処理
                            # 街の名前を参照したとき引数の形が出てきたら街が指定されていない
                            if re.match(r"^(-[a-zA-Z]|--[a-zA-Z]+)$", msgParse[3]):
                                await message.channel.send("エラー: 引数-tに対して街の名前が指定されていません。")
                                return
                            else:
                                # 第4引数を参照して引数の形でなければ街を参照したと見做す
                                if not re.match(r"^(-[a-zA-Z]|--[a-zA-Z]+)$", msgParse[4]):
                                    await message.channel.send("エラー: 引数-tに対して街を複数指定することはできません。")
                                    return
                        # 第4引数[-b]
                        if msgParse[4] != "-b":
                            msgParse.insert(4, "--release")

                # Falseで返ってない場合はそのままチャットへ流す。Falseだった場合は見つからないと表示
                try:
                    print(f"{message.author} が {msgParse[0]} をリクエストしました")
                    parseRes = itemParser(msgParse[0], msgParse[1], msgParse[3], msgParse[4])
                    if parseRes != False:
                        await message.channel.send(parseRes)
                    else:
                        await message.channel.send(f"エラー: {msgParse[0]}は見つかりませんでした。")
                except NoTownError:
                    await message.channel.send(f"エラー: {msgParse[3]}という街は見つかりませんでした。")
                except:
                    await self.errorWrite()
                finally:
                    return

        # エイリアスコマンド
        if message.content.startswith(commandAlias):
            msgParse = message.content.split()
            del msgParse[0]
            if len(msgParse) == 0:
                await self.showHelpAlias()
                return
            else:
                if msgParse[0] == "add":
                    if len(msgParse) != 3:
                        helpMsg = textwrap.dedent(f"""
                        エイリアスを追加します。
                        使用方法: {commandAlias} add [エイリアス名] [正式名称]
                        """)
                        await message.channel.send(helpMsg)
                        return
                    
                    try:
                        addAlias(msgParse[1], msgParse[2])
                    except OSError:
                        await message.channel.send("エラー: alias.jsonにアクセスできません。")
                    except SameAliasNameExistError:
                        await message.channel.send("エラー: 既に登録されています。")
                    except NoItemError:
                        await message.channel.send(f"エラー: {msgParse[2]}は存在しません。")
                    except NameDuplicationError:
                        await message.channel.send(f"エラー: {msgParse[1]}というアイテムが既に存在しています。")
                    except:
                        await self.errorWrite()
                    else:
                        await message.channel.send(f"エイリアスを追加しました。\n{msgParse[1]} → {msgParse[2]}")
                    finally:
                        return

                elif msgParse[0] == "remove":
                    if len(msgParse) != 2:
                        helpMsg = textwrap.dedent(f"""
                        エイリアスを削除します。
                        使用方法: {commandAlias} remove [エイリアス名]
                        """)
                        await message.channel.send(helpMsg)
                        return

                    try:
                        if removeAlias(msgParse[1]):
                            await message.channel.send("エイリアスを削除しました。")
                        else:
                            await message.channel.send(f"エラー: {msgParse[1]}というエイリアス名は存在しません。")
                    except OSError:
                        await message.channel.send("エラー: alias.jsonにアクセスできません。")
                    except:
                        await self.errorWrite()
                    finally:
                        return

                elif re.match(r"([Hh][Ee][Ll][Pp]|[へヘﾍ][るルﾙ][ぷプﾌﾟ])", msgParse[0]):
                    await self.showHelpAlias()
                    return

                elif msgParse[0] == "show":
                    res = showAlias()
                    if res == False:
                        await message.channel.send("エラー: エイリアスは登録されていません。")
                        return
                    else:
                        await message.channel.send(res)
                        return

                else:
                    await message.channel.send("エラー: コマンドが無効です。")
                    return

        # シャットダウンコマンド
        if message.content.startswith(commandShutdown):
            try:
                if re.match(r"[0-9]+", str(adminID)):
                    if message.author.id == int(adminID):
                        await message.channel.send("botがシャットダウンされます。")
                        sys.exit()
                    else:
                        await message.channel.send("エラー: コマンドを実行する権限がありません。")
            except ValueError:
                await message.channel.send("エラー: 設定ファイルで指定された管理者のユーザーIDの形式が正しくありません。")
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
            finally:
                return

        # バージョンコマンド
        if message.content.startswith(commandVersion):
            verMsg = textwrap.dedent(f"""
            **SOLD OUT 2 市場情報bot for Discord**

            Version {DEFINE_VERSION}
            製作者: キューマン・エノビクト、ゆずりょー
            ライセンス: MIT License
            リポジトリ: https://github.com/Qman11010101/SO2MarketInfoBotForDiscord
            """)
            await message.channel.send(verMsg)
            return

        # アイテム検索コマンド
        if message.content.startswith(commandSearch):
            msgParse = message.content.split()
            # コマンドを削除
            del msgParse[0]
            # コマンド単体だった場合
            if len(msgParse) == 0:
                await self.showHelpSearch()
                return
            else:
                # ヘルプ表示の場合
                if re.match(r"([Hh][Ee][Ll][Pp]|[へヘﾍ][るルﾙ][ぷプﾌﾟ])", msgParse[0]):
                    await self.showHelpSearch()
                    return
                elif len(msgParse) == 1: # 検索文字列単体
                    msgParse.extend(["-n", "-c", "none", "--release", "--end"])
                else:
                    if msgParse[-1] != "--end":
                        msgParse.append("--end") # 終端引数を追加する
                    # 文字列が1つになっていない場合引数かどうかを確認する
                    if len(msgParse) >= 2 and not re.match(r"^(-[a-zA-Z]|--[a-zA-Z]+)$", msgParse[1]): # 引数の形になっていない場合
                        await message.channel.send("文字列は1つにまとめるようにしてください。複数の文字列の検索は正規表現を利用してください。")
                        return
                    else: # 引数の形だった場合
                        # 引数が正しいか判定する(変な引数は全部ここで弾かれる)
                        for arg in msgParse:
                            # 引数の形をしているが予約されていないものがあったらエラー
                            if re.match(r"^(-[a-zA-Z]|--[a-zA-Z]+)$", arg):
                                if arg not in ("-i", "-r", "-b", "-c", "--end"): # ここに最初の引数になる可能性のあるものを追加していく
                                    print(f"エラー: 引数{arg}は予約されていません")
                                    await message.channel.send("エラー: 無効な引数です: " + arg)
                                    return
                        # 第1引数[-s|-r|-n]
                        if msgParse[1] != "-i" and msgParse[1] != "-r":
                            msgParse.insert(1, "-n")
                        # 第2引数/第3引数[-c ***]
                        if msgParse[2] != "-c":
                            msgParse.insert(2, "-c")
                            msgParse.insert(3, "none")
                        # 第4引数[-b]
                        if msgParse[4] != "-b":
                            msgParse.insert(4, "--release")

                try:
                    res = itemSearch(msgParse[0], msgParse[1], msgParse[3], msgParse[4])
                    await message.channel.send(res)
                except discord.errors.HTTPException:
                    await message.channel.send("エラー: 検索結果が2000文字を超えているため表示できません。")
                except NoCategoryError:
                    await message.channel.send(f"エラー: {msgParse[3]}というカテゴリは存在しません。")
                except:
                    await self.errorWrite()
                finally:
                    return
        
        # ヘルプコマンド
        if message.content.startswith(commandHelp):
            helpMsg = textwrap.dedent(f"""
            **SOLD OUT 2 市場情報bot for Discord Version {DEFINE_VERSION}**

            このbotでは以下のコマンドが使用可能です。
            各コマンドのより詳細な情報は各コマンドに「ヘルプ」「help」などを引数として渡すと閲覧可能です。
            ただし、一部のコマンドについてはヘルプが存在しません。

            {commandMarket} [商品名] [-s|-r] [-t 街名] [-b]
            {commandAlias} [add|delete] [エイリアス名] [正式名称]
            {commandAlias} [show]
            {commandSearch} [文字列もしくは正規表現] [-i|-r] [-c カテゴリ名] [-b]
            {commandVersion}
            {commandShutdown}
            {commandWiki} [アイテム名]
            """)
            await message.channel.send(helpMsg)
            return

        # Wikiコマンド
        if message.content.startswith(commandWiki):
            msgParse = message.content.split()
            # コマンドを削除
            del msgParse[0]
            # コマンド単体だった場合
            if len(msgParse) == 0:
                await self.showHelpWiki()
                return
            else:
                # ヘルプ表示の場合
                if re.match(r"([Hh][Ee][Ll][Pp]|[へヘﾍ][るルﾙ][ぷプﾌﾟ])", msgParse[0]):
                    await self.showHelpWiki()
                    return
                else:
                    try:
                        resmes = wikiLinkGen(msgParse[0])
                        await message.channel.send(resmes)
                    except:
                        await self.errorWrite()
                    finally:
                        return

        # エラー発生コマンド(仮)
        if message.content.startswith("!error"):
            try:
                res = 1 / 0 # ZeroDivisionError
                await message.channel.send(res)
            except:
                await self.errorWrite()
            finally:
                return
                

    async def showHelpMarket(self):
        helpMsg = textwrap.dedent(f"""
        市場に出ている商品・レシピ品の販売価格や注文価格などを調べることができます。
        使用方法: {commandMarket} [商品名] [-s|-r] [-t 街名] [-b]
        出力情報一覧: 
        ・販売
        　・最安値
        　・最高値
        　・最安TOP5平均
        　・全体平均
        　・中央値
        　・市場全体の個数
        　・販売店舗数
        ・注文
        　・最高値
        　・最安値
        　・最高TOP5平均
        　・全体平均
        　・中央値
        　・市場全体の注文数
        　・注文店舗数

        引数:
        -s: 販売品の情報のみを表示することができます。
        -r: 注文品の情報のみを表示することができます。
        -t 街名: 指定した街の情報のみを表示することができます。-s、-rとは併用可能です。
        -b: Beta版の市場情報を表示します。Beta版が開放されている時のみ使用可能です。
        
        {commandMarket} help(ヘルプ等でも可) でこのヘルプを表示することができます。
        """)
        await self.targetChannel.send(helpMsg)

    async def showHelpAlias(self):
        helpMsg = textwrap.dedent(f"""
        {commandMarket}で商品を指定したときに、登録されたエイリアスを正式名称に変換します。
        ・add
        　エイリアスを追加します。
        　使用方法: {commandAlias} add [エイリアス名] [正式名称]
        ・help
        　このヘルプを表示します。
        ・show
        　エイリアス一覧を表示します。
        """)
        await self.targetChannel.send(helpMsg)

    async def showHelpSearch(self):
        helpMsg = textwrap.dedent(f"""
        指定した単語や文字を含むアイテムを検索します。
        正規表現を使用することができます。
        使用方法: {commandSearch} [文字列もしくは正規表現] [-i|-r] [-c カテゴリ名] [-b]

        引数:
        -i: レシピ品を除くアイテムのみから検索することができます。
        -r: レシピ品のみから検索することができます。
        -c カテゴリ名: カテゴリ名を指定して検索することができます。
        -b: Beta版の情報を取得します。Beta版が開放されている時のみ使用可能です。
        """)
        await self.targetChannel.send(helpMsg)

    async def showHelpWiki(self):
        helpMsg = textwrap.dedent(f"""
        指定したアイテムのWikiページへのリンクを生成します。
        登録されたエイリアスが使用可能です。
        レシピ品のWikiページへのリンクは存在しないため生成できません。
        使用方法: {commandWiki} [アイテム名]
        """)
        await self.targetChannel.send(helpMsg)

    async def errorWrite(self):
        now = datetime.datetime.now(timezone(config["misc"]["timezone"]))
        nowFormat = now.strftime("%Y/%m/%d %H:%M:%S%z")
        nowFileFormat = now.strftime("%Y%m%d")
        os.makedirs("error-log", exist_ok=True)
        with open(f"error-log/{nowFileFormat}.txt", "a") as f:
            f.write(f"--- Datetime: {nowFormat} ---\n")
            traceback.print_exc(file=f)
            f.write("\n")
        traceback.print_exc()
        if config["misc"].getboolean("EnableDisplayError"):
            typeExc, valueExc, tracebackExc = sys.exc_info()
            tracebackList = traceback.format_exception(typeExc, valueExc, tracebackExc)
            await self.targetChannel.send("以下のエラーが発生しました。")
            await self.targetChannel.send(f"```{''.join(tracebackList)}```")
        else:
            await self.targetChannel.send("エラーが発生しました。bot管理者に問い合わせてください。")
