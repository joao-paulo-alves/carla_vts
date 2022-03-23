import carla
from carla import *
import numpy
import pygame
import argparse
import random
import time


class Walker:
    def __init__(self):
        self.total_number = 20
        self.total_blueprint = 48


def random_attribution(total_number, total_blueprint, library, world, spawn_points):
    pos_rel = 2
    number = random.randrange(total_number)
    pedestrian_list = [0] * number
    for inc in pedestrian_list:
        base_command = 'walker.pedestrian.00'
        number = random.randrange(total_blueprint)
        while number == 0:
            number = random.randrange(total_blueprint)
        if number < 10:
            base_command = 'walker.pedestrian.000'
        base_command += str(number)
        pedestrian_id = library.find(base_command)
        info = world.try_spawn_actor(pedestrian_id, carla.Transform(
            spawn_points[0].location + carla.Location(x=pos_rel, z=-0.5),
            carla.Rotation(yaw=spawn_points[0].rotation.yaw, roll=spawn_points[0].rotation.roll,
                           pitch=spawn_points[0].rotation.pitch)))
        if info is not None:
            pedestrian_list[inc] = info.id
        pos_rel = pos_rel + 2
        world.wait_for_tick()


def main():
    vehicles_list = []

    all_id = []

    # SETTING CLIENT
    client = carla.Client('localhost', 2000)
    client.set_timeout(30.0)

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
    y = 0

    main_actor = world.spawn_actor(vehicle_main,
                                   carla.Transform(spawn_points[0].location + carla.Location(z=-0.5),
                                                   carla.Rotation(yaw=spawn_points[0].rotation.yaw,
                                                                  roll=spawn_points[0].rotation.roll,
                                                                  pitch=spawn_points[0].rotation.pitch)))
    sensor_location = carla.Location(0.4, 0, 1.2)
    sensor_rotation = carla.Rotation(8.75, 0, 0)
    sensor_transform = carla.Transform(sensor_location, sensor_rotation)
    camera = world.spawn_actor(sensor, sensor_transform, attach_to=main_actor,
                               attachment_type=carla.AttachmentType.Rigid)

    spectator = world.get_spectator()
    transform = main_actor.get_transform()

    spectator.set_transform(carla.Transform(transform.location + carla.Location(z=2) + carla.Location(x=-6),
                                            carla.Rotation(yaw=transform.rotation.yaw, pitch=-15)))

    random_attribution(20, 48, blueprint_library, world, spawn_points)

    camera.listen(lambda image: image.save_to_disk('output/%06d.png' % image.frame))



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')
