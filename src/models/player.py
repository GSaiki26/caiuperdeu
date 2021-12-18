'''
    The model to manage the players.
'''
# Libs
from typing import Union
from datetime import datetime, timedelta

# Pip libs
from discord.member import Member

# local Libs
from utils.treat_timedelta import treat_timedelta


# Classes
class Player:
    def __init__(self, discord_member: Member) -> None:
        self.alive = True
        self.member = discord_member
        self.__inittime = datetime.now()
        self.__endtime = None

    def get_player_time(self) -> Union[str, timedelta]:
        return treat_timedelta(self.__endtime - self.__inittime)

    def kill(self) -> None:
        self.alive = False
        self.__endtime = datetime.now()
