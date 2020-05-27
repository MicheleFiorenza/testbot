import discord
import datetime
from datetime import date
from discord.ext import commands
from fun_1 import *

#####################################################################

class channels(commands.Cog):
	def __init__(self,client):
		self.client = client

#####################################################################

				

#####################################################################

	@commands.command(usage = " on  *or*  off ", description = "Enables / Disables event commands")
	@commands.has_permissions(manage_channels = True)
	async def event_channels_setup(self,  ctx, value):
		channels = check_channels(ctx.guild.text_channels)
		if value == "on":
			category = False
			for x in ctx.guild.categories:
				if x.name == "Events and Games":
					new_cat = x
					category = True
			if not category: 
				new_cat = await ctx.guild.create_category("Events and Games")		
			if not channels[0][0]:
				await new_cat.create_text_channel("poll-channel")
			if not channels[1][0]:
				await new_cat.create_text_channel("events-channel")
			if not channels[2][0]:
				await new_cat.create_text_channel("games-channel")
		elif value == "off":
			ch_list = []
			if channels[0][0] == "poll-channel":
				ch_list.append(ctx.guild.get_channel(channels[0][1]))
			if channels[1][0] == "events-channel":
				ch_list.append(ctx.guild.get_channel(channels[1][1]))
			if channels[2][0] == "games-channel":
				ch_list.append(ctx.guild.get_channel(channels[2][1]))
			for channel in ch_list:
				await channel.delete()	
			for x in ctx.guild.categories:
				if x.name == "Events and Games": await x.delete()
											
		else:
			await ctx.send("Usage = !channels_setup on  *or* !channels_setup off")

#####################################################################

	@commands.command(usage = " on  *or*  off ", description = "Enables / Disables info commands")
	@commands.has_permissions(manage_channels = True)
	async def basic_channels_setup(self,  ctx, value):
		channels = check_basic_channels(ctx.guild.text_channels)
		if value == "on":
			category = False
			for x in ctx.guild.categories:
				if x.name == "Bot":
					new_cat = x
					category = True
			if not category: 
				new_cat = await ctx.guild.create_category("Bot")		
			if not channels[0][0]:
				await new_cat.create_text_channel("spam")
			if not channels[1][0]:
				await new_cat.create_text_channel("bot-channel")
		elif value == "off":
			if channels[1][0] == "bot-channel":
				await channels[1][1].delete()	
			for x in ctx.guild.categories:
				if x.name == "Bot": await x.delete()
											
		else:
			await ctx.send("Usage = !basic_channels_setup on  *or* !basic_channels_setup off")





def setup(client):
	client.add_cog(channels(client))
