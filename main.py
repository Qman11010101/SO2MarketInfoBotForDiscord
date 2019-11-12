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

# Discordのトークンの書かれたconfigの読み込み
if os.path.isfile("config.ini"):
    config = configparser.ConfigParser()
    config.read("config.ini")
else:
    print("設定ファイルがありません。")
    sys.exit(1) # 異常終了

if __name__ == "__main__":
    # 実行
    dcCli = Client()
    dcCli.run(config["discord"]["token"])
