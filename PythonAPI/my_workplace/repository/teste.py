import carla
import carla_agents
from carla import *
import numpy
import pygame
import random

from carla.agents.navigation.basic_agent import BasicAgent
from carla.agents.navigation.behavior_agent import BehaviorAgent


# ---------------------------------------Global-----------------------------
# SETTING CLIENT
client = carla.Client('localhost', 2000)
client.set_timeout(30.0)

# SET A SPECIFIED SCENARIO
world = client.load_world('Town10HD')

# GET THE CURRENT SCENARIO
# world = client.get_world()

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
settings.fixed_delta_seconds = 0.5

# ______________________________________________________

class Sensor:
    attr = blueprint_library.find('sensor.camera.rgb')
    attr.set_attribute('image_size_x', '1820')
    attr.set_attribute('image_size_y', '940')
    attr.set_attribute('fov', '110')
    attr.set_attribute('fstop', '1.6')

    location = carla.Location(0.4, 0, 1.2)
    rotation = carla.Rotation(8.75, 0, 0)
    transform = carla.Transform(location, rotation)
    info = 0


# ________________________________________________________
# ______________________________________________________

class MainActor:
    attr = blueprint_library.find('vehicle.tesla.model3')
    info = 0


# ________________________________________________________
# ______________________________________________________
# ______________________________________________________

class Cars:
    total = random.randint(25, 26)
    info = [0] * total
    attr = 0


# ________________________________________________________
class Walkers:
    info = 0


# ________________________________________________________

def generate_scenario():
    z = 0
    for x in Cars.info:
        y = random.randint(0, 154)
        Cars.attr = random.choice(lib_car)
        while Cars.attr.id == 'vehicle.bh.crossbike' or Cars.attr.id == 'vehicle.micro.microlino' or Cars.attr.id == 'vehicle.diamondback.century' or Cars.attr.id == 'vehicle.vespa.zx125' or Cars.attr.id == 'vehicle.gazelle.omafiets':
            print("Removed!|!!!")
            Cars.attr = random.choice(lib_car)
        spawned = world.try_spawn_actor(Cars.attr, carla.Transform(spawn_points[y].location,
                                                                   carla.Rotation(yaw=spawn_points[y].rotation.yaw,
                                                                                  roll=spawn_points[y].rotation.roll,
                                                                                  pitch=spawn_points[
                                                                                      y].rotation.pitch)))

        while spawned is None:
            y = random.randint(0, 154)
            spawned = world.try_spawn_actor(Cars.attr, carla.Transform(spawn_points[y].location,
                                                                       carla.Rotation(yaw=spawn_points[y].rotation.yaw,
                                                                                      roll=spawn_points[
                                                                                          y].rotation.roll,
                                                                                      pitch=spawn_points[
                                                                                          y].rotation.pitch)))


        Cars.info[z] = spawned
        z = z + 1
    for x in Cars.info:
        x.set_autopilot(True, tm_port)


# ________________________________________________________

def main():
    # SETTING UP MAIN ACTOR

    MainActor.info = world.spawn_actor(MainActor.attr,
                                       carla.Transform(spawn_points[1].location,
                                                       carla.Rotation(yaw=spawn_points[1].rotation.yaw,
                                                                      roll=spawn_points[1].rotation.roll,
                                                                      pitch=spawn_points[1].rotation.pitch)))

    Sensor.info = world.spawn_actor(Sensor.attr, Sensor.transform, attach_to=MainActor.info,
                                    attachment_type=carla.AttachmentType.Rigid)

    agent = BehaviorAgent(MainActor.info, 'normal')

    set_dest = 1
    agent.set_destination(spawn_points[54].location)
    #Sensor.info.listen(lambda image: image.save_to_disk('output/%06d.png' % image.frame))
    spectator = world.get_spectator()

    world.apply_settings(init_settings)
    #generate_scenario()

    while 1:
        world.tick()
        if agent.done():
            if set_dest == 0:
                agent.set_destination((spawn_points[54]).location)
                set_dest = 1
            elif set_dest == 1:
                agent.set_destination((spawn_points[80]).location)
                set_dest = 2
            elif set_dest == 2:
                agent.set_destination((spawn_points[86]).location)
                set_dest = 3
            elif set_dest == 3:
                agent.set_destination((spawn_points[1]).location)
                set_dest = 0
        MainActor.info.apply_control(agent.run_step())
        transform = MainActor.info.get_transform()
        spectator.set_transform(carla.Transform(transform.location + carla.Location(z=25),
                                                carla.Rotation(pitch=-90)))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        settings.synchronous_mode = False
        traffic_manager.set_synchronous_mode(False)
        print('\ndone.')
