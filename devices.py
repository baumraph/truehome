import Observer
import mqtt_devices.IKEA

# Observer
observer = Observer.Observer('192.168.188.20', 'zigbee2mqtt')

# Lights
light_bedroom_top = mqtt_devices.IKEA.TRADFRI_RGB_LED('zigbee2mqtt/BRLightTop', observer.publish)
light_living_room_top = mqtt_devices.IKEA.TRADFRI_RGB_LED('zigbee2mqtt/LRLightTop', observer.publish)
light_living_room_shelf = mqtt_devices.IKEA.TRADFRI_RGB_LED('zigbee2mqtt/LRLightShelf', observer.publish)

# Switches
switch_bedroom = mqtt_devices.IKEA.TRADFRI_SWITCH('zigbee2mqtt/BRSwitch')
remote_bedroom = mqtt_devices.IKEA.TRADFRI_REMOTE('zigbee2mqtt/BRRemote')
switch_living_room = mqtt_devices.IKEA.TRADFRI_SWITCH('zigbee2mqtt/LRSwitch')
remote_living_room = mqtt_devices.IKEA.TRADFRI_REMOTE('zigbee2mqtt/LRRemote')

# # Sensors
# living_room_sensor = mqtt_devices.Xiaomi.Temperature_Humidity_Sensor('zigbee2mqtt/Living Room Sensor')
# bathroom_sensor = mqtt_devices.Xiaomi.Temperature_Humidity_Sensor('zigbee2mqtt/Bath Sensor')
# balcony_sensor = mqtt_devices.Xiaomi.Temperature_Humidity_Sensor('zigbee2mqtt/Balcony Sensor')
# motion_sensor = mqtt_devices.Xiaomi.Motion_Sensor('zigbee2mqtt/Motion Sensor')
# front_door = mqtt_devices.Xiaomi.Door_Window_Contact_Sensor('zigbee2mqtt/Front Door')
