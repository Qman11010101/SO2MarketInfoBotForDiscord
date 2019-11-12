from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

fileLevel = config["logs"]["fileLogLevel"]

def logger(message, level="debug"):
    """ログを出力します。

    引数:\n
        message(str): ログとして出力する内容です。
        level(str): ログレベルです。critical、error、warning、info、debugの5段階のいずれかを入力します。デフォルトはdebugです。

    返り値:\n
        str: メッセージの内容です。
    """

    