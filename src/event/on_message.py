import discord
from discord.ext import commands
from src.context import Context
from src.config import MainConfig
from src.handler.response_handler import ResponseHandler
class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.config: dict = MainConfig().get_config_data()
        self.logging = Context().logging
        self.mode = self.config.get("discord",{}).get("mode",{})

    async def response(self, message: discord.Message):
        self.logging.info(
            f"Trigger author={message.author} | content={message.content}"
        )

        response_handler: ResponseHandler = ResponseHandler(message.content)
        await response_handler.handler()
        response = response_handler.get_response(filter=True)

        if response:
            self.logging.info(
                f"Reply author={message.author} | response={response}"
            )

            await message.reply(response)
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user or message.author.bot:
            return
        if self.mode.get("always_reply"):
            await self.response(message)

        elif self.mode.get("on_mention"):
            if self.bot.user.mentioned_in(message):
                await self.response(message)
        elif self.mode.get("on_prefix"):
            if message.content.startswith(self.config.get("discord",{}).get("prefix","!")):
                await self.response(message)
            else:
                return
        else:
            return
