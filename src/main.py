import asyncio
import discord
from src.config import MainConfig
from discord.ext import commands


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
        await self.load_extension("src.event.on_message")
        if MainConfig().get_config_data().get("discord", {}).get("mode", {}).get("slash"):
            await self.load_extension("src.command.ask")

    async def _start(self):
        if not self.token or self.token == "YOUR DISCORD BOT TOKEN HERE":
            raise ValueError("Token not found")

        async with self:
            await self.start(self.token)


if __name__ == '__main__':
    bot = App()
    asyncio.run(bot._start())