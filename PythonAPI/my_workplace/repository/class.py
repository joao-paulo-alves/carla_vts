import carla
from carla import *
import numpy
import pygame
import argparse
import random


class Data(object):
    class Pawn:
        daf = 0

    class Vehicle:
        daf = 0

    class Building:
        daf = 0


def main():
    vehicles_list = []
    walkers_list = []
    all_id = []

    # SETTING CLIENT
    client = carla.Client('localhost', 2000)
    client.set_timeout(30.0)

    # SET A SPECIFIED SCENARIO
    world = client.load_world('Town03')

    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 1 / 60
    settings.max_substep_delta_time = 1 / 60
    world.apply_settings(settings)
    # GET THE CURRENT SCENARIO
    # world = client.get_world()
    # -------------------------------Main Vehicle Spawn---------------------------------------------#
    # GET ALL THE BLUEPRINTS
    blueprint_library = world.get_blueprint_library()

    # SETTING UP MAIN ACTOR
    vehicle_main = blueprint_library.find('vehicle.tesla.model3')

    # SPECIFY THE LOCATION
    # transform = Transform(Location(x=110, y=95, z=1), Rotation(yaw=90))

    # GET ALL THE RECOMMENDED SPAWN LOCATIONS FOR VEHICLES
    spawn_points = world.get_map().get_spawn_points()

    # SPAWN ACTOR
    main_actor = world.spawn_actor(vehicle_main, spawn_points[5])
    main_actor1 = world.spawn_actor(vehicle_main, carla.Transform(spawn_points[5].location + carla.Location(x=7)))
    # -------------------------------Sensor Attach-------------------------------------------------#
    sensor = blueprint_library.find('sensor.camera.rgb')
    sensor.set_attribute('image_size_x', '1820')
    sensor.set_attribute('image_size_y', '561')
    sensor.set_attribute('fov', '110')
    sensor.set_attribute('fstop', '1.6'),

    # sensor.set_attribute('sensor_tick', '1')
    sensor_location = carla.Location(0.4, 0, 1.2)
    sensor_rotation = carla.Rotation(8.75, 0, 0)
    sensor_transform = carla.Transform(sensor_location, sensor_rotation)
    camera = world.spawn_actor(sensor, sensor_transform, attach_to=main_actor,
                               attachment_type=carla.AttachmentType.Rigid)
    # camera.listen(lambda image: image.save_to_disk('output/%06d.png' % image.frame))

    # -------------------------------Auto Pilot-------------------------------------------------#
    main_actor.set_autopilot(True)
    main_actor1.set_autopilot(True)

    debug = world.debug

    while 1:
        # -------------------------------Spectator Mode-------------------------------------------------#
        world.tick()
        spectator = world.get_spectator()
        transform = camera.get_transform()
        spectator.set_transform(carla.Transform(transform.location + carla.Location(z=2) + carla.Location(x=-6),
                                                carla.Rotation(yaw=transform.rotation.yaw, pitch=-15)))

        world_snapshot = world.get_snapshot()

        for actor_snapshot in world_snapshot:
            actual_actor = world.get_actor(actor_snapshot.id)
            if "vehicle." in actual_actor.type_id:

                debug.draw_box(carla.BoundingBox(actual_actor.get_transform().location,actual_actor.bounding_box.extent),
                               actual_actor.get_transform().location, 0.05, carla.Color(255, 0, 0, 0), 1 / 30)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')
