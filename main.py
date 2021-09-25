## Libs
from time import sleep, strftime, gmtime
import discord ## Discord.
from termcolor import colored ## Colored text.
from discord.ext import commands ## Discord.

## Local Libs
from src.Time import Timer
from src.Log import Write as log

## CONSTANTS
TOKEN = input(colored('Please write the bot\'s token: ', 'cyan')) ## The constant to store the bot token.
DESCRIPTION = 'Made by Saiki#2044'
DESCRIPTION_URL = 'https://twitch.tv/GSaiki26'

## Data
bot = commands.Bot('!', None) ## Get the bot.
players = {} ## Dict to store the player

## Sup Methods
def TreatTime(seconds: float) -> str: ## Return a stringify time.
    return strftime('%H:%M:%S', gmtime(seconds))

## Methods
async def EmbedMessage(title: str, descr: str = '', ctx: object = None) -> discord.Embed: ## Create and return a embed message.
    embed = discord.Embed(title=title, description=descr, color=discord.Colour.from_rgb(192, 57, 43)) ## Create a embed message.
    if ctx:
        await ctx.send(embed=embed)
    return embed ## Return the embed message.

async def JoinVoiceChat(ctx: object): ## Method to join the author's voice chat.
    log('Joining voice chat...')
    channel = ctx.author.voice.channel ## Get the voice channel.
    if ctx.voice_client is None:
        await channel.connect() ## Connect to the voice chat.
    else:
        await ctx.voice_client.move_to(channel) ## Join to the voice chat.
    ##await channel.connect() ## Join the voice chat.
    return channel ## Return the channel

def AddMembersToPlayers(GUILDID: int, members): ## Method to add the Members of the voice chat to Players variable.
    global players ## get the global players.
    log('Adding members to Players..')
    members_dict = {}
    for member in members:
        print(member)
        if not member.bot:
            members_dict[member] = {
                'Alive': True,
                'Timer': Timer()
            }
            members_dict[member]['Timer'].Start()
    players[GUILDID] = members_dict

async def GetGameMessage(ctx: object, gameTimer: object): ## Method to write the game message.
    ## Data
    global players
    GUILDID = ctx.author.guild.id ## Get the guild id.

    log('Game: Writting the message...')
    ## Threat the current time.
    time = TreatTime(gameTimer.GetTime()) ## Convert the seconds to the hours format.
    ## Write the players.
    message = await EmbedMessage(f'Tempo da partida: [{time}]') ## Create a embed message.
    for item in players[GUILDID].items(): ## Foreach player.
        ## get the current item.
        playerKey = item[0]; playerValues = item[1] ## Get the players info.
        status = ':heart:' if playerValues['Alive'] else f':broken_heart: Tempo: {playerValues["Timer"].GetTime()}' ## Write the status.
        message.add_field(name=playerKey, value=f'Status: {status}', inline=False) ## Add the field to the embed message.
    return message

async def StartGame(ctx: object, channel): ## game.
    ## Data
    GUILDID = ctx.author.guild.id ## Get the guild id.
    gameMessage = '' ## ## The variable to store the gameMessage, with status and time foreach player.
    gameTimer = Timer(); gameTimer.Start()

    ## GameLoop.
    while True: ## The Main loop until someone wins.
        if gameMessage:
            await gameMessage.edit(embed=await GetGameMessage(ctx, gameTimer))
        else:
            gameMessage = await ctx.send(embed=await GetGameMessage(ctx, gameTimer)) ## Send message to discord.
        log('Game: Check alive players...')

        ## Check players.
        playersCount = [] ## The count of the current players playing. 
        for player in players[GUILDID].items():
            if player[0] not in channel.members:
                players[GUILDID][player[0]].update({'Alive':False}) ## Define the alive to false.
            else:
                playersCount.append(player)
        if len(playersCount) <= 0: ## Check if the amount of player is zero or below.
            await gameMessage.edit(embed=await GetGameMessage(ctx, gameTimer))
            await EmbedMessage('Empate? (╬ ಠ益ಠ)',f'Mas cadê todo mundo? Acho que deu empate para os dois ultimos finalistas... :sob::sleepy:',ctx); del players[GUILDID]; break ## Break the game.
        if len(playersCount) == 1: ## Check if there's a winner.
            await gameMessage.edit(embed=await GetGameMessage(ctx, gameTimer))
            await EmbedMessage('Vitória ( ˘ ³˘)♥',f'O player `@{playersCount[0][0]}` ganhou com um tempo de {TreatTime(playersCount[0][1]["Timer"].GetTime())}!! :clap::clap::heart:',ctx)
            del players[GUILDID]; break ## Break the game.
        log('Sleeping...')
        sleep(5) ## Sleep
    await ctx.voice_client.disconnect() ## Exit from the voice chat.
    await EmbedMessage('Match','Saindo...')
    log('End of the game!')
## Routes
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.activity.Streaming(name=DESCRIPTION, url=DESCRIPTION_URL)) ## Change the description
    log(f'[{bot.user}] is ready!')

@bot.command('ping')
async def Ping(ctx: object):
    message = await EmbedMessage('!ping', 'Um comando voltado ao Debug.') ## Get a embed message.
    message.add_field(name=f'{ctx.author.guild}',value=f'{ctx.author.guild.id}')
    await ctx.send(embed=message) ## Send the message.

@bot.command('play')
async def Play(ctx: object):
    global players
    ## Data
    GUILDID = ctx.author.guild.id ## get the guildid.
    try:
        players[GUILDID]
    except:
        pass
    else:
        log('Error: Already running a game...', 'red')
        await EmbedMessage('Error','Já estou em uma partida!! ಠ_ಠ', ctx); return ## Create an embed message.
    try:
        await ctx.voice_client.disconnect() ## Leave the voice chat
    except:
        pass

    ## Join the voice chat. [Just to go there...]
    channel = await JoinVoiceChat(ctx)
    await EmbedMessage('!Play', 'Começando o jogo... (｡◕‿◕｡)', ctx) ## Send the message.
    members = channel.members ## Get the members in the voice chat.

    ## Add the members to players variable.
    AddMembersToPlayers(GUILDID, members)
    ## Sttar the Game
    await StartGame(ctx, channel)

@bot.command('history')
async def History(ctx: object):
    await ctx.send('Not ready.')

#3 Code
bot.run(TOKEN) ## Run the bot.