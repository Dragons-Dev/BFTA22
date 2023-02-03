import discord
from discord.ext import commands

import config
from utils import db


class BFTA22(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.not_ready = True
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        if self.not_ready:
            print("Bot ist online")
            await db.setup()


bot = BFTA22(
    command_prefix=commands.when_mentioned_or("BFTA"),
    case_insensitive=True,
    strip_after_prefix=True,
    intents=discord.Intents.all(),
    activity=discord.Activity(type=discord.ActivityType.watching, name="you"),
    state=discord.Status.online,
    debug_guilds = config.GUILD,
)


bot.load_extensions("cogs", recursive = True)
bot.run(config.TOKEN)
