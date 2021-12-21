# Libs
from typing import Dict, List

# Pip Libs
import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.member import Member

# Local Libs
from models.game import Game
from models.player import Player
from config.config import Config
from interface.console import Console
from utils.discord import create_embed_message, join_voice_chat

# Data
console = Console()
games: Dict[int, Game] = {}
bot = commands.Bot('!', None)

config = Config('DISCORD')
TOKEN = config.get('token')
DESCRIPTION = config.get('description')
DESCRIPTION_URL = config.get('description_url')


# Routes
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.activity.Streaming(
        name=DESCRIPTION, url=DESCRIPTION_URL))
    console.write(f'{bot.user} is ready!')


@bot.command('ping')
async def Ping(ctx: Context):
    message = await create_embed_message(
        '!ping', 'Um comando voltado ao Debug.')
    message.add_field(
        name=f'{ctx.author.guild}',
        value=f'{ctx.author.guild.id}')
    await ctx.send(embed=message)


@bot.command('play')
async def Play(ctx: Context):
    guild_id = ctx.author.guild.id
    if guild_id in games:
        console.error('Already running a game...')
        await create_embed_message(
            'Error', 'Já estou em uma partida!! ಠ_ಠ', ctx)

    try:
        await ctx.voice_client.disconnect()
    except AttributeError:
        pass  # Voice_client not defined.

    # Join the voice chat.
    channel = await join_voice_chat(ctx)
    await create_embed_message('!Play', 'Começando o jogo... (｡◕‿◕｡)', ctx)
    members: List[Member] = channel.members

    # Create the players.
    players_dict: dict[Member, Player] = {}
    for member in members:
        if not member.bot:
            players_dict[f'{member}'] = Player(member)

    # Start the game.
    game = Game(ctx, channel, players_dict)
    await game.run()

    # Exit the voice chat.
    await ctx.voice_client.disconnect()


@bot.command('help')
async def Help(ctx: Context):
    message = await create_embed_message('Ajuda')
    message.add_field(
        name='!ping', value='Um comando usado no debug.'
                            'Não tem uma função exata.')
    message.add_field(name='!play', value='O comando para começar o jogo.')
    ctx.send(embed=message)


# Code
bot.run(TOKEN)
