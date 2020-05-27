import os
import configparser
from distutils.util import strtobool

if os.path.isfile("config.ini"):
    CONFIG = configparser.ConfigParser()
    CONFIG.read("config.ini")
else:
    CONFIG = {}
    CONFIG["discord"]["token"] = os.environ.get("token")
    CONFIG["discord"]["channel"] = os.environ.get("channel")
    CONFIG["discord"]["regChannel"] = os.environ.get("regChannel")
    CONFIG["command"]["prefix"] = os.environ.get("prefix")
    CONFIG["misc"]["GitHubUserID"] = os.environ.get("GitHubUserID")
    CONFIG["misc"]["GitHubRepoName"] = os.environ.get("GitHubRepoName")
    CONFIG["misc"]["EnableAlias"] = os.environ.get("EnableAlias", True)
    CONFIG["misc"]["EnableRegularExecution"] = os.environ("EnableRegularExecution", False)
    CONFIG["logs"]["loglevel"] = os.environ.get("loglevel")
    CONFIG["logs"]["enableLog"] = strtobool(os.environ.get("enableLog"))
