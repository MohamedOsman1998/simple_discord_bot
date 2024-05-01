from .old_message_deleter import OldMessageDeleter
import dotenv

import discord
from .async_client import MyClient
import os

dotenv.load_dotenv('.env')

async def setup(bot):
    await bot.add_cog(OldMessageDeleter(bot))
