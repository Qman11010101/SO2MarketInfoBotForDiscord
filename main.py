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
from SO2MI.cog import command, schedule

# bot初期化
bot = commands.Bot(command_prefix=CONFIG["command"]["prefix"])

# チャンネル変数初期化
if CONFIG["discord"]["channel"] == None:
    logger("bot実行チャンネルが登録されていません", "critical")
    sys.exit(1)
try:
    mainChannel = int(CONFIG["discord"]["channel"])
except TypeError:
    logger("bot実行チャンネルが正しく指定されていません", "critical")
    sys.exit(1)

if CONFIG["misc"]["EnableRegularExecution"]:
    try:
        regChannel = int(CONFIG["discord"]["regChannel"])
    except TypeError:
        logger("bot定期実行チャンネルが正しく指定されていません", "critical")
        sys.exit(1)
else:
    regChannel = None

@bot.event
async def on_ready():
    logger(f"次のユーザーとしてログインしました: {bot.user}")

    if CONFIG["misc"]["EnableRegularExecution"]:
        regCh = bot.get_channel(regChannel)
        if regCh == None:
            logger("定期実行サービスが実行されるチャンネルが見つかりませんでした")

if __name__ == "__main__":
    # トークンの確認
    if CONFIG["discord"]["token"] == None:
        logger("Discordのbotトークンが見つかりませんでした", "critical")
        raise Exception("Discord bot token not found")
    
    # cogへのコマンドの登録
    bot.add_cog(command.Mainframe(bot, mainChannel))
    if CONFIG["misc"]["EnableRegularExecution"]:
        bot.add_cog(schedule.Schedule(bot, regChannel))

    # 実行
    bot.run(CONFIG["discord"]["token"])
