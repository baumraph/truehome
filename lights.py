import enum
import devices
import groups


class LightScene(enum.Enum):
    UNKNOWN = 0
    OFF = 1
    LEARN = 2
    LOVE = 3
    RELAX = 4
    DIMMED = 5
    WARNING = 6


_current_scene = LightScene.UNKNOWN


def set_scene(scene):
    global _current_scene
    if scene == LightScene.UNKNOWN:
        pass
    elif scene == LightScene.OFF:
        _off()
    elif scene == LightScene.LEARN:
        _learn()
    elif scene == LightScene.LOVE:
        _love()
    elif scene == LightScene.RELAX:
        _relax()
    elif scene == LightScene.DIMMED:
        _dimmed()
    elif scene == LightScene.WARNING:
        _warning()
    _current_scene = scene


def toggle_scene(scene):
    if get_scene() == LightScene.OFF:
        set_scene(scene)
    else:
        set_scene(LightScene.OFF)


def get_scene():
    global _current_scene
    return _current_scene


def _off():
    for light in groups.lights:
        light.off()


def _learn():
    for light in groups.ambient_lights:
        light.off()
    for light in groups.desk_lights:
        light.brightness(230)
        light.on()


def _love():
    for light in groups.desk_lights:
        light.off()
    
    devices.shelves_light.brightness(100)
    devices.shelves_light.color(0.42, 0.2)

    devices.corner_light.brightness(254)
    devices.corner_light.color(0.72, 0.28)

    devices.bed_light.brightness(100)
    devices.bed_light.color(0.72, 0.28)

    for light in groups.ambient_lights:
        light.on()


def _relax():
    for light in groups.desk_lights:
        light.off()
    
    devices.shelves_light.brightness(180)
    devices.shelves_light.color(0.6, 0.3)

    devices.corner_light.brightness(180)
    devices.corner_light.color_temp(490)

    devices.bed_light.brightness(80)
    devices.bed_light.color_temp(500)

    for light in groups.ambient_lights:
        light.on()


def _dimmed():
    for light in groups.desk_lights:
        light.off()
    for light in groups.ambient_lights:
        light.brightness(30)
        light.color_temp(490)
        light.on()


def _warning():
    for light in groups.lights:
        light.off()
    for light in groups.ambient_lights:
        light.brightness(255)
        light.color(0.17, 0.26)
        light.on()
