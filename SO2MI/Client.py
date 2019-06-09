import discord
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class Client(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author.bot or message.author == self.user:
            # BOT属性アカウントはスルー
            return
