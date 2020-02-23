import datetime
import threading
import time
import devices
import groups


class Bedroom():
    def __init__(self):
        self.scene = 'OFF'

        devices.switch_bedroom.on_on(self.set_scene_normal)
        devices.switch_bedroom.on_off(self.set_scene_off)

        devices.remote_bedroom.on_toggle(self.toggle)
        devices.remote_bedroom.on_arrow_left_click(self.arrow)
        devices.remote_bedroom.on_arrow_right_click(self.arrow)
        devices.remote_bedroom.on_brightness_up_click(self.brightness_up)
        devices.remote_bedroom.on_brightness_down_click(self.brightness_down)

    def set_scene_normal(self):
        self.scene = 'NORMAL'

        devices.light_bedroom_top.color(0.475, 0.415)
        devices.light_bedroom_top.brightness(254)
        devices.light_bedroom_top.on()

    def set_scene_red(self):
        self.scene = 'RED'

        devices.light_bedroom_top.color(0.72, 0.28)
        devices.light_bedroom_top.brightness(254)
        devices.light_bedroom_top.on()

    def set_scene_off(self):
        self.scene = 'OFF'

        devices.light_bedroom_top.off()

    def toggle(self):
        if self.scene == 'OFF':
            self.set_scene_normal()
        elif self.scene == 'NORMAL':
            self.set_scene_off()
        elif self.scene == 'RED':
            self.set_scene_off()

    def arrow(self):
        if self.scene == 'NORMAL':
            self.set_scene_red()
        elif self.scene == 'RED':
            self.set_scene_normal()

    def brightness_up(self):
        b = devices.light_bedroom_top.brightness()
        b = int(min(254, b + 254 / 10))
        devices.light_bedroom_top.brightness(b)

    def brightness_down(self):
        b = devices.light_bedroom_top.brightness()
        b = int(max(0, b - 254 / 10))
        devices.light_bedroom_top.brightness(b)


class LivingRoom():

    def __init__(self):
        self.scene = 'OFF'

        devices.switch_living_room.on_on(self.set_scene_normal)
        devices.switch_living_room.on_off(self.set_scene_off)

        devices.remote_living_room.on_toggle(self.toggle)
        devices.remote_living_room.on_arrow_left_click(self.arrow)
        devices.remote_living_room.on_arrow_right_click(self.arrow)
        devices.remote_living_room.on_brightness_up_click(self.brightness_up)
        devices.remote_living_room.on_brightness_down_click(self.brightness_down)

    def set_scene_normal(self):
        self.scene = 'NORMAL'
        devices.light_living_room_shelf.color(0.475, 0.415)
        devices.light_living_room_top.color(0.475, 0.415)

        devices.light_living_room_shelf.on()
        devices.light_living_room_top.on()
        devices.plug_living_room.off()

    def set_scene_ambient(self):
        self.scene = 'AMBIENT'
        devices.light_living_room_top.color(0.72, 0.28)
        devices.light_living_room_shelf.color(0.6, 0.28)

        devices.light_living_room_top.on()
        devices.light_living_room_shelf.on()
        devices.plug_living_room.off()

    def set_scene_window(self):
        self.scene = 'WINDOW'
        devices.plug_living_room.on()
        devices.light_living_room_top.off()
        devices.light_living_room_shelf.off()

    def set_scene_off(self):
        self.scene = 'OFF'
        devices.light_living_room_top.off()
        devices.light_living_room_shelf.off()
        devices.plug_living_room.off()

    def toggle(self):
        if self.scene == 'OFF':
            self.set_scene_normal()
        elif self.scene == 'NORMAL':
            self.set_scene_off()
        elif self.scene == 'AMBIENT':
            self.set_scene_off()
        elif self.scene == 'WINDOW':
            self.set_scene_off()

    def arrow(self):
        if self.scene == 'NORMAL':
            self.set_scene_ambient()
        elif self.scene == 'AMBIENT':
            self.set_scene_window()
        elif self.scene == 'WINDOW':
            self.set_scene_normal()
        

    def brightness_up(self):
        b = devices.light_living_room_top.brightness()
        b = int(min(254, b + 254 / 10))
        devices.light_living_room_top.brightness(b)
        devices.light_living_room_shelf.brightness(b)

    def brightness_down(self):
        b = devices.light_living_room_top.brightness()
        b = int(max(0, b - 254 / 10))
        devices.light_living_room_top.brightness(b)
        devices.light_living_room_shelf.brightness(b)


import time
if __name__ == '__main__':
    # Add devices to observer
    for device in groups.all:
        devices.observer.add_device(device)

    # Create logic for each room
    bedroom = Bedroom()
    living_room = LivingRoom()

    # Run observer
    devices.observer.run()
