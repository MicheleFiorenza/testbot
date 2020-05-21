import discord
import os
from discord.ext import commands

#####################################################################	

client = commands.Bot(command_prefix = "!")

#####################################################################

@client.command(hidden = True)
@commands.is_owner()
async def load(ctx, *commands):
	for extension in commands:
		client.load_extension(f'cogs.{extension}')
		await ctx.send(f"{extension} Done")
	
#####################################################################

@client.command(hidden = True)
@commands.is_owner()
async def unload(ctx, *commands):
	for extension in commands:
		client.unload_extension(f'cogs.{extension}')
		await ctx.send(f" {extension} Done")

#####################################################################

@client.command(hidden = True)
@commands.is_owner()
async def reload(ctx, *commands):
	for extension in commands:
		client.unload_extension(f'cogs.{extension}')
		client.load_extension(f'cogs.{extension}')
		await ctx.send(f" {extension} Done")

#####################################################################

for filename in os.listdir("./cogs"):			
	if filename.endswith(".py"):
		client.load_extension(f'cogs.{filename[:-3]}')

#####################################################################


client.run("TOKEN")
