import Observer
import mqtt_devices.IKEA
import mqtt_devices.Philips
import mqtt_devices.Xiaomi

# Observer
observer = Observer.Observer('192.168.188.10', 'zigbee2mqtt')

# Lights
left_desk_light = mqtt_devices.IKEA.TRADFRI_LED('zigbee2mqtt/Left Desk Light', observer.publish)
right_desk_light = mqtt_devices.IKEA.TRADFRI_LED('zigbee2mqtt/Right Desk Light', observer.publish)
shelves_light = mqtt_devices.Philips.Hue_Color('zigbee2mqtt/Shelves Light', observer.publish)
corner_light = mqtt_devices.Philips.Hue_Color('zigbee2mqtt/Corner Light', observer.publish)
bed_light = mqtt_devices.Philips.Hue_Color('zigbee2mqtt/Bed Light', observer.publish)

# Switches
desk_switch = mqtt_devices.Xiaomi.Switch('zigbee2mqtt/Desk Switch')
bed_switch = mqtt_devices.Xiaomi.Switch('zigbee2mqtt/Bed Switch')
hall_switch = mqtt_devices.Xiaomi.Switch('zigbee2mqtt/Hall Switch')

# Sensors
living_room_sensor = mqtt_devices.Xiaomi.Temperature_Humidity_Sensor('zigbee2mqtt/Living Room Sensor')
bathroom_sensor = mqtt_devices.Xiaomi.Temperature_Humidity_Sensor('zigbee2mqtt/Bath Sensor')
balcony_sensor = mqtt_devices.Xiaomi.Temperature_Humidity_Sensor('zigbee2mqtt/Balcony Sensor')
motion_sensor = mqtt_devices.Xiaomi.Motion_Sensor('zigbee2mqtt/Motion Sensor')
front_door = mqtt_devices.Xiaomi.Door_Window_Contact_Sensor('zigbee2mqtt/Front Door')
