from scenehandler import Scene
import devices


class Scene_LR_OFF(Scene):
    def __init__(self):
        Scene.__init__(self, 'OFF')

    def run(self):
        devices.light_living_room_top.off()
        devices.light_living_room_shelf.off()
        devices.plug_window.off()


class Scene_LR_ON(Scene):
    def __init__(self):
        Scene.__init__(self, 'ON')

    def run(self):
        devices.light_living_room_shelf.color(0.475, 0.415)
        devices.light_living_room_top.color(0.475, 0.415)

        devices.light_living_room_shelf.on()
        devices.light_living_room_top.on()
        devices.plug_living_room.off()


class Scene_LR_AMBIENT(Scene):
    def __init__(self):
        Scene.__init__(self, 'AMBIENT')

    def run(self):
        devices.light_living_room_top.color(0.72, 0.28)
        devices.light_living_room_shelf.color(0.6, 0.28)

        devices.light_living_room_top.on()
        devices.light_living_room_shelf.on()
        devices.plug_living_room.off()


class Scene_LR_WINDOW(Scene):
    def __init__(self):
        Scene.__init__(self, 'WINDOW')

    def run(self):
        devices.plug_living_room.on()
        devices.light_living_room_top.off()
        devices.light_living_room_shelf.off()


class Scene_BR_OFF(Scene):
    def __init__(self):
        Scene.__init__(self, 'OFF')

    def run(self):
        devices.light_bedroom_top.off()


class Scene_BR_ON(Scene):
    def __init__(self):
        Scene.__init__(self, 'ON')

    def run(self):
        devices.light_bedroom_top.color(0.475, 0.415)
        devices.light_bedroom_top.on()


class Scene_BR_AMBIENT(Scene):
    def __init__(self):
        Scene.__init__(self, 'AMBIENT')

    def run(self):
        devices.light_bedroom_top.color(0.72, 0.28)
        devices.light_bedroom_top.on()
