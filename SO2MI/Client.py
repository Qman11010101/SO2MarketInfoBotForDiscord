import asyncio
import configparser
import datetime
import json
import os
import re
import sys
import textwrap
import traceback
from distutils.util import strtobool
from json.decoder import JSONDecodeError

import discord
from pytz import timezone

from .Alias import addAlias, removeAlias, showAlias
from .Chkver import chkver
from .Exceptions import (NameDuplicationError, NoCategoryError, NoItemError,
                         NoTownError, SameAliasNameExistError,
                         SameItemExistError)
from .Log import logger
from .Parser import itemParser
from .Population import getPopulation
from .Register import addRegister, removeRegister, showRegister
from .Regular import chkCost, chkEndOfMonth, chkEvent
from .Search import itemSearch
from .Shelf import getShelves
from .Wiki import wikiLinkGen

if os.path.isfile("config.ini"):
    config = configparser.ConfigParser()
    config.read("config.ini")

    prefix = config["command"]["prefix"]

    commandMarket = prefix + config["command"]["market"]
    commandAlias = prefix + config["command"]["alias"]
    commandVersion = prefix + config["command"]["version"]
    commandSearch = prefix + config["command"]["search"]
    commandHelp = prefix + config["command"]["help"]
    commandWiki = prefix + config["command"]["wiki"]
    commandRegister = prefix + config["command"]["register"]
    commandShelves = prefix + config["command"]["shelves"]
    commandPopulation = prefix + config["command"]["population"]
    commandChkver = prefix + config["command"]["chkver"]

    user = config["misc"]["GitHubUserID"]
    repo = config["misc"]["GitHubRepoName"]

    adminID = config["misc"]["administrator"]

    channel = config["discord"]["channel"]
    regChannel = config["discord"]["regChannel"]

    EnableRegularExecution = strtobool(
        config["misc"]["EnableRegularExecution"])
    EnableAlias = strtobool(config["misc"]["EnableAlias"])
    EnableDisplayError = strtobool(config["misc"]["EnableDisplayError"])

    RegExcCheckTime = config["misc"]["RegExcCheckTime"]
    RegExcHour = config["misc"]["RegExcHour"]
    RegExcMinute = config["misc"]["RegExcMinute"]
    RegEventDay = config["misc"]["RegEventDay"]

    tz = config["misc"]["timezone"]
else:
    prefix = os.environ.get("prefix")

    commandMarket = prefix + os.environ.get("market")
    commandAlias = prefix + os.environ.get("alias")
    commandVersion = prefix + os.environ.get("version")
    commandSearch = prefix + os.environ.get("search")
    commandHelp = prefix + os.environ.get("help")
    commandWiki = prefix + os.environ.get("wiki")
    commandRegister = prefix + os.environ.get("register")
    commandShelves = prefix + os.environ.get("shelves")
    commandPopulation = prefix + os.environ.get("population")
    commandChkver = prefix + os.environ.get("chkver")

    user = os.environ.get("GitHubUserID")
    repo = os.environ.get("GitHubRepoName")

    adminID = os.environ.get("administrator")

    channel = os.environ.get("channel")
    regChannel = os.environ.get("regChannel")

    EnableRegularExecution = strtobool(
        os.environ.get("EnableRegularExecution"))
    EnableAlias = strtobool(os.environ.get("EnableAlias"))
    EnableDisplayError = strtobool(os.environ.get("EnableDisplayError"))

    RegExcCheckTime = os.environ.get("RegExcCheckTime")
    RegExcHour = os.environ.get("RegExcHour")
    RegExcMinute = os.environ.get("RegExcMinute")
    RegEventDay = os.environ.get("RegEventDay")

    tz = os.environ.get("timezone")

DEFINE_VERSION = "4.1"


class Client(discord.Client):
    async def on_ready(self):
        self.targetChannel = self.get_channel(int(channel))
        if self.targetChannel == None:
            logger("botが実行されるチャンネルが見つかりませんでした", "critical")
            raise Exception("specified channel not found")
        else:
            pass
        self.regChannel = self.get_channel(int(regChannel))
        if self.regChannel == None:
            logger("定期実行サービスが実行されるチャンネルが見つかりませんでした", "critical")
            raise Exception("specified channel not found")
        else:
            pass
        logger(f"次のユーザーとしてログインしました: {self.user}")
        logger(f'bot実行チャンネルID: {channel}', "debug")
        logger(f'定期実行チャンネルID: {regChannel}', "debug")

        # 定期実行
        if EnableRegularExecution:
            logger("定期実行サービスはオンになっています")
            chkTime = int(RegExcCheckTime)
            while True:
                now = datetime.datetime.now(timezone(tz))

                startHour = int(RegExcHour)
                startMin = int(RegExcMinute)
                endMin = startMin + chkTime

                if now.hour == startHour and startMin <= now.minute <= endMin:
                    logger("定期実行サービスを実行します")
                    await self.cliChkCost()
                    await self.cliChkEndOfMonth()
                    await self.cliChkEvent()
                    await asyncio.sleep(50000)
                await asyncio.sleep(chkTime * 60)

    async def on_message(self, message):
        if message.author.bot or message.author == self.user or int(channel) != message.channel.id:
            return
        else:
            logger(f"{message.author} が入力しました: {message.content}")

        # コマンド受取部
        # 市場情報コマンド
        if message.content.startswith(commandMarket):
            msgParse = message.content.split()
            del msgParse[0]

            if len(msgParse) == 0:
                await self.showHelpMarket()
                return
            else:
                if re.match(r"([Hh][Ee][Ll][Pp]|[へヘﾍ][るルﾙ][ぷプﾌﾟ])", msgParse[0]):
                    await self.showHelpMarket()
                    return
                # 商品名が1つの場合
                elif len(msgParse) == 1:
                    # 「[商品名] -n -t none --release --end」というコマンド文字列を生成する
                    msgParse.extend(["-n", "-t", "none", "--release", "--end"])
                else:
                    if msgParse[-1] != "--end":
                        msgParse.append("--end")  # 終端引数を追加する
                    # 商品名が1つになっていない場合引数かどうかを確認する
                    if len(msgParse) >= 2 and not re.match(r"^(-[a-zA-Z]|--[a-zA-Z]+)$", msgParse[1]):
                        await message.channel.send("エラー: 同時に複数の商品を指定することはできません。")
                        return
                    else:  # 引数の形だった場合
                        # 引数が正しいか判定する(変な引数は全部ここで弾かれる)
                        for arg in msgParse:
                            # 引数の形をしているが予約されていないものがあったらエラー
                            if re.match(r"^(-[a-zA-Z]|--[a-zA-Z]+)$", arg):
                                # ここに最初の引数になる可能性のあるものを追加していく
                                if arg not in ("-s", "-r", "-t", "-b", "--end"):
                                    logger(f"引数{arg}は予約されていません", "info")
                                    await message.channel.send("エラー: 無効な引数です: " + arg)
                                    return
                        # 第1引数[-s|-r|-n]
                        if msgParse[1] not in ("-s", "-r"):
                            msgParse.insert(1, "-n")
                        # 第2引数/第3引数[-t ***]
                        if msgParse[2] != "-t":
                            msgParse.insert(2, "-t")
                            msgParse.insert(3, "none")
                        else:  # [-t]のときの処理
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
                    logger(f"{message.author} が {msgParse[0]} をリクエストしました")
                    parseRes = itemParser(
                        msgParse[0], msgParse[1], msgParse[3], msgParse[4])
                    if parseRes != False:
                        await message.channel.send(parseRes)
                    else:
                        await message.channel.send(f"「{msgParse[0]}」は見つかりませんでした。")
                except NoTownError:
                    await message.channel.send(f"エラー: 「{msgParse[3]}」という街は見つかりませんでした。")
                except:
                    await self.errorWrite()
                finally:
                    return

        # エイリアスコマンド
        if message.content.startswith(commandAlias):
            if EnableAlias:
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
                            使用方法: `{commandAlias} add [エイリアス名] [正式名称]`
                            """)
                            await message.channel.send(helpMsg)
                            return

                        try:
                            addAlias(msgParse[1], msgParse[2])
                        except OSError:
                            logger("alias.jsonにアクセスできませんでした", "error")
                            await message.channel.send("エラー: alias.jsonにアクセスできません。")
                        except SameItemExistError:
                            await message.channel.send("エラー: 既に登録されています。")
                        except NoItemError:
                            await message.channel.send(f"エラー: 「{msgParse[2]}」は存在しません。")
                        except NameDuplicationError:
                            await message.channel.send(f"エラー: 「{msgParse[1]}」というアイテムが既に存在しています。")
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
                            使用方法: `{commandAlias} remove [エイリアス名]`
                            """)
                            await message.channel.send(helpMsg)
                            return

                        try:
                            if removeAlias(msgParse[1]):
                                await message.channel.send("エイリアスを削除しました。")
                            else:
                                await message.channel.send(f"エラー: 「{msgParse[1]}」というエイリアス名は存在しません。")
                        except OSError:
                            logger("alias.jsonにアクセスできませんでした", "error")
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
                            logger("エイリアスは登録されていません")
                            await message.channel.send("エイリアスは登録されていません。")
                            return
                        else:
                            logger("エイリアス一覧を表示します")
                            await message.channel.send(res)
                            return

                    else:
                        await message.channel.send("エラー: コマンドが無効です。")
                        return
            else:
                logger("コマンドが無効化されています")
                await message.channel.send("このコマンドは管理者によって無効化されています。")
                return

        # バージョンコマンド
        if message.content.startswith(commandVersion):
            verMsg = textwrap.dedent(f"""
            **SOLD OUT 2 市場情報bot for Discord**

            Version {DEFINE_VERSION}
            製作者: キューマン・エノビクト、ゆずりょー
            ライセンス: MIT License
            リポジトリ: https://github.com/{user}/{repo}
            """)
            await message.channel.send(verMsg)
            return

        # アイテム検索コマンド
        if message.content.startswith(commandSearch):
            msgParse = message.content.split()
            del msgParse[0]

            if len(msgParse) == 0:
                await self.showHelpSearch()
                return
            else:
                if re.match(r"([Hh][Ee][Ll][Pp]|[へヘﾍ][るルﾙ][ぷプﾌﾟ])", msgParse[0]):
                    await self.showHelpSearch()
                    return
                elif len(msgParse) == 1:  # 検索文字列単体
                    msgParse.extend(["-n", "-c", "none", "--release", "--end"])
                else:
                    if msgParse[-1] != "--end":
                        msgParse.append("--end")  # 終端引数を追加する
                    # 文字列が1つになっていない場合引数かどうかを確認する
                    if len(msgParse) >= 2 and not re.match(r"^(-[a-zA-Z]|--[a-zA-Z]+)$", msgParse[1]):
                        await message.channel.send("文字列は1つにまとめるようにしてください。複数の文字列の検索は正規表現を利用してください。")
                        return
                    else:  # 引数の形だった場合
                        # 引数が正しいか判定する(変な引数は全部ここで弾かれる)
                        for arg in msgParse:
                            # 引数の形をしているが予約されていないものがあったらエラー
                            if re.match(r"^(-[a-zA-Z]|--[a-zA-Z]+)$", arg):
                                # ここに最初の引数になる可能性のあるものを追加していく
                                if arg not in ("-i", "-r", "-b", "-c", "--end"):
                                    logger(f"エラー: 引数{arg}は予約されていません")
                                    await message.channel.send("エラー: 無効な引数です: " + arg)
                                    return
                        # 第1引数[-s|-r|-n]
                        if msgParse[1] not in ("-i", "-r"):
                            msgParse.insert(1, "-n")
                        # 第2引数/第3引数[-c ***]
                        if msgParse[2] != "-c":
                            msgParse.insert(2, "-c")
                            msgParse.insert(3, "none")
                        # 第4引数[-b]
                        if msgParse[4] != "-b":
                            msgParse.insert(4, "--release")

                try:
                    mes = itemSearch(
                        msgParse[0], msgParse[1], msgParse[3], msgParse[4])
                    for i in range(len(mes)):
                        await message.channel.send(mes[i])
                except discord.errors.HTTPException:
                    await message.channel.send("エラー: 検索結果が2000文字を超えているため表示できません。")
                except NoCategoryError:
                    await message.channel.send(f"エラー: 「{msgParse[3]}」というカテゴリは存在しません。")
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
            また、一部のコマンドは管理者によって無効化されている可能性があります。

            `{commandMarket} [商品名] [-s|-r] [-t 街名] [-b]`
            `{commandAlias} [add|delete] [エイリアス名] [正式名称]`
            `{commandAlias} [show]`
            `{commandSearch} [文字列もしくは正規表現] [-i|-r] [-c カテゴリ名] [-b]`
            `{commandVersion}`
            `{commandWiki} [アイテム名]`
            `{commandRegister} [add|remove] [アイテム名]`
            `{commandRegister} [show]`
            `{commandShelves} [街名]`
            `{commandPopulation} [街名]`
            `{commandChkver}`
            """)
            await message.channel.send(helpMsg)
            return

        # Wikiコマンド
        if message.content.startswith(commandWiki):
            msgParse = message.content.split()
            del msgParse[0]

            if len(msgParse) == 0:
                await self.showHelpWiki()
                return
            else:
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

        # 登録コマンド
        if message.content.startswith(commandRegister):
            if EnableRegularExecution:
                msgParse = message.content.split()
                del msgParse[0]
                if len(msgParse) == 0:
                    await self.showHelpRegister()
                    return
                else:
                    if msgParse[0] == "add":
                        if len(msgParse) != 2:
                            helpMsg = textwrap.dedent(f"""
                            アイテムを登録します。
                            使用方法: `{commandRegister} add [アイテム名]`
                            """)
                            await message.channel.send(helpMsg)
                            return

                        try:
                            res = addRegister(msgParse[1])
                        except OSError:
                            logger("itemreg.jsonにアクセスできませんでした", "error")
                            await message.channel.send("エラー: itemreg.jsonにアクセスできません。")
                        except SameItemExistError:
                            await message.channel.send("エラー: 既に登録されています。")
                        except NoItemError:
                            await message.channel.send(f"エラー: 「{msgParse[1]}」は存在しません。")
                        except:
                            await self.errorWrite()
                        else:
                            await message.channel.send(f"「{res}」を登録しました。")
                        finally:
                            return

                    elif msgParse[0] == "remove":
                        if len(msgParse) != 2:
                            helpMsg = textwrap.dedent(f"""
                            アイテムを削除します。
                            使用方法: `{commandRegister} remove [アイテム名]`
                            """)
                            await message.channel.send(helpMsg)
                            return

                        try:
                            res = removeRegister(msgParse[1])
                            if res:
                                await message.channel.send(f"「{res}」を削除しました。")
                            else:
                                await message.channel.send(f"エラー: 「{msgParse[1]}」というアイテムは登録されていません。")
                        except OSError:
                            logger("itemreg.jsonにアクセスできませんでした", "error")
                            await message.channel.send("エラー: itemreg.jsonにアクセスできません。")
                        except:
                            await self.errorWrite()
                        finally:
                            return

                    elif msgParse[0] == "show":
                        res = showRegister()
                        if res == False:
                            await message.channel.send("アイテムは登録されていません。")
                            return
                        else:
                            await message.channel.send(res)
                            return

                    elif re.match(r"([Hh][Ee][Ll][Pp]|[へヘﾍ][るルﾙ][ぷプﾌﾟ])", msgParse[0]):
                        await self.showHelpRegister()
                        return

                    else:
                        await message.channel.send("エラー: コマンドが無効です。")
                        return
            else:
                await message.channel.send("このコマンドは管理者によって無効化されています。")
                return

        # 街販売額・販売棚数コマンド
        if message.content.startswith(commandShelves):
            msgParse = message.content.split()
            del msgParse[0]
            if len(msgParse) == 0:
                msgParse.append("--all")
            if re.match(r"([Hh][Ee][Ll][Pp]|[へヘﾍ][るルﾙ][ぷプﾌﾟ])", msgParse[0]):
                await self.showHelpShelves()
                return
            else:
                try:
                    res = getShelves(msgParse[0])
                except NoTownError:
                    await message.channel.send(f"エラー: 「{msgParse[0]}」という街は存在しません。")
                except:
                    await self.errorWrite()
                else:
                    await message.channel.send(res)
                finally:
                    return

        # 人口コマンド
        if message.content.startswith(commandPopulation):
            msgParse = message.content.split()
            del msgParse[0]
            if len(msgParse) == 0:
                await self.showHelpPopulation()
                return
            else:
                if re.match(r"([Hh][Ee][Ll][Pp]|[へヘﾍ][るルﾙ][ぷプﾌﾟ])", msgParse[0]):
                    await self.showHelpPopulation()
                    return
                else:
                    try:
                        res = getPopulation(msgParse[0])
                    except NoTownError:
                        await message.channel.send(f"エラー: 「{msgParse[0]}」という街は存在しません。")
                    except:
                        await self.errorWrite()
                    else:
                        await message.channel.send(res)
                    finally:
                        return

        # バージョンチェックコマンド
        if message.content.startswith(commandChkver):
            try:
                res = chkver(DEFINE_VERSION)
            except:
                await self.errorWrite()
            else:
                await message.channel.send(res)
            finally:
                return

    # ヘルプ等関数定義
    async def showHelpMarket(self):
        logger("helpを返します", "debug")
        helpMsg = textwrap.dedent(f"""
        市場に出ている商品・レシピ品の販売価格や注文価格などを調べることができます。
        使用方法: `{commandMarket} [商品名] [-s|-r] [-t 街名] [-b]`
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

        `{commandMarket} help`(ヘルプ等でも可) でこのヘルプを表示することができます。
        """)
        await self.targetChannel.send(helpMsg)

    async def showHelpAlias(self):
        logger("helpを返します", "debug")
        helpMsg = textwrap.dedent(f"""
        `{commandMarket}`で商品を指定したときに、登録されたエイリアスを正式名称に変換します。
        ・add
        　エイリアスを追加します。
        　使用方法: `{commandAlias} add [エイリアス名] [正式名称]`
        ・remove
        　エイリアスを削除します。
        　使用方法: `{commandAlias} remove [エイリアス名]`
        ・show
        　エイリアス一覧を表示します。
        ・help
        　このヘルプを表示します。
        """)
        await self.targetChannel.send(helpMsg)

    async def showHelpSearch(self):
        logger("helpを返します", "debug")
        helpMsg = textwrap.dedent(f"""
        指定した単語や文字を含むアイテムを検索します。
        正規表現を使用することができます。
        使用方法: `{commandSearch} [文字列もしくは正規表現] [-i|-r] [-c カテゴリ名] [-b]`

        引数:
        -i: レシピ品を除くアイテムのみから検索することができます。
        -r: レシピ品のみから検索することができます。
        -c カテゴリ名: カテゴリ名を指定して検索することができます。
        -b: Beta版の情報を取得します。Beta版が開放されている時のみ使用可能です。
        """)
        await self.targetChannel.send(helpMsg)

    async def showHelpWiki(self):
        logger("helpを返します", "debug")
        helpMsg = textwrap.dedent(f"""
        指定したアイテムのWikiページへのリンクを生成します。
        登録されたエイリアスが使用可能です。
        レシピ品のWikiページへのリンクは存在しないため生成できません。
        使用方法: `{commandWiki} [アイテム名]`
        """)
        await self.targetChannel.send(helpMsg)

    async def showHelpRegister(self):
        logger("helpを返します", "debug")
        helpMsg = textwrap.dedent(f"""
        定期実行が有効な際、価格を投稿するアイテムを登録したり削除したりできます。
        登録されたエイリアスが使用可能です。
        ・add
        　アイテムを登録します。
        　使用方法: `{commandRegister} add [アイテム名]`
        ・remove
        　アイテムを削除します。
        　使用方法: `{commandRegister} remove [アイテム名]`
        ・show
        　登録されたアイテムの一覧を表示します。
        ・help
        　このヘルプを表示します。
        """)
        await self.targetChannel.send(helpMsg)

    async def showHelpShelves(self):
        logger("helpを返します", "debug")
        helpMsg = textwrap.dedent(f"""
        指定された街の、現時点での販売棚数や販売額の合計を表示します。
        街名が指定されなかった場合は市場全体の情報が表示されます。
        使用方法: `{commandShelves} [街名]`
        """)
        await self.targetChannel.send(helpMsg)

    async def showHelpPopulation(self):
        logger("helpを返します", "debug")
        helpMsg = textwrap.dedent(f"""
        指定された街の、現時点での人口を表示します。
        使用方法: `{commandPopulation} [街名]`
        """)
        await self.targetChannel.send(helpMsg)

    # エラーログ出力関数
    async def errorWrite(self):
        now = datetime.datetime.now(timezone(tz))
        nowFormat = now.strftime("%Y/%m/%d %H:%M:%S%z")
        nowFileFormat = now.strftime("%Y%m%d")
        os.makedirs("error-log", exist_ok=True)
        with open(f"error-log/{nowFileFormat}.txt", "a") as f:
            f.write(f"--- Datetime: {nowFormat} ---\n")
            traceback.print_exc(file=f)
            f.write("\n")
        traceback.print_exc()
        if EnableDisplayError:
            typeExc, valueExc, tracebackExc = sys.exc_info()
            tracebackList = traceback.format_exception(
                typeExc, valueExc, tracebackExc)
            await self.targetChannel.send("以下のエラーが発生しました。")
            tracebackStr = "".join(tracebackList)
            if len(tracebackStr) <= 1900:
                await self.targetChannel.send(f"```{tracebackStr}```")
            else:
                await self.targetChannel.send("エラーが2000文字を超えているため表示できません。bot管理者に問い合わせてください。")
        else:
            await self.targetChannel.send("エラーが発生しました。bot管理者に問い合わせてください。")

    # 定期実行系関数定義
    async def cliChkCost(self):
        res = chkCost()
        if res != False:
            await self.regChannel.send(res)
        else:
            pass

    async def cliChkEndOfMonth(self):
        res = chkEndOfMonth()
        if res != False:
            await self.regChannel.send(res)
        else:
            pass

    async def cliChkEvent(self):
        res = chkEvent()
        if res != False:
            await self.regChannel.send(res)
        else:
            pass
