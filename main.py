#!/usr/bin/env python3
"""

    SOLD OUT 2 Market Information Bot for Discord
    @author: Kjuman Enobikto & YuzuRyo61
    @license: MIT License

"""

import configparser
import os
import sys

from discord.ext import commands

from SO2MI.config import CONFIG
from SO2MI.Log import logger
from SO2MI.cog import Market, Alias, Misc, Schedule

# bot初期化
bot = commands.Bot(command_prefix=CONFIG["command"]["prefix"])

@bot.event
async def on_ready():
    regChannel = bot.get_channel(int(CONFIG["discord"]["regChannel"]))
    if regChannel == None:
        logger("定期実行サービスが実行されるチャンネルが見つかりませんでした", "warning")
        raise Exception("specified channel not found")
    logger(f"次のユーザーとしてログインしました: {bot.user}")

if __name__ == "__main__":
    if CONFIG["discord"]["token"] == None:
        raise Exception("トークンがありません。")
    # cogモジュール
    mainChannel = int(CONFIG["discord"]["channel"])
    bot.add_cog(Market(bot, mainChannel))
    bot.add_cog(Alias(bot, mainChannel))
    bot.add_cog(Misc(bot, mainChannel))
    if CONFIG["misc"]["EnableRegularExecution"]:
        bot.add_cog(Schedule(bot, int(CONFIG["discord"]["regChannel"])))
    bot.run(CONFIG["discord"]["token"])
