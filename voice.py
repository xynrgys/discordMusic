import discord
from discord.ext import commands
import youtube_dl
import os
from discord.utils import get

client = commands.Bot(command_prefix="!")

@client.command()
async def play(ctx, url : str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing song to end or use the STOP command")
        return

    #userVoiceChannel = ctx.author.voice.channel
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        return await ctx.send('You need to be in a voice channel to use this command!')
    vc = get(client.voice_clients, guild=ctx.guild)
    await ctx.guild.change_voice_state(channel=vc, self_mute=False, self_deaf=True)
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        vc = await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
        vc = ctx.voice_client



    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',
    }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    vc.play(discord.FFmpegPCMAudio("song.mp3"))



@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
        await ctx.send("Leaving...")
    else:
        await ctx.send("Not in a voice channel")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("Song Paused")
    else:
        await ctx.send("Nothing is playing")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("Song Resumed")
    else:
        await ctx.send("Audio is not paused")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await ctx.send("Stopping...")
    voice.stop()


client.run('YOUR_TOKEN_HERE')
