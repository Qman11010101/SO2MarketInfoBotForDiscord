from discord.ext import commands

from SO2MI.Log import logger
from SO2MI.getApi import getApi
from SO2MI.Alias import alias
from SO2MI.Parser import itemParser
from SO2MI.Exceptions import NoTownError

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
    async def market(self, ctx, name=None, *options):
        if ctx.message.channel.id != self.channel_id:
            logger("channel does not match", "debug")
            return
        
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
