import discord
from discord.ext import commands

class Help(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        self.no_category = "カテゴリ未指定"
        self.command_attrs["description"] = "コマンド一覧を表示します。"

    def command_not_found(self, string):
        return f"{string} というコマンドは見つかりませんでした。"

    async def send_bot_help(self,mapping):
        content = ""
        for cog in mapping:
            # 各コグのコマンド一覧を content に追加していく
            command_list = await self.filter_commands(mapping[cog])
            if not command_list:
                # 表示できるコマンドがないので、他のコグの処理に移る
                continue
            if cog is None:
                # コグが未設定のコマンドなので、no_category属性を参照する
                content += f"```\n{self.no_category}```"
            else:
                content += f"```\n{cog.qualified_name} / {cog.description}\n```"
            for command in command_list:
                content += f"`{command.name}` / {command.description}\n"
            content += "\n"
        embed = discord.Embed(title="コマンドリスト",
            description=content,color=0x00ff00)
        embed.set_footer(text=f"コマンドのヘルプ {self.context.prefix}help コマンド名")
        await self.get_destination().send(embed=embed)
