'''
    Method to write in the console.
'''
# Libs
from datetime import datetime

# Pip libs
from termcolor import colored

# Local libs
from config.config import Config

# Data
config = Config('CONSOLE')
COLOR_TEXT = config.get('color_text')
COLOR_INPUT = config.get('color_input')
COLOR_ERROR = config.get('color_error')


# Methods
def get_time() -> str:
    return datetime.now().strftime('%H:%M:%S')


# Classes
class Console:
    def __init__(self, **kwargs) -> None:
        '''
            `Kwargs`:
                * `time` (bool): The time of the message.
                * `prefix` (str): The prefix of the all message.
        '''
        self.__prefix = kwargs.get('prefix', '')
        self.__time: bool = kwargs.get('time', True)

    def write(self, text: str, **kwargs) -> None:
        '''
            Method to write in the console.
            `Kwargs`:
                * `color` (str): The color of the message.
                * `time` (bool): The time of the message.
                * `prefix` (str): The prefix of the all message.
        '''
        message = ''
        if kwargs.get('time', '') or self.__time:
            message += f'[{get_time()}] '

        prefix = kwargs.get('prefix', self.__prefix)
        if prefix:
            message += f'({prefix}) '

        message = colored(message+text, kwargs.get('color', COLOR_TEXT))
        print(message)

    def input(self, text: str, **kwargs) -> str:
        '''
            Method to get the input from the console.
            `Kwargs`:
                * `color` (str): The color of the message.
                * `prefix` (str): The prefix of the all message.
        '''
        message = ''
        message += f'[{get_time()}] '

        prefix = kwargs.get('prefix', self.__prefix)
        if prefix:
            message += f'({prefix}) '

        message = colored(text, COLOR_INPUT)
        return input(message)

    def error(self, text: str, **kwargs) -> None:
        '''
            Method to write in the console.
            `Kwargs`:
                * `prefix` (str): The prefix of the all message.
        '''
        message = ''
        message += f'[{get_time()}] '

        prefix = kwargs.get('prefix', self.__prefix)
        if prefix:
            message += f'({prefix}) '

        message = colored(text, COLOR_ERROR)
        print(message)
