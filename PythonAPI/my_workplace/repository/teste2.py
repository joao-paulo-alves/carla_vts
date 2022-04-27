import glob
import os
import sys
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
import pygame

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla

import random
import time
import numpy as np
import cv2

IM_WIDTH = 640
IM_HEIGHT = 480


def saving(s, z):
    xc = 0


def sensor_callback(sensor_data):
    i = np.array(sensor_data.raw_data)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3]
    sensor_queue.put(i3)
    cv2.imwrite('output/%6d.tiff', i3)
    return i3/255.0


actor_list = []
try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(20.0)

    world = client.get_world()

    settings = world.get_settings()

    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 1 / 60
    settings.max_substep_delta_time = 1 / 60

    world.apply_settings(settings)

    blueprint_library = world.get_blueprint_library()

    bp = blueprint_library.filter('model3')[0]
    print(bp)

    spawn_point = random.choice(world.get_map().get_spawn_points())

    vehicle = world.spawn_actor(bp, spawn_point)
    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
    # vehicle.set_autopilot(True)  # if you just wanted some NPCs to drive.

    actor_list.append(vehicle)

    # https://carla.readthedocs.io/en/latest/cameras_and_sensors
    # get the blueprint for this sensor
    blueprint = blueprint_library.find('sensor.camera.rgb')
    # change the dimensions of the image
    blueprint.set_attribute('image_size_x', f'{IM_WIDTH}')
    blueprint.set_attribute('image_size_y', f'{IM_HEIGHT}')
    blueprint.set_attribute('fov', '110')

    # Adjust sensor relative to vehicle
    spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))

    # spawn the sensor and attach to vehicle.
    sensor = world.spawn_actor(blueprint, spawn_point, attach_to=vehicle)

    # add sensor to list of actors
    actor_list.append(sensor)
    sensor_queue = Queue()
    # do something with this sensor
    sensor.listen(lambda data: sensor_callback(data))
    timer = 0
    i = 0
    executor = ThreadPoolExecutor(16)
    while True:
        world.tick()
        if timer > 5:
            break
        if sensor_queue.qsize() > 0:
            s = sensor_queue.get(True, 0.01)
            # timestamp[i] = s[2]
            # location[i] = Ego(s[3].location.x, s[3].location.y, s[3].location.z, s[3].rotation.yaw,
            #                  s[3].rotation.roll, s[3].rotation.pitch)
            f = executor.submit(saving, s, i)
            i = i + 1
        timer = timer + 1 / 60
        print(timer)



finally:
    world.tick()
    settings = world.get_settings()
    settings.synchronous_mode = False
    settings.no_rendering_mode = False
    settings.fixed_delta_seconds = None
    settings.max_substep_delta_time = 0.1
    world.apply_settings(settings)
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')
