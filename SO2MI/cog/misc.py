import textwrap

from discord.ext import commands

import SO2MI
from SO2MI.Log import logger
from SO2MI.Chkver import chkver
from SO2MI.cog.lib import chk_channel

class Misc(commands.Cog):
    def __init__(self, bot, channel):
        self.bot = bot
        self.channel_id = channel
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.bot.get_channel(self.channel_id)
        if self.channel == None:
            logger("botが実行されるチャンネルが見つかりませんでした", "critical")
            raise Exception("specified channel not found")
    
    @commands.command()
    @commands.check(chk_channel)
    async def version(self, ctx):
        # バージョンチェックコマンド
        async with ctx.typing():
            res = chkver(SO2MI.__version__)
            await ctx.send(res)
