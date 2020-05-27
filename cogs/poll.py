import discord
import asyncio
from discord.ext import commands
from fun_1 import check_channels

#####################################################################

class poll(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.command()
	async def createpoll(self,  ctx):
		arglist = ['Title', 'Description', 'number of options']
		reslist = []
		optlist = []
		await ctx.channel.purge(limit = 1)
		channels = check_channels(ctx.guild.text_channels)
		if channels[0][0] == "poll-channel":
			channel_id = channels[0][1]
		else:
			await ctx.send("poll-channel not found")
		member = ctx.message.author	
		await member.send(f'Everythng is ready! please provide the following informations when requested: the *Title* of the poll, a short *Description* for the poll*, the *number* of different options and then the *Options*.After 2 minutes without a response the process will be terminated.')	
		for i in range(3):	
			DM = await member.send(f'Please type the following information: *{arglist[i]}*')
			def check(message):
				return message.channel == DM.channel and message.author != ctx.guild.me
			try:	
				msg = await self.client.wait_for("message", check = check, timeout = 120.0)
			except asyncio.TimeoutError:
				await member.send("Timeout error, please retry. ")
				return
			reslist.append(msg.content)
		for p in range(int(reslist[2])):
			c = p+1
			DM = await member.send(f'Please type the following information: *option{c}*')
			def check(message):
				return message.channel == DM.channel and message.author != ctx.guild.me
			try:	
				msg = await self.client.wait_for("message", check = check, timeout = 120.0)
			except asyncio.TimeoutError:
				await member.send("Timeout error, please retry. ")
				return
			optlist.append(msg.content)
		counter = 0
		embed = discord.Embed(title = f"*{reslist[0]}*", description = f'{reslist[1]}', colour = 0x987654)
		embed.add_field(name = "Number of answers:", value = "📝", inline = False )
		for arg in optlist:
			counter += 1
			embed.add_field(name = f"option {counter}:", value = arg, inline = False )
		embed.add_field(name = "Poll created by:", value = f"{ctx.author.name}", inline = False)
		embed.set_thumbnail(url = str(ctx.author.avatar_url))
		message = await ctx.guild.get_channel(channel_id).send(embed = embed)
		await message.add_reaction("✏️")

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
		if not channel.name == "poll-channel":return
		message = await channel.fetch_message(message_id)
		embed = message.embeds[0]
		for p in range(len(embed.fields)):
			if embed.fields[p].name == f"{member.name}{member.discriminator}": return
		if emoji.name == "✏️":
			DM = await member.send("Choose an *option* by typing the options' number eg 'option 3'")
			def check(message):
				return message.channel == DM.channel and message.author != member.guild.me
			try:	
				msg = await self.client.wait_for("message", check = check, timeout = 120.0)
			except asyncio.TimeoutError:
				await member.send("Timeout error, please retry. ")
				return
		option = msg.content+":"
		for p in range(len(embed.fields)):
			if embed.fields[p].name == option:
				embed.set_field_at(index = p, name = embed.fields[p].name, value = embed.fields[p].value + "✏️", inline = False)
		embed.add_field(name = f"{member.name}{member.discriminator}", value = "✏️")
		await message.edit(embed = embed)	



#####################################################################

def setup(client):
	client.add_cog(poll(client))				