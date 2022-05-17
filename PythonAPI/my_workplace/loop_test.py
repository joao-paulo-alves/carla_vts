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

IM_WIDTH = 1277
IM_HEIGHT = 370
images = []


class Ego:
    def __init__(self, x, y, z, yaw, pitch, roll):
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.roll = roll
        self.pitch = pitch


def sensor_callback(sensor_data, sensor_queue, timer, all_vehicle_actors):
    ego_location = all_vehicle_actors.get_transform()
    sensor_queue.put((sensor_data, timer, ego_location))


def saving(s, x):
    i = np.array(s[0].raw_data, dtype='uint8')
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3]
    im_rgb = cv2.cvtColor(i3, cv2.COLOR_BGR2GRAY)
    # dim = (1277, 370)
    # resized = cv2.resize(im_rgb, dim, interpolation=cv2.INTER_AREA)
    Image.fromarray(im_rgb).save('output/%06d.png' % x)
    # cv2.imwrite('output/%06d.png' % x, im_rgb)
    images.append(im_rgb)


# ---------------------------------------Global-----------------------------
# SETTING CLIENT
client = carla.Client('localhost', 2000)
client.set_timeout(60.0)

# SET A SPECIFIED SCENARIO
world = client.load_world('Town10HD')

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


def main():
    attr = blueprint_library.find('vehicle.tesla.model3')
    ego_car = world.spawn_actor(attr, spawn_points[88])

    attr = blueprint_library.find('sensor.camera.rgb')
    attr.set_attribute('image_size_x', '1277')
    attr.set_attribute('image_size_y', '370')
    attr.set_attribute('sensor_tick', str(1 / 10))
    sensor_location = carla.Location(1, 0, 1.2)
    sensor_rotation = carla.Rotation(8.75, 0, 0)
    transform = carla.Transform(sensor_location, sensor_rotation)
    sensor = world.spawn_actor(attr, transform, attach_to=ego_car,
                               attachment_type=carla.AttachmentType.Rigid)

    timer = 0
    while True:
        world.tick()
        timer += 1 / 60
        if timer > 1:
            break

    spectator = world.get_spectator()
    agent = BasicAgent(ego_car)
    set_dest = 3
    agent.set_destination((spawn_points[118]).location)
    world.tick()

    sensor_queue = Queue()
    timer = 0
    i = 0
    executor = ThreadPoolExecutor(16)
    timestamp = []
    location = []
    sensor.listen(lambda data: sensor_callback(data, sensor_queue, timer, ego_car))
    end = 0
    while True:
        world.tick()
        if agent.done():

            if set_dest == 0:
                agent.set_destination((spawn_points[69]).location)
                set_dest = 1
                print("Setting to 1")
            elif set_dest == 1:
                agent.set_destination((spawn_points[88]).location)
                set_dest = 2
                print("Setting to 2")
            elif set_dest == 2:
                agent.set_destination((spawn_points[118]).location)
                set_dest = 3
                print("Setting to 3")
            elif set_dest == 3:
                agent.set_destination((spawn_points[53]).location)
                set_dest = 0
                end = end + 1
                print("Setting to 0")
        ego_car.apply_control(agent.run_step())
        transform = sensor.get_transform()
        spectator.set_transform(carla.Transform(transform.location,
                                                transform.rotation))

        if timer > 300:
            break
        if end == 2:
            break

        if sensor_queue.qsize() > 0:
            s = sensor_queue.get(True, 0.01)
            # if s[2].rotation.yaw < 0:
            #     s[2].rotation.yaw = (s[2].rotation.yaw + 180) * (-1)
            # elif s[2].rotation.yaw > 0:
            #     s[2].rotation.yaw = (s[2].rotation.yaw - 180) * (-1)
            timestamp.append(s[1])
            location.append(Ego(-s[2].location.x, s[2].location.y, s[2].location.z, -s[2].rotation.yaw,
                                s[2].rotation.roll, s[2].rotation.pitch))
            f = executor.submit(saving, s, i)
            i = i + 1
        timer += 1 / 60

    world.tick()
    sensor.destroy()

    settings = world.get_settings()
    settings.synchronous_mode = False
    settings.no_rendering_mode = False
    settings.fixed_delta_seconds = None
    settings.max_substep_delta_time = 0.1
    world.apply_settings(settings)

    file = open("times.txt", "w+")
    f = open("times.txt", "w+")
    time = []
    for x in timestamp:
        time_origin = timestamp[0]
        if x is not None:
            x = float(x - time_origin)
            scientific_notation = "{:e}".format(x)
            f.write("%s\n" % scientific_notation)
            time.append(scientific_notation)

    f.close()

    file = open("base_coordinates.txt", "w+")
    f = open("base_coordinates.txt", "w+")
    for x in location:
        if x is not None:
            f.write("%f, %f, %f, %f, %f, %f\n" % (x.x, x.y, x.z, x.yaw, x.roll, x.pitch))
    f.close()

    reformed_location = []
    origin = location[0]
    i = 0
    for x in location:
        if x is not None:
            reformed_location.append(Ego(x.x - origin.x, x.y - origin.y,
                                         x.z - origin.z, x.yaw,
                                         x.roll,
                                         x.pitch))
    # <>
    newloc = []

    for x in reformed_location:
        theta = math.radians(location[0].yaw - 90)
        xx = x.x
        yy = x.y
        x1 = xx * math.cos(theta) - yy * math.sin(theta)
        y1 = xx * math.sin(theta) + yy * math.cos(theta)
        newloc.append(Ego(x1, y1,
                          x.z, x.yaw,
                          x.roll,
                          x.pitch))

    file = open("GT_coordinates.txt", "w+")
    f = open("GT_coordinates.txt", "w+")
    i = 0
    for x in newloc:
        if x is not None:
            f.write("%s, %f, %f, %f, %f, %f, %f\n" % (time[i], x.x, x.y, x.z, x.yaw, x.roll, x.pitch))
        i = i + 1
    f.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')
