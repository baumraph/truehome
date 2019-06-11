import dataset
import datetime
import devices
import lights
import threading
import time

_at_home = True
_is_probably_leaving = False
_is_front_door_open = False
_wait_for_movement_thread = None


def save_sensor_value(sensor_name, sensor_type, value):
    db = dataset.connect('sqlite:///dataset.db')
    db[sensor_type].insert({
        'sensor': sensor_name,
        'value': value,
        'timestamp': datetime.datetime.now()
    })


def save_sensor_data(sensor_name, sensor):
    save_sensor_value(sensor_name, 'temperature', sensor.temperature())
    save_sensor_value(sensor_name, 'humidity', sensor.humidity())


def on_arrival():
    print('on_arrival')


def on_leaving():
    print('on_leaving')
    lights.set_scene(lights.LightScene.OFF)


def motion_sensor():
    global _is_probably_leaving, _at_home
    print('OCCUPIED = {}'.format(devices.motion_sensor.is_occupied()))
    if devices.motion_sensor.is_occupied():
        _is_probably_leaving = False
        _at_home = True
        if not _at_home:
            on_arrival()


def wait_for_movement():
    global _is_probably_leaving, _at_home
    print('wait_for_movement')
    if not _is_probably_leaving:
        print('USER STILL HERE')
        return
    
    # Turn on warning lights, so user sees that he has to move
    prev_scene = lights.get_scene()
    lights.set_scene(lights.LightScene.WARNING)

    # Check if there is movement in the next 90 seconds
    now = datetime.datetime.now()
    end = now + datetime.timedelta(seconds=90)
    while (now < end):
        if not _is_probably_leaving:
            print('User is still at home')
            lights.set_scene(prev_scene)
            return
        now = datetime.datetime.now()
        time.sleep(0.2)

    # User is not present any more
    _at_home = False
    on_leaving()


def front_door():
    global _at_home,_is_front_door_open, _is_probably_leaving, _wait_for_movement_thread
    if _at_home and _is_front_door_open and devices.front_door.is_closed():
        print('CLOSED front door')
        _is_probably_leaving = True
        if _wait_for_movement_thread is not None:
            _wait_for_movement_thread.cancel()
            _wait_for_movement_thread.join()
        _wait_for_movement_thread = threading.Timer(90, wait_for_movement, ())
        _wait_for_movement_thread.start()
    _is_front_door_open = devices.front_door.is_open()