import discord
from src.config import MainConfig
from discord import app_commands
from discord.ext import commands
from src.handler.response_handler import ResponseHandler

class Ask(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name=str(MainConfig().get_config_data()
                                   .get("discord",{})
                                   .get("mode",{})
                                   .get("slash_command")
                                   .get("name","ask")),
                          description=str(MainConfig().get_config_data()
                                   .get("discord",{})
                                   .get("mode",{})
                                   .get("slash_command")
                                   .get("description","Ask a question to the bot")))
    @app_commands.describe(question=str(MainConfig().get_config_data()
                                   .get("discord",{})
                                   .get("mode",{})
                                   .get("slash_command")
                                   .get("question_placeholder","Ask your question")))
    async def ask(self, interaction: discord.Interaction, question: str):
        await interaction.response.defer(thinking=True)
        response_handler: ResponseHandler = ResponseHandler(question)
        response = response_handler.get_response()
        if response:
            await interaction.followup.send(f"{interaction.user.mention} {response}")