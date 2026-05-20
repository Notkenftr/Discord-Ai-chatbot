import discord
from src.context import Context
from src.config import MainConfig
from discord.ext import commands

from src.event.on_message import OnMessage
from src.command.ask import Ask

class App(commands.Bot):
    def __init__(self):
        self.config_data = MainConfig().get_config_data()
        discord_config = self.config_data.get("discord", {})

        prefix = discord_config.get("prefix", "!")
        self.token = discord_config.get("token", "")

        super().__init__(
            command_prefix=prefix,
            intents=discord.Intents.all()
        )

    async def setup_hook(self) -> None:
        from src.utils.logging import Logging

        Context().init().logging = Logging()

        await self.add_cog(OnMessage(self))

    async def on_ready(self) -> None:
        if MainConfig().get_config_data().get("discord", {}).get("mode", {}).get("slash_command",{}).get("enable",False):
            await self.add_cog(Ask(self))

        await self.tree.sync()
        logging = Context().logging
        logging.info("Bot is ready")

    async def _start(self):
        if not self.token or self.token == "YOUR DISCORD BOT TOKEN HERE":
            raise ValueError("Token not found")

        async with self:
            await self.start(self.token)

