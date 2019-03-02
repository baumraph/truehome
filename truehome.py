import datetime
import threading
import dataset
import logging
from Observer import Observer
from devices.IKEA import IKEA_TRADFRI_LED
from devices.Xiaomi import Xiaomi_Switch, Xiaomi_Temperature_Humidity, Xiaomi_Motion_Sensor
from devices.Philips import Philips_Hue_Color

observer = Observer('192.168.188.10', 'zigbee2mqtt')
db = dataset.connect('sqlite:///dataset.db')

# Setup logging
logger = logging.getLogger('truehome')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('truehome.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

# Lights
left_desk_light = IKEA_TRADFRI_LED('zigbee2mqtt/Left Desk Light', observer.publish)
right_desk_light = IKEA_TRADFRI_LED('zigbee2mqtt/Right Desk Light', observer.publish)
shelves_light = Philips_Hue_Color('zigbee2mqtt/Shelves Light', observer.publish)
corner_light = Philips_Hue_Color('zigbee2mqtt/Corner Light', observer.publish)
bed_light = Philips_Hue_Color('zigbee2mqtt/Bed Light', observer.publish)

# Switches
desk_switch = Xiaomi_Switch('zigbee2mqtt/Desk Switch')
bed_switch = Xiaomi_Switch('zigbee2mqtt/Bed Switch')
hall_switch = Xiaomi_Switch('zigbee2mqtt/Hall Switch')

# Sensors
living_room_sensor = Xiaomi_Temperature_Humidity('zigbee2mqtt/Living Room Sensor')
bath_sensor = Xiaomi_Temperature_Humidity('zigbee2mqtt/Bath Sensor')
balcony_sensor = Xiaomi_Temperature_Humidity('zigbee2mqtt/Balcony Sensor')
motion_sensor = Xiaomi_Motion_Sensor('zigbee2mqtt/Motion Sensor')

# Groups
group_lights = [left_desk_light, right_desk_light, shelves_light, corner_light, bed_light]
group_desk_lights = [left_desk_light, right_desk_light]
group_ambient_lights = [shelves_light, corner_light, bed_light]
group_switches = [desk_switch, bed_switch, hall_switch]
group_temp_humidity_sensors = [living_room_sensor, bath_sensor, balcony_sensor]
group_sensors = [living_room_sensor, bath_sensor, balcony_sensor, motion_sensor]
group_all = group_lights + group_switches + group_sensors

# States
current_light_scene = 'off'


def light_scene_off():
    global current_light_scene
    current_light_scene = 'off'
    logger.info('Set light scene to {}'.format(current_light_scene))
    for light in group_lights:
        light.off()


def light_scene_dimmed():
    global current_light_scene
    current_light_scene = 'dimmed'
    logger.info('Set light scene to {}'.format(current_light_scene))
    for light in group_desk_lights:
        light.off()
    for light in group_ambient_lights:
        light.brightness(30)
        light.color_temp(490)
        light.on()


def light_scene_learn():
    global current_light_scene
    current_light_scene = 'learn'
    logger.info('Set light scene to {}'.format(current_light_scene))
    for light in group_ambient_lights:
        light.off()
    for light in group_desk_lights:
        light.brightness(230)
        light.on()


def light_scene_love():
    global current_light_scene
    current_light_scene = 'love'
    logger.info('Set light scene to {}'.format(current_light_scene))
    for light in group_desk_lights:
        light.off()
    
    shelves_light.brightness(100)
    shelves_light.color(0.42, 0.2)

    corner_light.brightness(254)
    corner_light.color(0.72, 0.28)

    bed_light.brightness(100)
    bed_light.color(0.72, 0.28)

    for light in group_ambient_lights:
        light.on()


def light_scene_relax():
    global current_light_scene
    current_light_scene = 'love'
    logger.info('Set light scene to {}'.format(current_light_scene))
    for light in group_desk_lights:
        light.off()
    
    shelves_light.brightness(180)
    shelves_light.color(0.6, 0.3)

    corner_light.brightness(180)
    corner_light.color_temp(490)

    bed_light.brightness(80)
    bed_light.color_temp(500)

    for light in group_ambient_lights:
        light.on()


def toggle_light_scene(light_scene_fn):
    logger.info('Toggle light scene')
    if current_light_scene == 'off':
        light_scene_fn()
    else:
        light_scene_off()


def log_temperature_and_humidity(sensor):
    logger.info('Log temperature and humidity for {}'.format(sensor.topic()))
    db['sensors'].insert({
        'name': sensor.topic(),
        'timestamp': datetime.datetime.now(),
        'temperature': sensor.temperature(),
        'humidity': sensor.humidity()
    })


def is_night_time():
    start = datetime.time(23, 0, 0)
    end = datetime.time(6, 0, 0)
    now = datetime.datetime.now().time()
    return start <= now and now <= end     
    

def motion_changed():
    logger.info('Motion detected')
    if motion_sensor.is_occupied() and current_light_scene == 'off' and is_night_time():
        light_scene_dimmed()
        threading.Timer(3, lambda: light_scene_off() if current_light_scene == 'dimmed' else None).start()


if __name__ == '__main__':
    # Add devices to observer
    for device in group_all:
        observer.add_device(device)

    # Register callbacks
    desk_switch.on_single_click(lambda: toggle_light_scene(light_scene_learn))
    desk_switch.on_double_click(light_scene_relax)

    hall_switch.on_single_click(lambda: toggle_light_scene(light_scene_learn))
    hall_switch.on_double_click(light_scene_relax)

    bed_switch.on_single_click(lambda: toggle_light_scene(light_scene_dimmed))
    bed_switch.on_double_click(light_scene_love)

    living_room_sensor.on_update(lambda: log_temperature_and_humidity(living_room_sensor))
    bath_sensor.on_update(lambda: log_temperature_and_humidity(bath_sensor))
    balcony_sensor.on_update(lambda: log_temperature_and_humidity(balcony_sensor))
    motion_sensor.on_update(motion_changed)

    # Run observer
    observer.run()
