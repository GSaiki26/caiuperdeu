'''
    A module to quick do some tasks from discord lib.
'''
# Pip libs
import discord
from discord.ext.commands.context import Context
from discord.channel import VoiceChannel

# Local libs
from interface.console import Console

# Data
console = Console()


# Methods
async def create_embed_message(title: str, descr: str = '',
                               ctx: Context = None) -> discord.Embed:
    '''
        Method to create a embed message.
    '''
    embed_message = discord.Embed(title=title, description=descr,
                                  color=discord.Colour.from_rgb(192, 57, 43))
    if ctx:
        await ctx.send(embed=embed_message)
    return embed_message


async def join_voice_chat(ctx: Context) -> VoiceChannel:
    '''
        Method to join a voice chat.
    '''
    console.write('Joining voice chat...')
    channel: VoiceChannel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await channel.connect()
    else:
        await ctx.voice_client.move_to(channel)
    return channel
