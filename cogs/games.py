import discord
import datetime
from datetime import date
from discord.ext import commands
from fun_1 import check_channels

#####################################################################

class games(commands.Cog):
	def __init__(self,client):
		self.client = client

#####################################################################

	@commands.command()
	async def playgame(self, ctx):
		await ctx.channel.purge(limit = 1)
		channels = check_channels(ctx.guild.text_channels)
		if channels[2][0] == "games-channel":
			channel_id = channels[2][1]
		else:
			await ctx.send("games-channel not found")
		



def setup(client):
	client.add_cog(games(client))			