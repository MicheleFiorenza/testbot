import discord
import asyncio
from discord.ext import commands
from var import passfrase

#user related events/commands
#####################################################################

class user(commands.Cog):
	def __init__(self,client):
		self.client = client

	#################################################################	


	@commands.Cog.listener()
	async def on_member_join(self, member):
		if not ('manage_roles', True) in member.guild.me.guild_permissions:return
		DM = await member.send(f'If you want to be able to chat in this server just type: *{passfrase}* ')
		def check(message):
			return message.content == passfrase and message.channel == DM.channel
		try:	
			msg = await self.client.wait_for("message", check = check, timeout = 120.0)
		except asyncio.TimeoutError:
			await member.send("Timeout error, please retry. ")
			await member.kick(reason = "Timeout Error")
			return	
		await DM.channel.send(f"Welcome {member.mention}!")
		embed = discord.Embed(title = "***ATTENTION!***", description = "something something", colour = 0x666666)
		embed.add_field(name = "Name:", value = member.name, inline = False)
		embed.set_thumbnail(url = member.avatar_url)
		await member.add_roles(member.guild.roles[1])
		channels = check_basic_channels(member.guild.text_channels)
		if channels[1][0] == "bot-channel":
			channel_id = channels[1][1]
			await member.guild.get_channel(channel_id).send(embed = embed)
		else:	
			await member.guild.system_channel.send(embed = embed)


	#################################################################


	@commands.command(usage = "!ban @user", description = "Bans the mentioned user")
	@commands.has_permissions(ban_members = True)
	async def ban(self, ctx, member: discord.Member, *, reason=None):
		await ctx.channel.purge(limit = 1)
		if reason == None: reason = "Not specified"
		embed = discord.Embed(title = "***ATTENION***", description = "*Someone has been banned!*", colour = 0xed2378)
		embed.add_field(name = "***Banned user:***", value = member, inline = False)
		embed.add_field(name = "***Reason:***", value = reason, inline = False)
		embed.add_field(name = "***Who banned him:***", value = ctx.author, inline = False)
		icon = self.client.user.avatar_url
		embed.set_thumbnail(url = str(icon))
		channels = check_basic_channels(ctx.guild.text_channels)
		if channels[1][0] == "bot-channel":
			channel_id = channels[1][1]
			await ctx.guild.get_channel(channel_id).send(f"{member.mention}", embed = embed)
		else:	
			await ctx.guild.system_channel.send(f"{member.mention}", embed = embed)
		await member.ban(reason = reason)


	#################################################################


	@commands.command(usage = "!kick @user", description = "Kicks the mentioned used")
	@commands.has_permissions(kick_members = True)
	async def kick(self, ctx, member: discord.Member, *, reason=None):
		await ctx.channel.purge(limit = 1)
		if reason == None: reason = "Not specified"
		embed = discord.Embed(title = "***ATTENTION***", description = "*Someone has banned kicked!*", colour = 0xed2378)
		embed.add_field(name = "***Kicked user:***", value = member, inline = False)
		embed.add_field(name = "***Reason***", value = reason, inline = False)
		embed.add_field(name = "***Who kicked him:***", value = ctx.author, inline = False)
		icon = self.client.user.avatar_url
		embed.set_thumbnail(url = str(icon))
		channels = check_basic_channels(ctx.guild.text_channels)
		if channels[1][0] == "bot-channel":
			channel_id = channels[1][1]
			await ctx.guild.get_channel(channel_id).send(f"{member.mention}", embed = embed)
		else:	
			await ctx.guild.system_channel.send(f"{member.mention}", embed = embed)
		await member.kick(reason = reason)


	#################################################################


	@commands.command(usage = "!unban user.name#user.number", description = "Unbans 'user'")
	@commands.has_permissions(ban_members = True)
	async def unban(self, ctx, *, member):
		await ctx.channel.purge(limit = 1)
		banned_users = await ctx.guild.bans()
		member_name, member_discriminator = member.split("#")
		for entry in banned_users:
			user = entry.user
			if (user.name, user.discriminator) == (member_name, member_discriminator):
				embed  = discord.Embed(title  = "***ATTENTION**", description = "*Someone has been unbanned!*", colour = 0x123456)
				embed.add_field(name = "***User***", value = user, inline = False)
				embed.add_field(name = "***Reason of the previous ban***", value = entry.reason, inline = False)
				embed.add_field(name = "***Who revoked the ban:***", value = ctx.author, inline = False)
				icon = self.client.user.avatar_url
				embed.set_thumbnail(url = str(icon))
				await ctx.guild.unban(user)
				channels = check_basic_channels(ctx.guild.text_channels)
				if channels[1][0] == "bot-channel":
					channel_id = channels[1][1]
					await ctx.guild.get_channel(channel_id).send(f"{user.mention} can re-join the server!", embed = embed )
				else:	
					await ctx.guild.system_channel.send(f"{user.mention} can re-join the server!", embed = embed )
				if not user.bot:
					await user.send(f"You can now re-join {ctx.guild.name}")
		return

			
	#################################################################


	@commands.command( usage = "!changenick @user *new_nick*", description = "Sets the nickname of the mentrioned user to *new_nick*, or removes the nickname if *new_nick* is not given")
	@commands.has_permissions(manage_nicknames = True)
	async def changenick(self, ctx, user: discord.Member=None, *, args = None):
		await ctx.channel.purge(limit = 1)
		await user.edit( nick = args )


	#################################################################

def setup(client):
	client.add_cog(user(client))	
