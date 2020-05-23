import discord
from discord.ext import commands, tasks

##########################################à

class utility(commands.Cog):
	def __init__(self,client):
		self.client = client


#################################################################


	@commands.command(aliases = ["purge", "delete"], usage = " *Number* ", description = "Deletes *Number* messages in the current text channel")
	@commands.has_permissions(manage_messages = True)
	async def clear(self, ctx,amount=2):
		await ctx.channel.purge(limit=amount)

#àà#à######################################ààà

def setup(client):
	client.add_cog(utility(client))
