import discord
import configparser
import re
from pprint import pprint as pp

from .Parser import ItemParser

config = configparser.ConfigParser()
config.read('config.ini')

marketCmd = config['command']['PREFIX'] + config['command']['market']

class Client(discord.Client):
    async def on_ready(self):
        # 設定されているチャンネルIDに接続
        self.targetChannel = self.get_channel(int(config['discord']['channel']))
        if self.targetChannel == None:
            # 指定チャンネルが見つからない場合はExceptionをraise
            raise Exception('Specified discord channel is not found!')
        else:
            # await self.targetChannel.send("{0} is Ready!".format(self.user))
            pass
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author.bot or message.author == self.user or int(config['discord']['channel']) != message.channel.id:
            # BOT属性アカウント, 自身のアカウント or 指定したチャンネル以外はスルー
            return

        # 内部処理はここから
        if message.content.startswith(marketCmd):
            msgParse = message.content.split()
            # コマンドを削除
            del msgParse[0]
            print("{0} => {1}".format(message.author, msgParse))
            if len(msgParse) == 0:
                await self.showHelpMarket()
            else:
                if re.match(r'(ヘルプ|ﾍﾙﾌﾟ|へるぷ|[Hh][Ee][Ll][Pp])', msgParse[0]):
                    await self.showHelpMarket()
                else:
                    # 5つより多い場合は弾く
                    if len(msgParse) > 5:
                        await message.channel.send('リクエストする量が多すぎます。一度に最大5つまでリクエストできます。')
                        return
                    
                    # Falseで返ってない場合はそのままチャットへ流す。Falseだった場合は見つからないと表示
                    parseRes = None # for内のエラー回避用
                    for arg in msgParse:
                        parseRes = ItemParser(arg)
                        if parseRes != False:
                            await message.channel.send(parseRes)
                        else:
                            await message.channel.send('{0}は見つかりませんでした。'.format(arg))

    async def showHelpMarket(self):
        helpMsg = """
        marketコマンドの使い方
        ・ コマンドの後に空白を入れ、その後に商品名を入力すると市場情報を閲覧することができます。
        ・ コマンドの後にヘルプ（へるぷ、helpなども含む）と入力するとこのヘルプを見ることができます。
        """
        await self.targetChannel.send(helpMsg)
