import carla
import carla_agents
from carla import *
import numpy
import pygame
import random
import keyboard
import time

# ---------------------------------------Global-----------------------------
# SETTING CLIENT
client = carla.Client('localhost', 2000)
client.set_timeout(300.0)

# SET A SPECIFIED SCENARIO
world = client.load_world('Town03')

# GET ALL THE RECOMMENDED SPAWN LOCATIONS FOR VEHICLES
spawn_points = world.get_map().get_spawn_points()
i_len = len(spawn_points)


def main():
    loc_init = carla.Transform(Location(x=0, y=0, z=10))
    spectator = world.get_spectator()
    spectator.set_transform(carla.Transform(loc_init.location))
    i = 0
    while True:
        if keyboard.read_key() == "d":  # if key 'q' is pressed
            spectator.set_transform(carla.Transform(loc_init.location + Location(y=1)))
            loc_init = carla.Transform(loc_init.location + Location(y=1))

        elif keyboard.read_key() == "a":
            spectator.set_transform(carla.Transform(loc_init.location + Location(y=-1)))
            loc_init = carla.Transform(loc_init.location + Location(y=-1))

        elif keyboard.read_key() == "w":
            spectator.set_transform(carla.Transform(loc_init.location + Location(x=1)))
            loc_init = carla.Transform(loc_init.location + Location(x=1))

        elif keyboard.read_key() == "s":
            spectator.set_transform(carla.Transform(loc_init.location + Location(x=-1)))
            loc_init = carla.Transform(loc_init.location + Location(x=-1))

        elif keyboard.read_key() == "x":
            print(loc_init)

        elif keyboard.read_key() == "q":
            i = i - 1
            if i < 0:
                i = 0
            spectator.set_transform(spawn_points[i])
            print(i)

        elif keyboard.read_key() == "e":
            i = i + 1
            if i > i_len - 1:
                i = i_len - 1
            spectator.set_transform(spawn_points[i])
            print(i)

        elif keyboard.read_key() == "z":
            break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')
