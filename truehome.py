import datetime
import threading
import dataset
import logging
import threading
import time
import devices
import groups
import lights
import logic


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


if __name__ == '__main__':
    # Add devices to observer
    for device in groups.all:
        devices.observer.add_device(device)

    # Register callbacks
    devices.desk_switch.on_single_click(lambda: lights.toggle_scene(lights.LightScene.LEARN))
    devices.desk_switch.on_double_click(lambda: lights.set_scene(lights.LightScene.RELAX))

    devices.hall_switch.on_single_click(lambda: lights.toggle_scene(lights.LightScene.LEARN))
    devices.hall_switch.on_double_click(lambda: lights.set_scene(lights.LightScene.RELAX))

    devices.bed_switch.on_single_click(lambda: lights.toggle_scene(lights.LightScene.DIMMED))
    devices.bed_switch.on_double_click(lambda: lights.set_scene(lights.LightScene.LOVE))

    devices.living_room_sensor.on_update(lambda: logic.save_sensor_data('living_room', devices.living_room_sensor))
    devices.bathroom_sensor.on_update(lambda: logic.save_sensor_data('bathroom', devices.bathroom_sensor))
    devices.balcony_sensor.on_update(lambda: logic.save_sensor_data('balcony', devices.balcony_sensor))

    # Run observer
    devices.observer.run()
