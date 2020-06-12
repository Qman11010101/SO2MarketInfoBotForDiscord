from discord.ext import commands

from SO2MI.Log import logger
from SO2MI.getApi import getApi
from SO2MI.Alias import alias
from SO2MI.Parser import itemParser
from SO2MI.Exceptions import NoTownError
from SO2MI.cog.lib import chk_channel
from SO2MI.Population import getPopulation

class Market(commands.Cog):
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
    async def population(self, ctx, town_name):
        try:
            async with ctx.typing():
                res = getPopulation(town_name)
        except NoTownError:
            await self.channel.send(f"エラー: 「{town_name}」という街は存在しません。")
        else:
            await self.channel.send(res)
