from redbot.core import commands

class RoleHelper(commands.Cog):
    """
    """

    def __init__(self, bot):
        self.bot = bot
        bot.remove_command("help")

        bot.remove_command("contact")
        bot.remove_command("embedset")
        bot.remove_command("info")
        bot.remove_command("licenseinfo")
        bot.remove_command("mydata")
        bot.remove_command("set")
        bot.remove_command("uptime")


    @commands.command()
    async def help(self, ctx):
        roles = ["meetup","daily-paper-discussion"]
        message = "send .role <role> to get a role:\npossible roles:"
        for role in roles:
            message += f"\n{role}"
        await ctx.send(message)

