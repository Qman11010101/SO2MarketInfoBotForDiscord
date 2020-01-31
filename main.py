#!/usr/bin/env python3
"""

    SOLD OUT 2 Market Information Bot for Discord
    @author: Kjuman Enobikto & YuzuRyo61
    @license: MIT License

"""

import configparser
import os
import sys

from SO2MI import Client
from SO2MI.Log import logger

# Discordのトークンの読み込み
if os.path.isfile("config.ini"):
    config = configparser.ConfigParser()
    config.read("config.ini")

    token = config["discord"]["token"]
else:
    logger("config.iniが存在しないため、環境変数から値を読み取ります")
    token = os.environ.get("token")
    if token == None:
        logger("トークンが存在しません", "critical")
        sys.exit(1)

if __name__ == "__main__":
    # 実行
    dcCli = Client()
    dcCli.run(token)
