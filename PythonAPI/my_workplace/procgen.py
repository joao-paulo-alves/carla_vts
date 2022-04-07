import glob
import os
import sys
import time
import carla
from carla import VehicleLightState as vls
import logging
import math
from numpy import random
##import imageio
from queue import Queue
from queue import Empty
from configparser import ConfigParser
import threading
from concurrent.futures import ThreadPoolExecutor

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


def saving(s):
    s[0].save_to_disk('output/%06d.png' % s[1])


def Weather(world, parser):
    day_choice = parser.getint('worldsettings', 'timeofday')

    if day_choice == 1:
        choice = random.randint(1, 28)
        while 19 <= choice <= 25:
            choice = random.randint(1, 28)
    elif day_choice == 2:
        choice = random.randint(1, 28)
        while 1 <= choice <= 18 or 26 <= choice <= 28:
            choice = random.randint(1, 28)

    # ------------------------Cloudy Day---------------------------------
    if choice == 1:
        world.set_weather(carla.WeatherParameters.CloudyNoon)
    elif choice == 2:
        world.set_weather(carla.WeatherParameters.WetNoon)
    elif choice == 3:
        world.set_weather(carla.WeatherParameters.WetCloudyNoon)
    elif choice == 4:
        world.set_weather(carla.WeatherParameters.SoftRainNoon)
    elif choice == 5:
        world.set_weather(carla.WeatherParameters.MidRainyNoon)
    elif choice == 6:
        world.set_weather(carla.WeatherParameters.HardRainNoon)
    elif choice == 7:
        world.set_weather(carla.WeatherParameters.CloudySunset)
    elif choice == 8:
        world.set_weather(carla.WeatherParameters.WetSunset)
    elif choice == 9:
        world.set_weather(carla.WeatherParameters.WetCloudySunset)
    elif choice == 10:
        world.set_weather(carla.WeatherParameters.SoftRainSunset)
    elif choice == 11:
        world.set_weather(carla.WeatherParameters.MidRainSunset)
    elif choice == 12:
        world.set_weather(carla.WeatherParameters.HardRainSunset)
    elif choice == 13:
        weather_conversion = carla.WeatherParameters.CloudySunset
        weather_conversion.sun_azimuth_angle = weather_conversion.sun_azimuth_angle + 180  # Dawn
        world.set_weather(weather_conversion)
    elif choice == 14:
        weather_conversion = carla.WeatherParameters.WetSunset
        weather_conversion.sun_azimuth_angle = weather_conversion.sun_azimuth_angle + 180  # Dawn
        world.set_weather(weather_conversion)
    elif choice == 15:
        weather_conversion = carla.WeatherParameters.WetCloudySunset
        weather_conversion.sun_azimuth_angle = weather_conversion.sun_azimuth_angle + 180  # Dawn
        world.set_weather(weather_conversion)
    elif choice == 16:
        weather_conversion = carla.WeatherParameters.SoftRainSunset
        weather_conversion.sun_azimuth_angle = weather_conversion.sun_azimuth_angle + 180  # Dawn
        world.set_weather(weather_conversion)
    elif choice == 17:
        weather_conversion = carla.WeatherParameters.MidRainSunset
        weather_conversion.sun_azimuth_angle = weather_conversion.sun_azimuth_angle + 180  # Dawn
        world.set_weather(weather_conversion)
    elif choice == 18:
        weather_conversion = carla.WeatherParameters.HardRainSunset
        weather_conversion.sun_azimuth_angle = weather_conversion.sun_azimuth_angle + 180  # Dawn
        world.set_weather(weather_conversion)
    elif choice == 19:
        weather_conversion = carla.WeatherParameters.CloudyNoon
        weather_conversion.sun_altitude_angle = weather_conversion.sun_altitude_angle - 180  # Night
        world.set_weather(weather_conversion)
    elif choice == 20:
        weather_conversion = carla.WeatherParameters.WetNoon
        weather_conversion.sun_altitude_angle = weather_conversion.sun_altitude_angle - 180  # Night
        world.set_weather(weather_conversion)
    elif choice == 21:
        weather_conversion = carla.WeatherParameters.WetCloudyNoon
        weather_conversion.sun_altitude_angle = weather_conversion.sun_altitude_angle - 180  # Night
        world.set_weather(weather_conversion)
    elif choice == 22:
        weather_conversion = carla.WeatherParameters.SoftRainNoon
        weather_conversion.sun_altitude_angle = weather_conversion.sun_altitude_angle - 180  # Night
        world.set_weather(weather_conversion)
    elif choice == 23:
        weather_conversion = carla.WeatherParameters.MidRainyNoon
        weather_conversion.sun_altitude_angle = weather_conversion.sun_altitude_angle - 180  # Night
        world.set_weather(weather_conversion)
    elif choice == 24:
        weather_conversion = carla.WeatherParameters.HardRainNoon
        weather_conversion.sun_altitude_angle = weather_conversion.sun_altitude_angle - 180  # Night
        world.set_weather(weather_conversion)

        # ------------------------------Clear Day----------------------------------------
    elif choice == 25:
        weather_conversion = carla.WeatherParameters.ClearNoon
        weather_conversion.sun_altitude_angle = weather_conversion.sun_altitude_angle - 180  # Night
        world.set_weather(weather_conversion)
    elif choice == 26:
        world.set_weather(carla.WeatherParameters.ClearSunset)
    elif choice == 27:
        weather_conversion = carla.WeatherParameters.ClearSunset
        weather_conversion.sun_azimuth_angle = weather_conversion.sun_azimuth_angle + 180  # Dawn
        world.set_weather(weather_conversion)
    elif choice == 28:
        world.set_weather(carla.WeatherParameters.ClearNoon)

    return choice


def get_actor_blueprints(world, filter, generation):
    bps = world.get_blueprint_library().filter(filter)

    if generation.lower() == "all":
        return bps

    # If the filter returns only one bp, we assume that this one needed
    # and therefore, we ignore the generation
    if len(bps) == 1:
        return bps

    try:
        int_generation = int(generation)
        # Check if generation is in available generations
        if int_generation in [1, 2]:
            bps = [x for x in bps if int(x.get_attribute('generation')) == int_generation]
            return bps
        else:
            print("   Warning! Actor Generation is not valid. No actor will be spawned.")
            return []
    except:
        print("   Warning! Actor Generation is not valid. No actor will be spawned.")
        return []


def sensor_callback(sensor_data, sensor_queue, sensor_name):
    # Do stuff with the sensor_data data like save it to disk
    # Then you just need to add to the queue
    # sensor_data.save_to_disk('output/%06d.png' % sensor_data.frame)

    sensor_queue.put((sensor_data, sensor_data.frame))


def main():
    parser = ConfigParser()
    parser.read('config.ini')
    number_of_vehicles = parser.getint('vehiclesettings', 'number_of_vehicles')
    number_of_walkers = parser.getint('walkersettings', 'number_of_walkers')
    seed = None

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    vehicles_list = []
    walkers_list = []
    all_id = []
    client = carla.Client(parser.get('worldsettings', 'host'), parser.getint('worldsettings', 'port'))
    client.set_timeout(40.0)
    synchronous_master = False
    random.seed(seed if seed is not None else int(time.time()))

    try:
        map_choice = random.randint(1, 6)
        if map_choice == 6:
            world = client.load_world('Town10HD')
        else:
            world = client.load_world('Town0%d' % map_choice)

        # world = client.get_world()

        traffic_manager = client.get_trafficmanager(parser.getint('worldsettings', 'tm_port'))
        traffic_manager.set_global_distance_to_leading_vehicle(2.5)
        if parser.getboolean('worldsettings', 'respawn'):
            traffic_manager.set_respawn_dormant_vehicles(True)
        if parser.getboolean('worldsettings', 'hybrid'):
            traffic_manager.set_hybrid_physics_mode(True)
            traffic_manager.set_hybrid_physics_radius(70.0)
        if seed is not None:
            traffic_manager.set_random_device_seed(seed)

        settings = world.get_settings()
        if not parser.getboolean('worldsettings', 'asynch'):
            traffic_manager.set_synchronous_mode(True)
            if not settings.synchronous_mode:
                synchronous_master = True
                settings.synchronous_mode = True
                settings.fixed_delta_seconds = 1 / 60
                settings.max_substep_delta_time = 1 / 60


            else:
                synchronous_master = False
        else:
            print("You are currently in asynchronous mode. If this is a traffic simulation, \
            you could experience some issues. If it's not working correctly, switch to synchronous \
            mode by using traffic_manager.set_synchronous_mode(True)")

        if parser.getboolean('worldsettings', 'no_rendering'):
            settings.no_rendering_mode = True
        world.apply_settings(settings)

        choice = Weather(world, parser)

        blueprints = get_actor_blueprints(world, parser.get('worldsettings', 'filterv'),
                                          parser.get('worldsettings', 'generationv'))
        blueprintsWalkers = get_actor_blueprints(world, parser.get('worldsettings', 'filterw'),
                                                 parser.get('worldsettings', 'generationw'))

        if parser.getboolean('worldsettings', 'safe'):
            blueprints = [x for x in blueprints if int(x.get_attribute('number_of_wheels')) == 4]
            blueprints = [x for x in blueprints if not x.id.endswith('microlino')]
            blueprints = [x for x in blueprints if not x.id.endswith('carlacola')]
            blueprints = [x for x in blueprints if not x.id.endswith('cybertruck')]
            blueprints = [x for x in blueprints if not x.id.endswith('t2')]
            blueprints = [x for x in blueprints if not x.id.endswith('sprinter')]
            blueprints = [x for x in blueprints if not x.id.endswith('firetruck')]
            blueprints = [x for x in blueprints if not x.id.endswith('ambulance')]

        blueprints = sorted(blueprints, key=lambda bp: bp.id)

        spawn_points = world.get_map().get_spawn_points()
        number_of_spawn_points = len(spawn_points)

        if number_of_vehicles < number_of_spawn_points:
            random.shuffle(spawn_points)
        elif number_of_vehicles > number_of_spawn_points:
            msg = 'requested %d vehicles, but could only find %d spawn points'
            logging.warning(msg, number_of_vehicles, number_of_spawn_points)
            number_of_vehicles = number_of_spawn_points

        # @todo cannot import these directly.
        SpawnActor = carla.command.SpawnActor
        SetAutopilot = carla.command.SetAutopilot
        FutureActor = carla.command.FutureActor
        blueprint_library = world.get_blueprint_library()
        # --------------
        # Spawn vehicles
        # --------------
        batch = []
        hero = parser.getboolean('worldsettings', 'hero')
        for n, transform in enumerate(spawn_points):
            if n >= number_of_vehicles:
                break
            blueprint = random.choice(blueprints)
            if hero:
                blueprint = blueprint_library.find('vehicle.tesla.model3')
            if blueprint.has_attribute('color'):
                color = random.choice(blueprint.get_attribute('color').recommended_values)
                blueprint.set_attribute('color', color)
            if blueprint.has_attribute('driver_id'):
                driver_id = random.choice(blueprint.get_attribute('driver_id').recommended_values)
                blueprint.set_attribute('driver_id', driver_id)
            if hero:
                blueprint.set_attribute('role_name', 'hero')
                hero = False
            else:
                blueprint.set_attribute('role_name', 'autopilot')

            # spawn the cars and set their autopilot and light state all together

            x = SpawnActor(blueprint, transform)
            z = SetAutopilot(FutureActor, True, traffic_manager.get_port())
            batch.append(x.then(z))

        for response in client.apply_batch_sync(batch, synchronous_master):
            if response.error:
                logging.error(response.error)
            else:
                vehicles_list.append(response.actor_id)

        # Set automatic vehicle lights update if specified
        all_vehicle_actors = world.get_actors(vehicles_list)

        attr = blueprint_library.find(parser.get('sensorsettings', 'bp'))
        attr.set_attribute('image_size_x', parser.get('sensorsettings', 'x'))
        attr.set_attribute('image_size_y', parser.get('sensorsettings', 'y'))
        attr.set_attribute('fov', parser.get('sensorsettings', 'fov'))
        attr.set_attribute('fstop', parser.get('sensorsettings', 'fstop'))
        attr.set_attribute('sensor_tick', parser.get('sensorsettings', 'tick'))
        sensor_location = carla.Location(1, 0, 1.2)
        sensor_rotation = carla.Rotation(8.75, 0, 0)
        sensor_transform = carla.Transform(sensor_location, sensor_rotation)

        sensor = world.spawn_actor(attr, sensor_transform, attach_to=all_vehicle_actors[0],
                                   attachment_type=carla.AttachmentType.Rigid)

        if parser.getboolean('worldsettings', 'car_lights_on'):
            if 1 <= choice <= 25:
                all_vehicle_actors = world.get_actors(vehicles_list)
                for actor in all_vehicle_actors:
                    traffic_manager.update_vehicle_lights(actor, True)
            if 7 <= choice <= 27:
                lights = world.get_lightmanager()
                street = lights.get_all_lights(carla.LightGroup.Street)
                lights.turn_on(street)
            if 19 <= choice <= 25:
                lights = world.get_lightmanager()
                building = lights.get_all_lights(carla.LightGroup.Building)
                lights.turn_on(building)

        # -------------
        # Spawn Walkers
        # -------------
        # some settings
        percentagePedestriansRunning = parser.getfloat('walkersettings', 'perc_run')  # how many pedestrians will run
        percentagePedestriansCrossing = parser.getfloat('walkersettings',
                                                        'perc_cross')  # how many pedestrians will walk through the road
        if parser.getint('worldsettings', 'seedw'):
            world.set_pedestrians_seed(parser.getint('worldsettings', 'seedw'))
            random.seed(parser.getint('worldsettings', 'seedw'))
        # 1. take all the random locations to spawn
        spawn_points = []
        for i in range(number_of_walkers):
            spawn_point = carla.Transform()
            loc = world.get_random_location_from_navigation()
            if (loc != None):
                spawn_point.location = loc
                spawn_points.append(spawn_point)
        # 2. we spawn the walker object
        batch = []
        walker_speed = []
        for spawn_point in spawn_points:
            walker_bp = random.choice(blueprintsWalkers)
            # set as not invincible
            if walker_bp.has_attribute('is_invincible'):
                walker_bp.set_attribute('is_invincible', 'false')
            # set the max speed
            if walker_bp.has_attribute('speed'):
                if (random.random() > percentagePedestriansRunning):
                    # walking
                    walker_speed.append(walker_bp.get_attribute('speed').recommended_values[1])
                else:
                    # running
                    walker_speed.append(walker_bp.get_attribute('speed').recommended_values[2])
            else:
                print("Walker has no speed")
                walker_speed.append(0.0)
            batch.append(SpawnActor(walker_bp, spawn_point))
        results = client.apply_batch_sync(batch, True)
        walker_speed2 = []
        for i in range(len(results)):
            if results[i].error:
                logging.error(results[i].error)
            else:
                walkers_list.append({"id": results[i].actor_id})
                walker_speed2.append(walker_speed[i])
        walker_speed = walker_speed2
        # 3. we spawn the walker controller
        batch = []
        walker_controller_bp = world.get_blueprint_library().find('controller.ai.walker')
        for i in range(len(walkers_list)):
            batch.append(SpawnActor(walker_controller_bp, carla.Transform(), walkers_list[i]["id"]))
        results = client.apply_batch_sync(batch, True)
        for i in range(len(results)):
            if results[i].error:
                logging.error(results[i].error)
            else:
                walkers_list[i]["con"] = results[i].actor_id
        # 4. we put together the walkers and controllers id to get the objects from their id
        for i in range(len(walkers_list)):
            all_id.append(walkers_list[i]["con"])
            all_id.append(walkers_list[i]["id"])
        all_actors = world.get_actors(all_id)

        # wait for a tick to ensure client receives the last transform of the walkers we have just created
        if parser.getboolean('worldsettings', 'asynch') or not synchronous_master:
            world.wait_for_tick()
        else:
            world.tick()

        # 5. initialize each controller and set target to walk to (list is [controler, actor, controller, actor ...])
        # set how many pedestrians can cross the road
        world.set_pedestrians_cross_factor(percentagePedestriansCrossing)
        for i in range(0, len(all_id), 2):
            # start walker
            all_actors[i].start()
            # set walk to random point
            all_actors[i].go_to_location(world.get_random_location_from_navigation())
            # max speed
            all_actors[i].set_max_speed(float(walker_speed[int(i / 2)]))

        print('spawned %d vehicles and %d walkers, press Ctrl+C to exit.' % (len(vehicles_list), len(walkers_list)))

        # Example of how to use Traffic Manager parameters
        traffic_manager.global_percentage_speed_difference(30.0)

        spectator = world.get_spectator()
        sensor_queue = Queue()
        timer = 0
        sensor.listen(lambda data: sensor_callback(data, sensor_queue, "camera01"))
        executor = ThreadPoolExecutor(10)
        t0 = time.time()
        while True:
            if not parser.getboolean('worldsettings', 'asynch') and synchronous_master:
                world.tick()
                transform = all_vehicle_actors[0].get_transform()
                spectator.set_transform(carla.Transform(transform.location + carla.Location(z=25),
                                                        carla.Rotation(pitch=-90)))
            else:
                world.wait_for_tick()

            if timer > 3600:
                break

            if sensor_queue.qsize() > 0:
                s = sensor_queue.get(True, 0.01)
                # t = threading.Thread(target=saving, args=(s,))
                # t.start()
                f = executor.submit(saving, s)
            timer += 1 / 60

            print(timer)
        t1 = time.time()
        print(f'Done in {t1 - t0} seconds.')





    finally:

        world.tick()
        sensor.destroy()

        if not parser.getboolean('worldsettings', 'asynch') and synchronous_master:
            settings = world.get_settings()
            settings.synchronous_mode = False
            settings.no_rendering_mode = False
            settings.fixed_delta_seconds = None
            settings.max_substep_delta_time = 0.1
            world.apply_settings(settings)

        print('\ndestroying %d vehicles' % len(vehicles_list))
        client.apply_batch([carla.command.DestroyActor(x) for x in vehicles_list])

        # stop walker controllers (list is [controller, actor, controller, actor ...])
        for i in range(0, len(all_id), 2):
            all_actors[i].stop()

        print('\ndestroying %d walkers' % len(walkers_list))
        client.apply_batch([carla.command.DestroyActor(x) for x in all_id])

        time.sleep(0.5)


if __name__ == '__main__':
    try:
        #while True:
        main()



    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')
