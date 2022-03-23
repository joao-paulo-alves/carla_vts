import carla
from carla import *
import numpy
import pygame
import argparse
import random



def main():
    vehicles_list = []
    walkers_list = []
    all_id = []

    # SETTING CLIENT
    client = carla.Client('localhost', 2000)
    client.set_timeout(30.0)

    # SET A SPECIFIED SCENARIO
    world = client.load_world('Town03')

    # GET THE CURRENT SCENARIO
    #world = client.get_world()
    # -------------------------------Main Vehicle Spawn---------------------------------------------#
    # GET ALL THE BLUEPRINTS
    blueprint_library = world.get_blueprint_library()

    # SETTING UP MAIN ACTOR
    vehicle_main = blueprint_library.find('vehicle.tesla.model3')

    # SPECIFY THE LOCATION
    #transform = Transform(Location(x=110, y=95, z=1), Rotation(yaw=90))

    # GET ALL THE RECOMMENDED SPAWN LOCATIONS FOR VEHICLES
    spawn_points = world.get_map().get_spawn_points()

    # SPAWN ACTOR
    main_actor = world.spawn_actor(vehicle_main, spawn_points[5])
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
    camera = world.spawn_actor(sensor, sensor_transform , attach_to=main_actor,attachment_type=carla.AttachmentType.Rigid)
    camera.listen(lambda image: image.save_to_disk('output/%06d.png' % image.frame))

    # -------------------------------Auto Pilot-------------------------------------------------#
    main_actor.set_autopilot(True)


    while 1:
        # -------------------------------Spectator Mode-------------------------------------------------#
        spectator = world.get_spectator()
        transform = camera.get_transform()
        spectator.set_transform(carla.Transform(transform.location + carla.Location(z=2)+carla.Location(x=-6),carla.Rotation(yaw=transform.rotation.yaw, pitch=-15)))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')
