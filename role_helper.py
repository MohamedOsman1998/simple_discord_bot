from redbot.core import commands

class RoleHelper(commands.Cog):
    """
    """

    def __init__(self, bot):
        self.bot = bot
        bot.remove_command("help")

        bot.remove_command("embedset")
        bot.remove_command("info")
        bot.remove_command("licenseinfo")
        bot.remove_command("mydata")
        bot.remove_command("set")
        bot.remove_command("uptime")


    @commands.command()
    async def help(self, ctx):
        roles = [
            "meetup",
            "daily-paper-discussion",
            "reinforcement-learning",
            "natural-language-processing",
            "computer-vision",
            "world-modelz",
            "arc-challenge",
            "arc-challenge-blackbox",
            "arc-challenge-explainable",
            "homebrew-nlp"
        ]
        message = "send `.role <role-name>` to get a role:\npossible roles:"
        for i,role in enumerate(roles):
            if i % 3 == 0:
                message += "\n"
                message += "> "
            if i == len(roles) - 1:
                message += f"`{role}`"
            else:
                message += f"`{role}`, "
        await ctx.send(message)

