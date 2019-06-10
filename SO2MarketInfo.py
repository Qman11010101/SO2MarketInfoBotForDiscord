#!/usr/bin/env python3
"""

    SOLD OUT 2 Market Information Bot for Discord
    @author: Kjuman Enobikto & YuzuRyo61
    @license: MIT License

"""

import configparser
import json
import urllib.request as urlreq

#トークンの書かれたconfigの読み込み
from SO2MI import Client
config = configparser.ConfigParser()
config.read('config.ini')

#販売品取得
url = "https://so2-api.mutoys.com/json/sale/all.json"
urlreq.urlretrieve(url, 'data/sale.json')

#注文品取得
url = "https://so2-api.mutoys.com/json/request/all.json"
urlreq.urlretrieve(url, 'data/req.json')

#JSONの読み込み
s = open("data/sale.json", "r", encoding="utf-8_sig")
r = open("data/req.json", "r", encoding="utf-8_sig")
sale = json.load(s)
req = json.load(r)


if __name__ == "__main__":
    # Run
    dcCli = Client()
    dcCli.run(config['discord']['token'])