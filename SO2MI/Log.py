from configparser import ConfigParser
import datetime
import inspect
import sys

config = ConfigParser()
config.read("config.ini")

streamLevel = config["logs"]["streamLogLevel"]
fileLevel = config["logs"]["fileLogLevel"]

def logger(message, level="info"):
    """ログを出力します。

    引数:\n
        message(str): ログとして出力する内容です。
        level(str): ログレベルです。critical、error、warning、info、debugのいずれかを入力します。デフォルトはinfoです。

    返り値:\n
        str: メッセージの内容です。
    """
    if config["logs"].getboolean("enableLog"):
        # 時刻フォーマット
        nowtemp = datetime.datetime.now()
        now = nowtemp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-7]

        # メッセージフォーマット
        mes = f"[{now}] [{level}]: {message}"

        # 標準出力への書き込み
        if streamLevel == "debug":
            if level in ("debug", "info", "warning", "error", "critical"):
                print(mes)
        elif streamLevel == "info":
            if level in ("info", "warning", "error", "critical"):
                print(mes)
        elif streamLevel == "warning":
            if level in ("warning", "error", "critical"):
                print(mes)
        elif streamLevel == "error":
            if level in ("error", "critical"):
                print(mes)
        elif streamLevel == "critical":
            if level == "critical":
                print(mes)

        # ファイルへの書き込み
        if fileLevel == "debug":
            if level in ("debug", "info", "warning", "error", "critical"):
                with open("info.log", "a", encoding="utf-8_sig") as l:
                    l.write(mes + "\n")
        elif fileLevel == "info":
            if level in ("info", "warning", "error", "critical"):
                with open("info.log", "a", encoding="utf-8_sig") as l:
                    l.write(mes + "\n")
        elif fileLevel == "warning":
            if level in ("warning", "error", "critical"):
                with open("info.log", "a", encoding="utf-8_sig") as l:
                    l.write(mes + "\n")
        elif fileLevel == "error":
            if level in ("error", "critical"):
                with open("info.log", "a", encoding="utf-8_sig") as l:
                    l.write(mes + "\n")
        elif fileLevel == "critical":
            if level == "critical":
                with open("info.log", "a", encoding="utf-8_sig") as l:
                    l.write(mes + "\n")
