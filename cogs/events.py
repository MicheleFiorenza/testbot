import discord
import datetime
from datetime import date
from discord.ext import commands
from fun_1 import check_channels 

#####################################################################

class events(commands.Cog):
	def __init__(self,client):
		self.client = client

#####################################################################

	@commands.command(usage = "event_name date time *max_spots*", description = "Creates an event with *max_spots*  free spots, if limit is 0 => there are no restrictions")
	async def create_event(self,  ctx, date, time, max_spots: int, *event_name):
		await ctx.channel.purge(limit = 1)
		channels = check_channels(ctx.guild.text_channels)
		if channels[1][0] == "events-channel":
			channel_id = channels[1][1]
		else:
			await ctx.send("events-channel not found")
		date = str(date)+" "+str(time)
		format_ = "%d/%m/%Y %H:%M"
		try:
			date = datetime.datetime.strptime(date, format_)
		except ValueError: print("ValueError => invalid input!")
		ev_name = ""
		for name in event_name:
			ev_name += " " + name
		embed = discord.Embed(title = f"{ev_name}", description = "Press ✅ to confirm your partecipation, ❌ to confirm your absence or ❓ if you are not sure yet!", colour = 0x987654)
		embed.add_field(name = "📅 When:", value = f"{date}", inline = False)
		embed.add_field(name = "Number of participants:", value = "🥳", inline = False )
		embed.add_field(name = "Number of absent:", value = "😢", inline = False )
		embed.add_field(name = "Number of uncertain:", value = "🤔", inline = False )					
		embed.add_field(name = "For more info please ask:", value = f"{ctx.author.name}", inline = False)
		if max_spots >= 1:
			embed.add_field(name = f"Free spots:", value = max_spots )
		embed.set_thumbnail(url = str(ctx.author.avatar_url))
		message = await ctx.guild.get_channel(channel_id).send(embed = embed)
		await message.add_reaction("✅")
		await message.add_reaction("❌")
		await message.add_reaction("❓")

#####################################################################

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		channel_id = payload.channel_id
		message_id = payload.message_id
		member = payload.member
		user_id = payload.user_id
		emoji = payload.emoji
		if self.client.user.id == user_id:return
		channel = member.guild.get_channel(channel_id)
		if not channel.name == "events-channel":return
		message = await channel.fetch_message(message_id)
		embed = message.embeds[0]
		event_date = embed.fields[0].value
		now = datetime.datetime.now()
		if not datetime.datetime.strptime(event_date, "%Y-%m-%d %H:%M:%S") > now: return
		for field in embed.fields:
			if field.name == f"{member.name}{member.discriminator}":return
		if emoji.name == "✅":
			limit = False
			spots = True
			for field in embed.fields:
				if field.name == "Free spots:" and int(field.value) > 0:
					limit = True
					break
				elif field.name == "Free spots:" and int(field.value) == 0:
					limit = True
					spots = False
					break
			if not limit:		
				embed.set_field_at(index = 1, name = "Participants:", value = embed.fields[1].value + "✅", inline = False)
			elif limit and spots:
				embed.set_field_at(index = 1, name = "Participants:", value = embed.fields[1].value + "✅", inline = False)
				embed.set_field_at(index = 5, name = "Free spots:", value = int(embed.fields[5].value) - 1, inline = False)
			else: return
		#############################################################
		elif emoji.name == "❌":
			embed.set_field_at(index = 2, name = "Absent:", value = embed.fields[2].value + "❌", inline = False)
		#############################################################			
		elif emoji.name == "❓":
			embed.set_field_at(index = 3, name = "Uncertain:", value = embed.fields[3].value + "❓", inline = False)
		else:return
		#############################################################
		embed.add_field(name = f"{member.name}{member.discriminator}", value = emoji)
		await message.edit(embed = embed)

#####################################################################

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		guild = self.client.get_guild(payload.guild_id)
		channel = guild.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		user_id = payload.user_id
		member = guild.get_member(user_id)
		emoji = payload.emoji
		target_field1 = False
		target_field2 = False
		if self.client.user.id == user_id:return
		if not channel.name == "events-channel":return
		embed = message.embeds[0]
		event_date = embed.fields[0].value
		now = datetime.datetime.now()
		if not datetime.datetime.strptime(event_date, "%Y-%m-%d %H:%M:%S") > now: return
		for field in range(len(embed.fields)):
			if embed.fields[field].name == f"{member.name}{member.discriminator}" and embed.fields[field].value == emoji.name:
				target_field1 = field
		if embed.fields[5].name == "Free spots:":
				target_field2 = True		
		if target_field1 == False: return			
		embed.remove_field(target_field1)
		if emoji.name == "❓":
			new_field_value = embed.fields[3].value.replace("❓", "", 1)
			embed.set_field_at(index = 3, name = "Uncertain:", value = new_field_value, inline = False)
		elif emoji.name == "❌":
			new_field_value = embed.fields[2].value.replace("❌", "", 1)
			embed.set_field_at(index = 2, name = "Absent:", value = new_field_value, inline = False)	
		elif emoji.name == "✅":
			new_field_value = embed.fields[1].value.replace("✅", "", 1)
			embed.set_field_at(index = 1, name = "Participants:", value = new_field_value, inline = False)
			if target_field2:
				embed.set_field_at(index = 5, name = "Free spots:", value = int(embed.fields[5].value) + 1, inline = False)
		await message.edit(embed = embed)




#####################################################################

def setup(client):
	client.add_cog(events(client))