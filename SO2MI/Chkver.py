import configparser
import json
import os
import textwrap

import requests

from .Log import logger

if os.path.isfile("config.ini"):
    config = configparser.ConfigParser()
    config.read("config.ini")

    user = config["misc"]["GitHubUserID"]
    repo = config["misc"]["GitHubRepoName"]
else:
    user = os.environ.get("GitHubUserID")
    repo = os.environ.get("GitHubRepoName")


def chkver(verstr):
    endpoint = f"https://api.github.com/repos/{user}/{repo}/releases/latest"
    logger(f"次のエンドポイントにアクセスしています: {endpoint}")
    r = requests.get(endpoint)
    res = json.loads(r.text)
    versionName = res["name"]
    verstr = f"Version {verstr}"
    if versionName != verstr:
        resstr = textwrap.dedent(f"""
        現在のバージョン: {verstr}
        最新バージョン: {versionName}
        
        新しいバージョンが存在します。
        """)
    else:
        resstr = textwrap.dedent(f"""
        現在のバージョン: {verstr}
        最新バージョン: {versionName}

        このbotは最新バージョンです。
        """)

    return resstr
