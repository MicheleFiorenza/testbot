import discord
from discord.ext import commands

#####################################################################

class client_(commands.Cog):
	def __init__(self,client):
		self.client = client

#####################################################################

	@commands.Cog.listener()
	async def on_ready(self):
		print("Bot online!")
		status = discord.Status.online
		activity = discord.Game("GTA VI: Napoli")
		await self.client.change_presence(status = status, activity = activity)
		print(f"Status = {status}\nActivity = {activity}")

#####################################################################

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			await ctx.send(f'The command " {ctx.message.content.split(" ")[0]} " does not exist')
			return
		name = ctx.command.name
		print(f"User = {ctx.author}", error)
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("MissingRequiredArgument")
		elif isinstance(error, commands.MissingPermissions):
			await ctx.send(f"MissingPermissions {name}")
		elif isinstance(error, commands.DisabledCommand):
			await ctx.send(f"DisabledCommand {name}")
		elif isinstance(error, commands.TooManyArguments):
			await ctx.send("TooManyArguments")
		elif isinstance(error, commands.UserInputError):
			await ctx.send("UserInputError")
		elif isinstance(error, commands.NotOwner):
			await ctx.send(f"NotOwner")
		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.send(f"CommandOnCooldown {name}")
		elif isinstance(error, commands.BotMissingPermissions):
			await ctx.send(f"BotMissingPermissions {name}.")
		elif isinstance(error, commands.MissingRole):
			await ctx.send(f"BotMissingRole {name}")
		elif isinstance(error, commands.BotMissingRole):
			await ctx.send(f"BotMissingRole {name}")
		elif isinstance(error, commands.CommandInvokeError):
			await ctx.send(f"Bip Boop! CommandInvokeError {name}.")
		elif isinstance(error, commands.CheckFailure):
			await ctx.author.send(f"CheckFailure!")		
		else:
			await ctx.author.send("Error")	
			
#####################################################################			

def setup(client):
	client.add_cog(client_(client))
