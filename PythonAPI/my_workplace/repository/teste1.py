import carla
import carla_agents
from carla import *
import numpy
import pygame
import random

from carla_agents.agents.navigation.basic_agent import BasicAgent
from carla_agents.agents.navigation.behavior_agent import BehaviorAgent


def main():
    # SETTING CLIENT
    client = carla.Client('localhost', 2000)
    client.set_timeout(300.0)

    # SET A SPECIFIED SCENARIO
    world = client.load_world('Town10HD')
    # GET THE CURRENT SCENARIO
    # world = client.get_world()

    # -------------------------------Main Vehicle Spawn---------------------------------------------#
    # GET ALL THE BLUEPRINTS
    blueprint_library = world.get_blueprint_library()

    # SETTING UP MAIN ACTOR
    vehicle_main = blueprint_library.find('vehicle.tesla.model3')
    sensor = blueprint_library.find('sensor.camera.rgb')
    sensor.set_attribute('image_size_x', '1820')
    sensor.set_attribute('image_size_y', '561')
    sensor.set_attribute('fov', '110')
    sensor.set_attribute('fstop', '1.6')

    # GET ALL THE RECOMMENDED SPAWN LOCATIONS FOR VEHICLES
    spawn_points = world.get_map().get_spawn_points()
    spectator = world.get_spectator()
    x = 0
    for x, transform in enumerate(spawn_points):
        spectator.set_transform(carla.Transform(spawn_points[x].location+ carla.Location(z=25),
                                                carla.Rotation(pitch=-90)))
        input(x)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')
