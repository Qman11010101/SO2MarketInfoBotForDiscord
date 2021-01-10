from configparser import ConfigParser
import datetime
from distutils.util import strtobool
import os
import sys
import logging

if os.path.isfile("config.ini"):
    config = ConfigParser()
    config.read("config.ini")
    settingLogLevel = config["logs"]["loglevel"]
    enableLog = strtobool(config["logs"]["enableLog"])
else:
    settingLogLevel = os.environ.get("loglevel")
    if (existEnableLog := os.environ.get("enableLog")) != None:
        enableLog = existEnableLog
    else:
        enableLog = True

LOGGER = logging.getLogger("SO2MIBOT")
LOGFORMAT = logging.Formatter("[%(asctime)s] %(levelname)-8s [%(module)s#%(funcName)s %(lineno)d]: %(message)s")

if settingLogLevel == "debug":
    logLevel = logging.DEBUG
elif settingLogLevel == "info":
    logLevel = logging.INFO
elif settingLogLevel == "error":
    logLevel = logging.ERROR
elif settingLogLevel == "critical":
    logLevel = logging.CRITICAL
else:
    logLevel = logging.WARNING

LOG_SH = logging.StreamHandler()
LOG_FH = logging.FileHandler("info.log")

LOGGER.setLevel(logLevel)

LOG_SH.setFormatter(LOGFORMAT)
LOGGER.addHandler(LOG_SH)

LOG_FH.setFormatter(LOGFORMAT)
LOGGER.addHandler(LOG_FH)

def logger(message, level="info"):
    """ログを出力します。

    引数:\n
        message(str): ログとして出力する内容です。
        level(str): ログレベルです。critical、error、warning、info、debugのいずれかを入力します。デフォルトはinfoです。

    返り値:\n
        str: メッセージの内容です。
    """
    if enableLog:
        if level == "debug":
            LOGGER.debug(message)
        elif level == "info":
            LOGGER.info(message)
        elif level == "warning":
            LOGGER.warning(message)
        elif level == "error":
            LOGGER.error(message)
        elif level == "critical":
            LOGGER.critical(message)
