import datetime
import threading
import dataset
import logging
from Observer import Observer
from devices.Xiaomi import Xiaomi_Temperature_Humidity


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

# Sensors
living_room_sensor = Xiaomi_Temperature_Humidity('zigbee2mqtt/Living Room Sensor')
bath_sensor = Xiaomi_Temperature_Humidity('zigbee2mqtt/Bath Sensor')
balcony_sensor = Xiaomi_Temperature_Humidity('zigbee2mqtt/Balcony Sensor')

# Groups
group_sensors = [living_room_sensor, bath_sensor, balcony_sensor]
group_all = group_sensors


def save_temperature(name, temperature):
    logger.info('Save temperature of {}'.format(name))
    db['temperature'].insert({
        'name': name,
        'temperature': temperature,
        'timestamp': datetime.datetime.now()
    })


def save_humidity(name, humidity):
    logger.info('Save humidity of {}'.format(name))
    db['humidity'].insert({
        'name': name,
        'humidity': humidity,
        'timestamp': datetime.datetime.now()
    })


def save_sensor_data(name, sensor):
    save_temperature(name, sensor.temperature())
    save_humidity(name, sensor.humidity())


if __name__ == '__main__':
    # Add devices to observer
    for device in group_all:
        observer.add_device(device)

    # Register callbacks
    living_room_sensor.on_update(lambda: save_sensor_data('living_room', living_room_sensor))
    bath_sensor.on_update(lambda: save_sensor_data('bathroom', bath_sensor))
    balcony_sensor.on_update(lambda: save_sensor_data('balcony', balcony_sensor))

    # Run observer
    observer.run()
