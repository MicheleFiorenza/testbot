import discord
import os
from discord.ext import commands

#####################################################################	

TOKEN = 'NTc0NjM3MTg1OTI4NzkwMDE3.XsaqNA.TsaKkLDclaHZ33qoKZd5KQMJgbc'
client = commands.Bot(command_prefix = '!')

for filename in os.listdir("./cogs"):			
	if filename.endswith(".py"):
		client.load_extension(f'cogs.{filename[:-3]}')

#####################################################################


client.run(TOKEN)
