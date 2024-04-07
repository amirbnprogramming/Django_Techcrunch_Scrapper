import logging

from .logger import info_log


def function_caller(function):
    def wrapper(*args, **kwargs):
        # info_log.log(f'Start Scraping function ({function.__name__})')
        print(f'Start Scraping function ({function.__name__})')
        return function(*args, **kwargs)

    return wrapper
