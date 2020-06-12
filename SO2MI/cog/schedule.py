from datetime import datetime

from discord.ext import commands, tasks

from SO2MI.config import CONFIG
from SO2MI.Log import logger
from SO2MI.Regular import chkCost, chkEndOfMonth, chkEvent

class Schedule(commands.Cog):
    def __init__(self, bot, channel_id):
        self.bot = bot
        self.regChannel_id = channel_id

    @commands.Cog.listener()
    async def on_ready(self):
        self.regChannel = self.bot.get_channel(self.regChannel_id)
        if self.regChannel == None:
            logger("定期実行サービスが実行されるチャンネルが見つかりませんでした", "critical")
            raise Exception("specified channel not found")

        logger(f'定期実行チャンネルID: {self.regChannel_id}', "debug")
        logger("定期実行サービスはオンになっています")

        self.loop.start() # pylint: disable=no-member

    # 1分に1回実行するけどまだ動作保証なし。
    @tasks.loop(seconds=60)
    async def loop(self):
        now = datetime.now().strftime('%H:%M')
        if now == '07:00':
            await self._cliChkCost()
            await self._cliChkEndOfMonth()
            await self._cliChkEvent()

    # 定期実行系関数定義
    async def _cliChkCost(self):
        async with self.regChannel.typing():
            res = chkCost()
            if res != None:
                await self.regChannel.send(res)

    async def _cliChkEndOfMonth(self):
        async with self.regChannel.typing():
            res = chkEndOfMonth()
            if res != False:
                await self.regChannel.send(res)

    async def _cliChkEvent(self):
        async with self.regChannel.typing():
            res = chkEvent()
            if res != False:
                await self.regChannel.send(res)
