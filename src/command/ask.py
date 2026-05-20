import discord
from src.config import MainConfig
from discord import app_commands
from discord.ext import commands
from src.handler.response_handler import ResponseHandler
from src.context import Context
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
        logging = Context().logging
        logging.info(f"Trigger Slash Command Author= {interaction.user.name} | response= {question}")
        response_handler: ResponseHandler = ResponseHandler(question)
        await response_handler.handler()
        response = response_handler.get_response()
        if response:
            logging.info(f"Reply Author= {interaction.user.name} | response= {response}")
            await interaction.followup.send(f"{interaction.user.mention} {response}")

