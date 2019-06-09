#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

    SOLD OUT 2 Market Information Bot for Discord
    @author: Kjuman Enobikto & YuzuRyo61
    @license: MIT License
    
"""

import configparser
import json
import urllib.request as urlreq

from SO2MI import Client #トークンの書かれたconfigの読み込み
config = configparser.ConfigParser()
config.read('config.ini')

if __name__ == "__main__":
    # Run
    dcCli = Client()
    dcCli.run(config['discord']['token'])