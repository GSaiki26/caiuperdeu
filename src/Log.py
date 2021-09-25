## Libs
from termcolor import colored

## Local Libs
from src.Time import GetTime

## Methods
def Write(text:str, color:str = 'magenta'): ## Method to write colored text.
    print(colored(f'[{GetTime()}] {text}', color))