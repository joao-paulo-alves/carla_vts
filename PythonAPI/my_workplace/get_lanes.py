import glob
import os
import sys
import time
from math import cos, sin, atan2
import carla
import imageio
from carla import VehicleLightState as vls
import logging
from numpy import random
from queue import Queue
from configparser import ConfigParser
from concurrent.futures import ThreadPoolExecutor
import os
import random
import time
import numpy as np
import cv2
import atexit
import imageio
import transforms3d
# import time
from tqdm import tqdm
import pygame
import math
from PIL import Image
from carla_agents.agents.navigation.basic_agent import BasicAgent
from carla_agents.agents.navigation.basic_agent import BasicAgent
from carla_agents.agents.navigation.behavior_agent import BehaviorAgent
import matplotlib.pyplot as plt
def main():
    # SETTING CLIENT
    client = carla.Client('localhost', 2000)
    client.set_timeout(60.0)

    # SET A SPECIFIED SCENARIO
    world = client.load_world('Town04')
    world_data = world.get_map()
    spectator = world.get_spectator()
    # GET ALL THE BLUEPRINTS
    blueprint_library = world.get_blueprint_library()
    lib_car = world.get_blueprint_library().filter('vehicle.*')
    lib_walker = world.get_blueprint_library().filter('walker.pedestrian.*')

    # GET ALL THE RECOMMENDED SPAWN LOCATIONS FOR VEHICLES
    spawn_points = world.get_map().get_spawn_points()

    # CREATE TRAFFIC MANAGER INSTANCE
    traffic_manager = client.get_trafficmanager()
    tm_port = traffic_manager.get_port()
    # SYNCH MODE FOR INCREASED TRAFFIC_MANAGER STABILITY
    init_settings = world.get_settings()
    settings = world.get_settings()
    settings.synchronous_mode = True
    traffic_manager.set_synchronous_mode(True)
    settings.fixed_delta_seconds = 1 / 60
    settings.max_substep_delta_time = 1 / 60
    world.apply_settings(settings)

    attr = blueprint_library.find('vehicle.tesla.model3')
    ego_car = world.spawn_actor(attr, spawn_points[1])

    attr = blueprint_library.find('sensor.camera.rgb')
    attr.set_attribute('image_size_x', '1277')
    attr.set_attribute('image_size_y', '370')
    attr.set_attribute('sensor_tick', str(1 / 10))
    sensor_location = carla.Location(1, 0, 1.2)
    sensor_rotation = carla.Rotation(8.75, 0, 0)
    transform = carla.Transform(sensor_location, sensor_rotation)
    sensor = world.spawn_actor(attr, transform, attach_to=ego_car,
                               attachment_type=carla.AttachmentType.Rigid)
    ego_car.set_autopilot(True, tm_port)
    spectator.set_transform(ego_car.get_transform())
    left_boundary = []
    center_boundary = []
    right_boundary = []
    timer = 0

    while True:
        world.tick()
        waypoint = world_data.get_waypoint(ego_car.get_location(), project_to_road=True, lane_type=(carla.LaneType.Driving))
        center_boundary.append(waypoint)


        timer = timer + 1 / 60

        if timer > 30:
            break
        print(timer)
    world.tick()
    settings = world.get_settings()
    settings.synchronous_mode = False
    settings.no_rendering_mode = False
    settings.fixed_delta_seconds = None
    settings.max_substep_delta_time = 0.1
    world.apply_settings(settings)


    for i in center_boundary:
        world.debug.draw_string(i.transform.location, 'O', draw_shadow=False,
                                color=carla.Color(r=0, g=255, b=0), life_time=120,
                                persistent_lines=True)
        if i.get_left_lane() is not None:
            world.debug.draw_string(i.get_left_lane().transform.location, 'O', draw_shadow=False,
                                color=carla.Color(r=0, g=0, b=255), life_time=120,
                                persistent_lines=True)
        if i.get_right_lane() is not None:
            world.debug.draw_string(i.get_right_lane().transform.location, 'O', draw_shadow=False,
                                color=carla.Color(r=255, g=0, b=0), life_time=120,
                                persistent_lines=True)






if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')
