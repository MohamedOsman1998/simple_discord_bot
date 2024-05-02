import discord
import os
import dotenv
import logging
from logging.handlers import RotatingFileHandler
import datetime
import asyncio


PRUNED_CHANNELS = [
    (736963923521175612, 30),  # shitposting - 30 days
    (986699377257119794, 180),  # general - 6 months
    (986699973800390677, 180),  # random - 6 months
    (986700814938697728, 180),  # text-for-voice - 3 months
]

PRUNED_CHANNELS = [(1234263126632042567, 30)]

list_of_coroutines = []

DEBUG_MODE = False

if not DEBUG_MODE:
    run_every = 3600  # i.e. run every hour in production
else:
    run_every = 60  # seconds

# log with rotating file handler
logger = logging.getLogger("discordOldMessageDeleter")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(
    "discordOldMessageDeleter.log", maxBytes=1000000, backupCount=5
)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


async def prune(client, channel_id: int, delay_days: int):
    channel: discord.TextChannel = client.get_channel(channel_id)
    time_delta = (
        datetime.timedelta(seconds=delay_days)
        if DEBUG_MODE
        else datetime.timedelta(days=delay_days)
    )
    async for msg in channel.history(
        limit=None, before=datetime.datetime.now() - time_delta
    ):
        try:
            fire(msg.delete())
        except discord.errors.NotFound:
            logger.error(f"message not found: {msg.id}")
            break


def fire(coro):
    list_of_coroutines.append(asyncio.create_task(coro))


class OldMessageDeleter(discord.Client):
    """
    Deletes old messages one by one,
    has to do it one by one because no bulk delete api:
    https://github.com/discord/discord-api-docs/issues/208

    Must avoid rate limits and bans
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        logger.info("------")

    async def my_background_task(self):
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                for channel_id, delay_days in PRUNED_CHANNELS:
                    print(f"pruning channel {channel_id} with delay {delay_days}")
                    logger.info(f"pruning channel {channel_id} with delay {delay_days}")
                    await prune(self, channel_id, delay_days)
                await asyncio.gather(*list_of_coroutines)
                logger.info("finished gathering coroutines")
                await asyncio.sleep(run_every)
            except Exception as e:
                logger.error(f"error in background task: {e}")

        logger.error("connection closed")


if __name__ == "__main__":
    dotenv.load_dotenv(".env")
    client = OldMessageDeleter(intents=discord.Intents.default())
    token = os.getenv("DISCORD_TOKEN")

    try:
        client.run(token)
    except Exception as e:
        logger.error(f"error in main: {e}")
        raise e
