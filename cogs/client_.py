import discord
from discord.ext import commands


#####################################################################

class client_(commands.Cog):
	def __init__(self,client):
		self.client = client

	#################################################################

	@commands.Cog.listener()
	async def on_ready(self):
		print("Bot online!")
		status = discord.Status.online
		activity = discord.Game("GTA VI: Napoli")
		await self.client.change_presence(status = status, activity = activity)
		print(f"Status = {status}\nActivity = {activity}")

def setup(client):
	client.add_cog(client_(client))
