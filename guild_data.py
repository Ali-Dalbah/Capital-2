from ytdl import YTDL
import discord
from discord.utils import get
import os
import asyncio
import random

def remove_file(filename: str):
  if os.path.exists(filename):
    os.remove(filename)


class guild_data:
  bot = None
  def __init__(self, ctx):
    self.guild = ctx.guild
    self.voice_channel = ctx.message.author.voice.channel
    self.typing = ctx.typing
    self.chat = ctx.send
    self.loop: bool = False
    self.queue: list = []
    self.filename: str = ""
    self.list: list = []

  def get_client(self):
    return get(guild_data.bot.voice_clients, guild=self.guild)

  
  async def send_msg(self, msg: str):
    async with self.typing():
      await self.chat(msg)

  
  def is_connected(self) -> bool:
    voice_client = self.get_client()
    if not voice_client:
      return False
    return voice_client.is_connected()

  
  def is_playing(self) -> bool:
    voice_client = self.get_client()
    if not voice_client:
      return False
    return voice_client.is_connected() and voice_client.is_playing()

  def get_next_song(self) -> str:
    if len(self.queue) <= 0:
      return None
    return self.queue[0]

  def dequeue(self) -> str:
    if len(self.queue) <= 0:
      return None
    return self.queue.pop()

  
  def enqueue(self, song: str) -> None:
    self.queue.insert(0, song)

  async def blay(self) -> None:
    if not self.is_connected():
      await self.join_channel()
    elif self.is_playing() or self.is_paused():
      await self.chat(f'{self.queue[len(self.queue) - 1]} was added to the queue with {len(self.queue)} before it ')
      return
    song = self.dequeue()
    if not song == None:
      async with self.typing():
        filename = await YTDL.from_url(song, loop=guild_data.bot.loop)
        self.filename = filename
      self.get_client().play(discord.FFmpegPCMAudio(source=filename), after=lambda e: asyncio.run_coroutine_threadsafe(self.__play_callback(), guild_data.bot.loop))
      await self.send_msg(f'now playing {song}')
    else:
      await self.send_msg("empty queue no baley :|")
  
  async def join_channel(self, voice_channel=None):
    if not voice_channel == None:
      self.voice_channel = voice_channel
    await self.voice_channel.connect()

  async def __play_callback(self):
    remove_file(self.filename)
    if len(self.queue) > 0 and self.is_connected():
      await self.blay()
    else:
      await self.send_msg("No More songs to play!")
      await self.leave_channel()
    
  async def skip(self):
    if self.is_playing():
      self.get_client().stop()
      await self.send_msg('skib sonk')
    else:
      await self.send_msg("cant skip retard")

  async def leave_channel(self):
    if self.is_connected():
      await self.get_client().disconnect()

  async def pause(self):
    voice_client = self.get_client()
    if not voice_client or not voice_client.is_playing():
      await self.send_msg("I'm not playing retard")
      return
    if voice_client.is_paused():
      await self.send_msg("already paused retard")
      return
    voice_client.pause()
    await self.send_msg("paused")

  def is_paused(self):
    voice_client = self.get_client()
    if not voice_client:
      return False
    return voice_client.is_paused()

  async def resume(self):
    voice_client = self.get_client()
    if not voice_client or not voice_client.is_connected() or not voice_client.is_paused():
      await self.send_msg("Nothing paused to be resumed")
      return
    voice_client.resume()
    await self.send_msg("resumed")

  async def move_to(self, voice_channel):
    voice_client = self.get_client()
    if voice_client and voice_client.is_connected() and await voice_client.move_to(voice_channel):
      self.voice_channel = voice_channel

