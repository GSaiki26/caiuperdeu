# Libs
import os
from json import loads
from pathlib import Path
from configparser import ConfigParser

# data
config_path = Path(
    os.path.dirname(os.path.realpath(__file__)), '.conf').absolute()


# Classes
class Config:
    def __init__(self, section: str) -> None:
        self.__section = section
        self.__config = ConfigParser()
        self.__config.read(config_path)
        self.add_section(section)

    def get(self, key: str, return_if_null: any = None,
            convert_value: bool = True) -> str:
        '''
            Method to get a value from the config file.
        '''
        if self.__config.has_option(self.__section, key):
            value = self.__config.get(self.__section, key)
            if convert_value:
                return loads(value)
            return value
        self.__config.set(self.__section, key, '""')
        self.__save()
        return return_if_null

    def set(self, key: str, value: any) -> None:
        '''
            Method to set a value in the config file.
        '''
        self.__config.set(self.__section, key, str(value))
        self.__save()

    def add_section(self, section: str) -> None:
        if not self.__config.has_section(section):
            self.__config.add_section(section)
            self.__save()
            print(f'The section {section} doesn\'t exist!')

    def __save(self) -> None:
        self.__config.write(open(config_path, 'w'))
