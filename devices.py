import Observer
import mqtt_devices.IKEA
import mqtt_devices.OSRAM

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

# Plugs
plug_window = mqtt_devices.OSRAM.OSRAM_SMART_PLUG('zigbee2mqtt/LRPlugWindow', observer.publish)
plug_shelf = mqtt_devices.OSRAM.OSRAM_SMART_PLUG('zigbee2mqtt/LRPlugShelf', observer.publish)
