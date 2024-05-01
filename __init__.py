from .role_helper import RoleHelper


async def setup(bot):
    await bot.add_cog(RoleHelper(bot))
