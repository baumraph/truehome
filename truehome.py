import datetime
import threading
import dataset
import logging
from Observer import Observer
from devices.Xiaomi import Xiaomi_Temperature_Humidity


observer = Observer('192.168.188.10', 'zigbee2mqtt')


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
