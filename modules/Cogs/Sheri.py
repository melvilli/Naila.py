import os

import discord
import httpx
from discord.ext import commands

from utils.checks import checks

base_url = "https://sheri.bot/api/"


async def sheri_embed(ctx):
    em = discord.Embed(color=await ctx.guildcolor(), description="**Website:** https://sheri.bot/\n")
    em.set_author(name="Images provided by Sheri Blossom", url="https://sheri.bot/")
    em.set_footer(text="If there's an issue with ANY image, please take it up with the provider.")
    return em


async def image_send(ctx, endpoint: str):
    async with httpx.AsyncClient as session:
        data = await session.get(url=base_url + endpoint, headers={"Authorization": os.getenv("SHERI"),
                                                                   "User-Agent": "Naila Discord Bot - By Kanin#0001"})
        if data.status_code == 200:
            response = data.json()
            embed = await sheri_embed(ctx)
            embed.set_image(url=response['url'])
            embed.add_field(name="Issue with image?",
                            value="Report it to the sheri.bot using the below link\n"
                                  f"{response['report_url']}")
            return await ctx.send(embed=embed)
        else:
            return await ctx.send("Either the website is down or there is an internal error, Please contact support!")


class Sheri(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="sheri")
    async def sheri(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @checks.is_nsfw()
    @sheri.group(name="nsfw")
    async def sheri_nsfw(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @sheri.group(name="sfw")
    async def sheri_nsfw(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @sheri_nsfw.group(name="yiff")
    async def sheri_nsfw_yiff(self, ctx):
        await image_send(ctx, "yiff")


def setup(bot):
    bot.add_cog(Sheri(bot))
