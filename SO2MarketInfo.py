#!/usr/bin/env python3
"""

    SOLD OUT 2 Market Information Bot for Discord
    @author: Kjuman Enobikto & YuzuRyo61
    @license: MIT License

"""

import configparser

from SO2MI import Client

config = configparser.ConfigParser()
config.read('config.ini')

if __name__ == "__main__":
    # Run
    dcCli = Client()
    dcCli.run(config['discord']['token'])