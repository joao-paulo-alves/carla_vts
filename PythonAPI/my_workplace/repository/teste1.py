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
import numpy as np
import os
import cv2

IM_WIDTH = 1422
IM_HEIGHT = 889
zxc = 0


def saving(s):
    zxc = +1
    i = np.array(s[0].raw_data)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3]
    cv2.imwrite('output/%06d.raw' % zxc, i3 / 255.0)
    return i3 / 255.0
    # s[0].save_to_disk('output/%06d.png' % s[1])
    # i = 1


def process_img(image):
    i = np.array(image.raw_data)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, 3]
    cv2.imshow("", i3)
    cv2.waitKey(1)
    return i3 / 255.0


def main():
    # SETTING CLIENT
    client = carla.Client('localhost', 2000)
    client.set_timeout(300.0)
    parser = ConfigParser()
    parser.read('config.ini')
    # SET A SPECIFIED SCENARIO
    world = client.load_world('Town10HD')
    # GET THE CURRENT SCENARIO
    # world = client.get_world()

    settings = world.get_settings()

    synchronous_master = True
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 1 / 60
    settings.max_substep_delta_time = 1 / 60
    world.apply_settings(settings)
    # -------------------------------Main Vehicle Spawn---------------------------------------------#
    # GET ALL THE BLUEPRINTS
    blueprint_library = world.get_blueprint_library()

    # SETTING UP MAIN ACTOR
    vehicle_main = blueprint_library.find('vehicle.tesla.model3')
    attr = blueprint_library.find(parser.get('sensorsettings', 'bp'))
    attr.set_attribute('enable_postprocess_effects', parser.get('sensorsettings', 'enable_postprocess_effects'))
    # Basic camera attributes
    attr.set_attribute('bloom_intensity', parser.get('sensorsettings', 'bloom_intensity'))
    attr.set_attribute('fov', parser.get('sensorsettings', 'fov'))
    attr.set_attribute('fstop', parser.get('sensorsettings', 'fstop'))
    attr.set_attribute('image_size_x', parser.get('sensorsettings', 'image_size_x'))
    attr.set_attribute('image_size_y', parser.get('sensorsettings', 'image_size_y'))
    attr.set_attribute('iso', parser.get('sensorsettings', 'iso'))
    attr.set_attribute('gamma', parser.get('sensorsettings', 'gamma'))
    attr.set_attribute('lens_flare_intensity', parser.get('sensorsettings', 'lens_flare_intensity'))
    attr.set_attribute('sensor_tick', parser.get('sensorsettings', 'sensor_tick'))
    attr.set_attribute('shutter_speed', parser.get('sensorsettings', 'shutter_speed'))

    # Camera lens distortion attributes
    attr.set_attribute('lens_circle_falloff', parser.get('sensorsettings', 'lens_circle_falloff'))
    attr.set_attribute('lens_circle_multiplier', parser.get('sensorsettings', 'lens_circle_multiplier'))
    attr.set_attribute('lens_k', parser.get('sensorsettings', 'lens_k'))
    attr.set_attribute('lens_kcube', parser.get('sensorsettings', 'lens_kcube'))
    attr.set_attribute('lens_x_size', parser.get('sensorsettings', 'lens_x_size'))
    attr.set_attribute('lens_y_size', parser.get('sensorsettings', 'lens_y_size'))

    # Advanced camera attributes
    attr.set_attribute('min_fstop', parser.get('sensorsettings', 'min_fstop'))
    attr.set_attribute('blade_count', parser.get('sensorsettings', 'blade_count'))
    attr.set_attribute('exposure_mode', parser.get('sensorsettings', 'exposure_mode'))
    attr.set_attribute('exposure_compensation', parser.get('sensorsettings', 'exposure_compensation'))
    attr.set_attribute('exposure_min_bright', parser.get('sensorsettings', 'exposure_min_bright'))
    attr.set_attribute('exposure_max_bright', parser.get('sensorsettings', 'exposure_max_bright'))
    attr.set_attribute('exposure_speed_up', parser.get('sensorsettings', 'exposure_speed_up'))
    attr.set_attribute('exposure_speed_down', parser.get('sensorsettings', 'exposure_speed_down'))
    attr.set_attribute('calibration_constant', parser.get('sensorsettings', 'calibration_constant'))
    attr.set_attribute('focal_distance', parser.get('sensorsettings', 'focal_distance'))
    attr.set_attribute('blur_amount', parser.get('sensorsettings', 'blur_amount'))
    attr.set_attribute('blur_radius', parser.get('sensorsettings', 'blur_radius'))
    attr.set_attribute('motion_blur_intensity', parser.get('sensorsettings', 'motion_blur_intensity'))
    attr.set_attribute('motion_blur_max_distortion', parser.get('sensorsettings', 'motion_blur_max_distortion'))
    attr.set_attribute('motion_blur_min_object_screen_size',
                       parser.get('sensorsettings', 'motion_blur_min_object_screen_size'))
    attr.set_attribute('slope', parser.get('sensorsettings', 'slope'))
    attr.set_attribute('toe', parser.get('sensorsettings', 'toe'))
    attr.set_attribute('shoulder', parser.get('sensorsettings', 'shoulder'))
    attr.set_attribute('black_clip', parser.get('sensorsettings', 'black_clip'))
    attr.set_attribute('white_clip', parser.get('sensorsettings', 'white_clip'))
    attr.set_attribute('temp', parser.get('sensorsettings', 'temp'))
    attr.set_attribute('tint', parser.get('sensorsettings', 'tint'))
    attr.set_attribute('chromatic_aberration_intensity', parser.get('sensorsettings', 'chromatic_aberration_intensity'))
    attr.set_attribute('chromatic_aberration_offset', parser.get('sensorsettings', 'chromatic_aberration_offset'))

    sensor_location = carla.Location(1, 0, 1.2)
    sensor_rotation = carla.Rotation(8.75, 0, 0)
    sensor_transform = carla.Transform(sensor_location, sensor_rotation)

    # GET ALL THE RECOMMENDED SPAWN LOCATIONS FOR VEHICLES
    spawn_points = world.get_map().get_spawn_points()
    actor = world.spawn_actor(vehicle_main, spawn_points[1])
    sensor = world.spawn_actor(attr, sensor_transform, attach_to=actor)
    timer = 0
    spectator = world.get_spectator()
    transform = actor.get_transform()
    spectator.set_transform(carla.Transform(transform.location,
                                            transform.rotation))
    while True:
        world.tick()
        timer += 1 / 60
        if timer > 1:
            break
    timer = 0
    sensor_queue = Queue()
    executor = ThreadPoolExecutor(16)

    sensor.listen(lambda data: process_img(data))
    actor.set_autopilot(True)
    while True:
        spectator = world.get_spectator()
        transform = actor.get_transform()
        spectator.set_transform(carla.Transform(transform.location,
                                                transform.rotation))
        world.tick()

        if timer > 10:
            break

        # if sensor_queue.qsize() > 0:
        #     s = sensor_queue.get(True, 0.01)
        #     f = executor.submit(saving, s)
        timer += 1 / 60

    world.tick()
    settings = world.get_settings()
    settings.synchronous_mode = False
    settings.no_rendering_mode = False
    settings.fixed_delta_seconds = None
    settings.max_substep_delta_time = 0.1
    world.apply_settings(settings)
    time.sleep(2)


if __name__ == '__main__':
    try:
        main()


    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')
