import configparser
import json
import os
import textwrap

import requests

from SO2MI.config import CONFIG as config
from SO2MI.Log import logger

user = config["misc"]["GitHubUserID"]
repo = config["misc"]["GitHubRepoName"]

def chkver(verstr):
    endpoint = f"https://api.github.com/repos/{user}/{repo}/releases/latest"
    logger(f"次のエンドポイントにアクセスしています: {endpoint}")
    r = requests.get(endpoint)
    res = json.loads(r.text)
    versionName = res["name"]
    verstr = f"Version {verstr}"
    resstr = textwrap.dedent(f"""
        **SOLD OUT 2 市場情報bot for Discord**

        製作者: キューマン・エノビクト、ゆずりょー
        ライセンス: MIT License
        リポジトリ: https://github.com/{user}/{repo}
        """)
    if versionName != verstr:
        resstr += textwrap.dedent(f"""
        現在のバージョン: {verstr}
        最新バージョン: {versionName}
        
        新しいバージョンが存在します。
        """)
    else:
        resstr += textwrap.dedent(f"""
        現在のバージョン: {verstr}
        最新バージョン: {versionName}

        このbotは最新バージョンです。
        """)

    return resstr
