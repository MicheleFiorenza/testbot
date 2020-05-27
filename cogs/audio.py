import discord
from discord.ext import commands
import asyncio
import os
import random

#####################################################################

ffmpeg_options = {
	'options': '-vn'
}

#####################################################################

class audio(commands.Cog):
	def __init__(self,client):
		self.client = client

#####################################################################

	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		connected = [False]
		for connection in self.client.voice_clients:
			if connection.guild == member.guild and connection.channel == after.channel:
				connected[0] = True
				connected.append(connection)
		if not connected[0] or member == member.guild.me: return
		if before != None and before.channel == after.channel: return
		mlist =  os.listdir("./mp3")
		mfile = random.choice(mlist)
		source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f'./mp3/{mfile}'))
		vc = connected[1]
		vc.play(source, after = lambda e: print(f'error {e}') if e else None)



#####################################################################

	@commands.command( description = "The bot joins the channel")
	async def join(self, ctx):
		if not ctx.voice_client == None:
			return await ctx.voice_client.move_to(ctx.message.author.voice.channel)
		await ctx.message.author.voice.channel.connect()	

#####################################################################

	@commands.command( description = "The bot leaves the channel")
	async def leave(self, ctx):
		leave = False
		for connection in self.client.voice_clients:
			if connection.guild == ctx.guild: leave = True
		if leave: await ctx.voice_client.disconnect()
				
#####################################################################

	"""@commands.command()
				async def play(self, ctx, url):
					ctx.voice_client.play(discord.FFmpegPCMAudio(url, **ffmpeg_options), after=lambda e: print(f'Player error: {e}') if e else None)
					await ctx.send(f'Now playing: {url}')
			"""
##################################################################### ends here		

	"""@commands.command( description = "Change volume")
				async def volume(self, ctx, volume: int):
					if ctx.voice_client == None:
						return await ctx.send('Not connected to a voice channel!')
					ctx.voice_client.source.volume = volume/100
					await ct.send(f'Changed volume to {volume}/100')	
			"""
#####################################################################

def setup(client):
	client.add_cog(audio(client))