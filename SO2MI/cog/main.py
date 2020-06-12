from discord.ext import commands

import SO2MI
from SO2MI.Alias import addAlias, alias, removeAlias, showAlias
from SO2MI.cog.lib import chk_channel
from SO2MI.config import CONFIG
from SO2MI.Exceptions import (NameDuplicationError, NoItemError, NoTownError,
                              SameItemExistError)
from SO2MI.getApi import getApi
from SO2MI.Log import logger
from SO2MI.Parser import itemParser
from SO2MI.Population import getPopulation
from SO2MI.Chkver import chkver


class Main(commands.Cog):
    def __init__(self, bot, channel):
        self.bot = bot
        self.channel_id = channel

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.bot.get_channel(self.channel_id)
        if self.channel == None:
            logger("botが実行されるチャンネルが見つかりませんでした", "critical")
            raise Exception("specified channel not found")
        else:
            logger(f"チャンネルID: {self.channel_id}", "debug")

    @commands.command()
    @commands.check(chk_channel)
    async def market(self, ctx, name=None, *options):
        """
        市場に出ている商品・レシピ品の販売価格や注文価格などを調べることができます。
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

        [name]:
        商品名を入力します。登録されているエイリアス名が使用できます。

        [options...]:
        -s: 販売品の情報のみを表示することができます。
        -r: 注文品の情報のみを表示することができます。
        -t=[街名]: 指定した街の情報のみを表示することができます。-s、-rとは併用可能です。
        -b: Beta版の市場情報を表示します。Beta版が開放されている時のみ使用可能です。
        """
        if name == None:
            await ctx.send(f"{ctx.message.author.mention} 商品名が指定されていません。")
            return

        logger(f"{ctx.message.author} が {name} をリクエストしました")

        # 入力中のサインを出す（こうすることで処理している表示ができる）
        async with ctx.typing():
            beta = True if "-b" in options else False
            try:
                msg = itemParser(name, beta, *options)
            except NoTownError:
                # 引数から街の名前を取得
                townName = None
                for arg in options:
                    if arg.startswith("-t="):
                        townName = arg.split("=", 1)[1]
                await ctx.send(f"「{townName}」という街は見つかりませんでした。")
            else:
                if msg == False:
                    await ctx.send(f"「{name}」は見つかりませんでした。")
                else:
                    await ctx.send(msg)

    @commands.command()
    @commands.check(chk_channel)
    async def alias(self, ctx, action=None, aliasName=None, *, realName=None):
        """
        エイリアスを追加・表示・削除ができます。

        action:
            add:
                エイリアスを追加します。
                [aliasName]にエイリアス名、[realName]に実際の商品を指定します。
            remove:
                エイリアスを削除します。
                [aliasName]にエイリアス名を指定します。
            list | show:
                エイリアス一覧を表示します。
        """
        if not CONFIG["misc"]["EnableAlias"]:
            logger("aliasコマンドは無効化されています")
            await ctx.send("このコマンドは管理者によって無効化されています。")
            return

        if action == None:
            await ctx.send("不明なアクションです。")
            return

        if action.lower() == "add":
            async with ctx.typing():
                try:
                    if aliasName == None or realName == None:
                        await ctx.send("引数が足りません。")
                    else:
                        addAlias(aliasName, realName)
                        await ctx.send(f"エイリアスを追加しました。\n{aliasName} → {realName}")
                except OSError:
                    logger("alias.jsonにアクセスできませんでした", "error")
                    await ctx.send("エラー: alias.jsonにアクセスできません。")
                except SameItemExistError:
                    await ctx.send("エラー: 既に登録されています。")
                except NoItemError:
                    await ctx.send(f"エラー: 「{realName}」は存在しません。")
                except NameDuplicationError:
                    await ctx.send(f"エラー: 「{aliasName}」というアイテムが既に存在しています。")
                finally:
                    return
        elif action.lower() == "remove":
            async with ctx.typing():
                try:
                    if aliasName == None:
                        await ctx.send("引数が足りません。")
                    else:
                        if removeAlias(aliasName):
                            await ctx.send("エイリアスを削除しました。")
                        else:
                            await ctx.send(f"エラー: 「{aliasName}」というエイリアス名は存在しません。")
                except OSError:
                    logger("alias.jsonにアクセスできませんでした", "error")
                    await ctx.send("エラー: alias.jsonにアクセスできません。")
                finally:
                    return
        elif action.lower() in ("show", "list"):
            async with ctx.typing():
                res = showAlias()
                if res == False:
                    logger("エイリアスは登録されていません")
                    await ctx.send("エイリアスは登録されていません。")
                    return
                else:
                    logger("エイリアス一覧を表示します")
                    await ctx.send(res)
                    return
        else:
            await ctx.send("不明なアクションです。")

    @commands.command()
    @commands.check(chk_channel)
    async def population(self, ctx, town_name):
        try:
            async with ctx.typing():
                res = getPopulation(town_name)
        except NoTownError:
            await self.channel.send(f"エラー: 「{town_name}」という街は存在しません。")
        else:
            await self.channel.send(res)

    @commands.command()
    @commands.check(chk_channel)
    async def version(self, ctx):
        # バージョンチェックコマンド
        async with ctx.typing():
            res = chkver(SO2MI.__version__)
            await ctx.send(res)

