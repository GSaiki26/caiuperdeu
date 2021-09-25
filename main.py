## Libs
import discord ## Discord.
from termcolor import colored ## Colored text.
from discord.ext import commands ## Discord.

## Local Libs

## CONSTANTS
TOKEN = input(colored('Please write the bot\'s token: ', 'cyan')) ## The constant to store the bot token.
DESCRIPTION = 'Made by Saiki#2044'
DESCRIPTION_URL = 'https://twitch.tv/GSaiki26'

## Data
bot = commands.Bot('!', None) ## Get the bot.
players = {} ## Dict to store the player

## Methods
def EmbedMessage(title: str, descr: str = ''): ## Create and return a embed message.
    embed = discord.Embed(title=title, description=descr, color=discord.Colour.from_rgb(192, 57, 43)) ## Create a embed message.
    return embed ## Return the embed message.

## Routes
@bot.event
async def on_ready():
    bot.change_presence(activity=discord.activity.Streaming(name=DESCRIPTION, url=DESCRIPTION_URL)) ## Change the description
    print(colored(f'[{bot.user}] is ready!','magenta'))

@bot.command('ping')
async def Ping(ctx: object):
    message = EmbedMessage('!ping', 'Um comando voltado ao Debug.') ## Get a embed message.
    message.add_field(name=f'{ctx.athor.guild}',value=f'{ctx.athor.guild.id}')
    await ctx.send(message) ## Send the message.

@bot.command('play')
async def Play(ctx: object):


@bot.command('history')
async def History(ctx: object):
    await ctx.send('Not ready.')

#3 Code
bot.run(TOKEN) ## Run the bot.