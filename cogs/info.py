import discord
from discord.ext import commands


#####################################################################

class info(commands.Cog):
	def __init__(self,client):
		self.client = client

	#################################################################

	
	@commands.command(aliases = ["info_server", "server_info", "info"], usage = "", description = "Basic info about the server")#ritorna le info del server
	async def info_(self, ctx):
		await ctx.channel.purge(limit = 1)
		guild = ctx.guild
		name = guild.name
		owner = guild.owner
		icon = str(guild.icon_url)
		n_members = guild.member_count
		creation_time = str(guild.created_at)[:-7]
		region = guild.region
		afk = guild.afk_timeout
		embed = discord.Embed(title = name, colour = 0xff0000)
		embed.set_thumbnail(url = icon)
		embed.add_field(name = "*Owner:*", value = owner, inline = False)
		embed.add_field(name = "*Number of members:*", value = n_members, inline = False)
		embed.add_field(name = "*Creation date:*", value = creation_time, inline = False)
		embed.add_field(name = "*Region*", value = region, inline = False)
		embed.add_field(name = "*Incativity time in seconds:*", value = afk, inline = False)
		await ctx.channel.send(embed = embed)

	
	#################################################################


	@commands.command(aliases = ["emoji", "emote", "emotes", "reactions"], usage = "", description = "Shows the server's custom emojis")
	async def emojis(self, ctx):	
		await ctx.channel.purge(limit = 1)
		guild = ctx.guild
		emojis = guild.emojis
		icon = str(guild.icon_url)
		embiid = discord.Embed(title = "***Emoji List***", colour = 0xab4523 )
		embiid.set_thumbnail(url = icon)
		if not emojis: embiid.add_field(name = "*ERROR*", value = "No custom emojis found")
		for p in emojis:
			embiid.add_field(name = p.name, value = str(p))		
		await ctx.channel.send(embed = embiid)

	
	#################################################################

	@commands.command(aliases = ["infoc", "info_channels", "channelslist", "infochannels"], usage = "", description = "Shows a list of the server's channels")
	
	async def channels(self, ctx):
		await ctx.channel.purge(limit = 1)
		guild = ctx.guild
		icon = str(guild.icon_url)
		embed = discord.Embed(title = "***Channels***", colour = 0xcdef01 )
		embed.set_thumbnail(url = icon)
		channels_by_category = guild.by_category()
		for p in channels_by_category:
			for i in range(len(p[1])):
				embed.add_field(name = p[0], value = p[1][i], inline = False)
		await ctx.channel.send(embed = embed)

	
	#################################################################

	
	@commands.command(aliases = ["info_bot", "bot", "botinfo"], usage = "", description = "Shows informations about the bot")
	
	async def infobot(self,  ctx):
		await ctx.channel.purge(limit = 1)
		embed = discord.Embed(title = "***BOT_NAME_HERE***", colour = 0xff0000 )
		icon = self.client.user.avatar_url
		n_guilds = len(self.client.guilds)
		latency = round(self.client.latency * 1000)
		joined = str(ctx.guild.me.joined_at)[:-7]
		embed.set_thumbnail(url = str(icon))
		embed.add_field(name = "*Nickname:*", value = ctx.guild.me.display_name, inline = False)
		embed.add_field(name = f"*Member of {ctx.guild.name} since:*", value = joined, inline = False)
		embed.add_field(name = "*For info about my commands type:*", value = "***!help***", inline = False)
		embed.add_field(name = "*Number of servers where i work:*", value = n_guilds, inline = False)
		embed.add_field(name = "*Latency in ms:*", value = latency, inline = False)
		await ctx.channel.send(embed = embed)


	#################################################################

	
	@commands.command(aliases = ["userinfo", "user_info"], usage = " @user", description = "Shows some info about the mentiones user")
	async def user(self,  ctx, user: discord.Member):
		await ctx.channel.purge(limit = 1)
		icon = user.avatar_url
		joined_at = str(user.joined_at)[:-7]
		nick = user.nick
		premium = user.premium_since
		colour = user.colour
		top_role = user.top_role
		embed = discord.Embed(title = f"{user.name}", colour = colour )
		embed.set_thumbnail(url = str(icon))
		embed.add_field(name = "*Nickname:*", value = nick, inline = False)
		if premium: embed.add_field(name = "*Premium since:*", value = premium, inline = False)
		embed.add_field(name = "*Member since:*", value = joined_at, inline = False)
		embed.add_field(name = "*Top rank:*", value = top_role.name, inline = False)
		await ctx.channel.send(embed = embed)


	#################################################################
	

def setup(client):
	client.add_cog(info(client))			
