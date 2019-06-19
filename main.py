#!/usr/bin/env python3
"""

    SOLD OUT 2 Market Information Bot for Discord
    @author: Kjuman Enobikto & YuzuRyo61
    @license: MIT License

"""

import configparser
import os
import sys

#Discordのトークンの書かれたconfigの読み込み
from SO2MI import Client

if os.path.isfile("config.ini"):
    config = configparser.ConfigParser()
    config.read("config.ini")
else:
    print("設定ファイルがありません。")
    sys.exit(1)    

if __name__ == "__main__":
    # Run
    dcCli = Client()
    dcCli.run(config["discord"]["token"])
