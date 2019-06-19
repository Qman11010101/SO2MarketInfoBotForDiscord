import discord
import configparser
import re
from pprint import pprint as pp

from .Parser import ItemParser

config = configparser.ConfigParser()
config.read("config.ini")

commandMarket = config["command"]["prefix"] + config["command"]["market"]

class Client(discord.Client):
    async def on_ready(self):
        # 設定されているチャンネルIDに接続
        self.targetChannel = self.get_channel(int(config["discord"]["channel"]))
        if self.targetChannel == None:
            # 指定チャンネルが見つからない場合はExceptionをraise
            raise Exception("指定されたチャンネルは見つかりませんでした")
        else:
            # await self.targetChannel.send("{0} is Ready!".format(self.user))
            pass
        print("次のユーザーとしてログインしました", self.user)

    async def on_message(self, message):
        if message.author.bot or message.author == self.user or int(config["discord"]["channel"]) != message.channel.id:
            # BOT属性アカウント, 自身のアカウント or 指定したチャンネル以外はスルー
            return

        # 内部処理はここから
        if message.content.startswith(commandMarket):
            msgParse = message.content.split()
            # コマンドを削除
            del msgParse[0]
            print("{0} => {1}".format(message.author, msgParse))
            if len(msgParse) == 0:
                await self.showHelpMarket()
            else:
                if re.match(r"([Hh][Ee][Ll][Pp]|[へヘﾍ][るルﾙ][ぷプﾌﾟ])", msgParse[0]):
                    await self.showHelpMarket()
                else:
                    # 2つ以上指定している場合は弾く
                    if len(msgParse) >= 2:
                        await message.channel.send("商品は1つのみを指定してください。")
                        return
                    
                    # Falseで返ってない場合はそのままチャットへ流す。Falseだった場合は見つからないと表示
                    arg = msgParse[0]
                    parseRes = ItemParser(arg)
                    if parseRes != False:
                        await message.channel.send(parseRes)
                    else:
                        await message.channel.send("{0}は見つかりませんでした。".format(arg))

    async def showHelpMarket(self):
        helpMsg = f"""
        SO2市場情報bot
        市場に出ている商品・レシピ品の販売価格や注文価格などを調べることができます。
        使用方法: {commandMarket} [商品名]
        出力情報一覧: 
        ・販売
        　・最安値
        　・最高値
        　・最安TOP5平均
        　・全体平均
        　・市場全体の個数
        ・注文
        　・最高値
        　・最安値
        　・最高TOP5平均
        　・全体平均
        　・市場全体の注文数
        
        {commandMarket} help(ヘルプ等でも可) でこのヘルプを表示することができます。
        """
        await self.targetChannel.send(helpMsg)
