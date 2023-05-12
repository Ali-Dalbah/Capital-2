import discord
from dotenv import load_dotenv
from discord.ext import commands
from guild_data import guild_data
import os

load_dotenv()

map = {}

# FFMPEG_PATH = '/home/runner/qabital/node_modules/ffmpeg-static/ffmpeg'

# TO-DO list:
# Handling the bot being kicked or moved
# adding slash commands

token = os.environ['TOKEN']
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
discord.opus.load_opus("./libopus.so.0.8.0")
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print('Bot is Online')

@bot.command(name='blay', aliases=['play', 'p', 'جيب'], help='blay song')
async def blay(ctx, *, query: str):
  if not ctx.message.author.voice:
    await ctx.send("foot 3l voice ya ga7ba")
    return 
  if not ctx.guild in map.keys() or map[ctx.guild] == None:
    map[ctx.guild] = guild_data(ctx)
  guild = map[ctx.guild]
  if not guild.is_connected():
    await guild.join_channel(ctx.message.author.voice.channel)
  guild.enqueue(query)
  await guild.blay()    

@bot.command(name='zgib', aliases=['skip', "مشي"], help='zgib zong')
async def zgib(ctx):
  if ctx.guild in map.keys() and not map[ctx.guild] == None:
    await map[ctx.guild].skip()

@bot.command(name='stop', aliases =['كسمك'] , help='stop player')
async def stop(ctx):
  if not ctx.message.author.voice:
    await ctx.send("fot voice 3shan ard 3lek")
    return
  if not ctx.guild in map.keys() or map[ctx.guild] == None or not map[ctx.guild].is_connected():
    await ctx.send("mne msh fayt ya ka7ba")
    return
  await map[ctx.guild].leave_channel()

@bot.command(name='pause', help='pause current song')
async def pause(ctx):
  if not ctx.message.author.voice:
    await ctx.send('join voice channel retard')
    return
  if not ctx.guild in map.keys() or map[ctx.guild] == None:
    return
  await map[ctx.guild].pause()

@bot.command(name='resume', help='to resume paused song')
async def resume(ctx):
  if not ctx.message.author.voice:
    await ctx.send("you are not in a voice channel ")
    return
  if not ctx.guild in map.keys() or map[ctx.guild] == None:
    await ctx.send('طيب ماشي بحكيلك معه')
    return
  await map[ctx.guild].resume()

# @bot.command(name='seek', help='seek sonk')
# async def seek(ctx):
#   await ctx.voice_client.seek(10000)
#   await ctx.send('sek')

@bot.command(name='move', help='move the bot voice channel')
async def move(ctx):
  if not ctx.message.author.voice:
    async with ctx.typing():
      await ctx.send('You are not in voice channel retard')
      return
  if not ctx.guild in map.keys() or map[ctx.guild] == None or not map[ctx.guild].is_connected():
    async with ctx.typing():
      await ctx.send("I'm not in voice channel retard")
      return
  async with ctx.typing():
    await ctx.send('Moving')
    await map[ctx.guild].move_to(ctx.message.author.voice.channel)

@bot.event
async def on_command_error(ctx, err):
  if isinstance(err, commands.CommandNotFound):
    async with ctx.typing():
      await ctx.send("yes i fully understood that retard")
  raise err

def run():
  guild_data.bot = bot
  bot.run(token)
