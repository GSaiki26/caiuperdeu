'''
    A module to treat the timedelta.
'''
# Libs
from datetime import timedelta


# Methods
def treat_timedelta(time: timedelta) -> str:
    '''
        Method to get the time of the timedelta.
    '''
    seconds = get_seconds(time.total_seconds())
    minutes = get_minutes(time.total_seconds()/60)
    hours = get_hours(time.total_seconds()/3600)
    return f'{int(hours)}h {int(minutes)}m {int(seconds)}s'


def get_seconds(seconds: float) -> float:
    '''
        Method to get the seconds remaining from the minutes.
        Example 2 minutes and 30 seconds = 150 seconds.
        return 30 seconds.
    '''
    return seconds % 60


def get_minutes(minutes: float) -> float:
    '''
        Method to get the minutes remaining from the seconds.
    '''
    return minutes % 60


def get_hours(hours: float) -> float:
    '''
        Method to get the hours remaining from the minutes.
    '''
    return hours % 24
