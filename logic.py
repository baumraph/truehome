import dataset
import datetime


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
