from discord.ext import commands

from SO2MI.config import CONFIG
from SO2MI.Log import logger
from SO2MI.Alias import addAlias, removeAlias, showAlias
from SO2MI.Exceptions import SameItemExistError, NoItemError, NameDuplicationError
from SO2MI.CogLib import chk_channel

class Alias(commands.Cog):
    def __init__(self, bot, channel):
        self.bot = bot
        self.channel_id = channel
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.bot.get_channel(self.channel_id)
        if self.channel == None:
            logger("botが実行されるチャンネルが見つかりませんでした", "critical")
            raise Exception("specified channel not found")

    @commands.command()
    @commands.check(chk_channel)
    async def alias(self, ctx, action=None, aliasName=None, *, realName=None):
        """
        エイリアスを追加・表示・削除ができます。

        action:
            add:
                エイリアスを追加します。
                [aliasName]にエイリアス名、[realName]に実際の商品を指定します。
            remove:
                エイリアスを削除します。
                [aliasName]にエイリアス名を指定します。
            list | show:
                エイリアス一覧を表示します。
        """
        if not CONFIG["misc"]["EnableAlias"]:
            logger("aliasコマンドは無効化されています")
            await ctx.send("このコマンドは管理者によって無効化されています。")
            return

        if action == None:
            await ctx.send("不明なアクションです。")
            return

        if action.lower() == "add":
            async with ctx.typing():
                try:
                    if aliasName == None or realName == None:
                        await ctx.send("引数が足りません。")
                    else:
                        addAlias(aliasName, realName)
                        await ctx.send(f"エイリアスを追加しました。\n{aliasName} → {realName}")
                except OSError:
                    logger("alias.jsonにアクセスできませんでした", "error")
                    await ctx.send("エラー: alias.jsonにアクセスできません。")
                except SameItemExistError:
                    await ctx.send("エラー: 既に登録されています。")
                except NoItemError:
                    await ctx.send(f"エラー: 「{realName}」は存在しません。")
                except NameDuplicationError:
                    await ctx.send(f"エラー: 「{aliasName}」というアイテムが既に存在しています。")
                finally:
                    return
        elif action.lower() == "remove":
            async with ctx.typing():
                try:
                    if aliasName == None:
                        await ctx.send("引数が足りません。")
                    else:
                        if removeAlias(aliasName):
                            await ctx.send("エイリアスを削除しました。")
                        else:
                            await ctx.send(f"エラー: 「{aliasName}」というエイリアス名は存在しません。")
                except OSError:
                    logger("alias.jsonにアクセスできませんでした", "error")
                    await ctx.send("エラー: alias.jsonにアクセスできません。")
                finally:
                    return
        elif action.lower() in ("show", "list"):
            async with ctx.typing():
                res = showAlias()
                if res == False:
                    logger("エイリアスは登録されていません")
                    await ctx.send("エイリアスは登録されていません。")
                    return
                else:
                    logger("エイリアス一覧を表示します")
                    await ctx.send(res)
                    return
        else:
            await ctx.send("不明なアクションです。")
