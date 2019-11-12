from configparser import ConfigParser
import datetime
import sys
import logging

config = ConfigParser()
config.read("config.ini")

LOGGER = logging.getLogger("SO2MIBOT")
LOGFORMAT = logging.Formatter("[%(asctime)s][%(levelname)-7s]: %(message)s")

if config["logs"]["logLevel"] == "debug":
    logLevel = logging.DEBUG
elif config["logs"]["logLevel"] == "info":
    logLevel = logging.INFO
elif config["logs"]["logLevel"] == "error":
    logLevel = logging.ERROR
elif config["logs"]["logLevel"] == "critical":
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
    if config["logs"].getboolean("enableLog"):
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
