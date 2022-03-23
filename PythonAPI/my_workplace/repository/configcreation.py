from configparser import ConfigParser
import random

config = ConfigParser()

config['worldsettings'] = {










    'host': '127.0.0.1',
    'port': 2000,
    'safe': True,
    'filterv': 'vehicle.*',
    'generationv': 'All',
    'filterw': 'walker.pedestrian.*',
    'generationw': '2',
    'tm_port': 8000,
    'asynch': False,
    'hybrid': True,
    'seedw': 0,
    'car_lights_on': False,
    'hero': True,
    'respawn': False,
    'no_rendering': False
}

with open('../config.ini', 'w') as f:
    config.write(f)