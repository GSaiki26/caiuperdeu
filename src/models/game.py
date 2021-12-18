'''
    A module for the game match.
'''
# Libs
from time import sleep
from datetime import datetime
from typing import Dict, Tuple

# pip Libs
import discord
from discord.member import Member
from discord.channel import VoiceChannel
from discord.ext.commands.context import Context

# Local Libs
from config.config import Config
from models.player import Player
from interface.console import Console
from utils.discord import create_embed_message
from utils.treat_timedelta import treat_timedelta

# Data
console = Console(prefix='Game')
config = Config('GAME')


# Classes
class Game:
    def __init__(self, ctx: Context, channel: VoiceChannel,
                 players_dict: Dict[Member, Player]) -> None:
        self.__ctx = ctx
        self.__alive_player = len(players_dict.keys())
        self.__inittime = datetime.now()
        self.__delay: int = config.get('delay')
        self.__players: Dict[Member, Player] = players_dict

    async def run(self) -> None:
        '''
            Method to run the game.
        '''
        status_message: discord.message.Message = await self.__ctx.send(
            embed=await self.__get_status_message())

        if await self.__is_check_match(status_message):
            console.write('End of the game!')
            return

        while True:
            sleep(self.__delay)
            await status_message.edit(embed=await self.__get_status_message())

            console.write('Checking alive players...')
            for player_member, player_obj in self.__players.items():
                await self.__is_player_alive(player_member, player_obj)

            if await self.__is_check_match(status_message):
                console.write('End of the game!')
                break

    async def __get_status_message(self,
                                   finished: bool = False) -> discord.Embed:
        time = treat_timedelta(datetime.now() - self.__inittime)
        if finished:
            match_title = '[Finalizado] '
        match_title = f'Tempo da partida: [{time}]'
        message = await create_embed_message(match_title)
        for player_name, player_obj in self.__players.items():
            message.add_field(
                name=player_name,
                value=(
                    'Status: '
                    ':heart: ' if player_obj.alive else ':broken_heart: '
                    f'Tempo: {player_obj.get_player_time()}'),
                inline=False)
        return message

    async def __is_player_alive(self, player_member: Member,
                                player_obj: Player) -> bool:
        '''
            Method to check if the player is alive.
        '''
        if player_obj.member not in self.__ctx.voice_client.channel.members:
            self.__alive_player -= 1
            player_obj.kill()
            self.__players[player_member] = player_obj
            console.write(f'Player {player_member} is not alive.')
            return False
        return True

    async def __find_last_player(self) -> Player:
        '''
            Method to find the last player alive.
        '''
        for player_obj in self.__players.values():
            if player_obj.alive:
                return player_obj
        return None  # Return none if all the players are dead.

    async def __is_check_match(
            self, status_message: discord.message.Message) -> None:
        '''
            Method to check if the match is finished.
        '''
        if self.__alive_player <= 1:
            console.write('Game finished!')
            await status_message.edit(
                embed=await self.__get_status_message(True))
            last_player = await self.__find_last_player()
            if not last_player:
                message: Tuple[str, str] = (
                    'Empate? (╬ ಠ益ಠ)',
                    'Mas cadê todo mundo? Acho que deu empate para os '
                    'ultimos finalistas... :sob::sleepy:')
            else:
                last_player.kill()
                message: Tuple[str, str] = (
                    'Vitória ( ˘ ³˘)♥',
                    f'O player `@{last_player.member}` ganhou com um tempo de '
                    f'{last_player.get_player_time()}!! '
                    ':clap::clap::heart:')
            await create_embed_message(*message, self.__ctx)
            await create_embed_message('Match', 'Saindo...', self.__ctx)
            return True
        return False
