import configparser
import json
import requests

config = configparser.ConfigParser()
config.read("config.ini")

user = config["misc"]["GitHubUserID"]
repo = config["misc"]["GitHubRepoName"]

def chkver():
    r = requests.get(f"https://api.github.com/repos/{user}/{repo}/releases/latest")
    with open(r, "r", encoding="utf-8_sig") as g:
        res = json.load(g)
    # 動かない
    versionName = res["name"]