from mqtt_devices.MQTTDevice import MQTTDevice


class TRADFRI_LED(MQTTDevice):
    def __init__(self, topic, fn_publish):
        MQTTDevice.__init__(self, 'LED1623G12', topic, {
            'state': 'off',
            'brightness': 0
        })
        self._publish = fn_publish

    def on(self):
        self._payload['state'] = 'on'
        self._publish('{}/set'.format(self._topic), '{"state": "on"}')
    
    def off(self):
        self._payload['state'] = 'off'
        self._publish('{}/set'.format(self._topic), '{"state": "off"}')

    def brightness(self, brightness=None):
        if brightness:
            brightness = max(0, min(brightness, 254))
            self._payload['brightness'] = brightness
            self._publish('{}/set'.format(self._topic), '{{"brightness": "{}"}}'.format(brightness))
        else:
            return self._payload['brightness']

    def is_on(self):
        return self._payload['state'].lower() == 'on'

    def is_off(self):
        return self._payload['state'].lower() == 'off'


class TRADFRI_RGB_LED(MQTTDevice):
    def __init__(self, topic, fn_publish):
        MQTTDevice.__init__(self, 'LED1624G9', topic, {
            'state': 'off',
            'brightness': 0,
            'color': {'x': 0.0, 'y': 0.0}
        })
        self._publish = fn_publish

    def on(self):
        self._payload['state'] = 'on'
        self._publish('{}/set'.format(self._topic), '{"state": "on"}')
    
    def off(self):
        self._payload['state'] = 'off'
        self._publish('{}/set'.format(self._topic), '{"state": "off"}')

    def brightness(self, brightness=None):
        if brightness:
            brightness = max(0, min(brightness, 254))
            self._payload['brightness'] = brightness
            self._publish('{}/set'.format(self._topic), '{{"brightness": "{}"}}'.format(brightness))
        else:
            return self._payload['brightness']

    def color(self, x=None, y=None):
        if x and y:
            x = max(0.0, min(x, 1.0))
            y = max(0.0, min(y, 1.0))
            self._payload['color']['x'] = x
            self._payload['color']['y'] = y
            self._publish('{}/set'.format(self._topic), '{{"color": {{"x": {}, "y": {}}}}}'.format(x, y))
        else:
            return self._payload['color']['x'], self._payload['color']['y']

    def is_on(self):
        return self._payload['state'].lower() == 'on'

    def is_off(self):
        return self._payload['state'].lower() == 'off'


class TRADFRI_SWITCH(MQTTDevice):
    def __init__(self, topic):
        MQTTDevice.__init__(self, 'E1743', topic, {
            'linkquality': None,
            'battery': None
        })
        self._callbacks = {
            'on': None,
            'off': None,
            'brightness_up': None,
            'brightness_down': None,
            'brightness_stop': None
        }

    def payload(self, payload=None):
        if payload:
            self._payload = payload
            click = self._payload['click']
            if self._callbacks[click]:
                self._callbacks[click]()
        else:
            return self._payload

    def on_on(self, fn):
        self._callbacks['on'] = fn

    def on_off(self, fn):
        self._callbacks['off'] = fn

    def on_brightness_up(self, fn):
        self._callbacks['brightness_up'] = fn

    def on_brightness_down(self, fn):
        self._callbacks['brightness_down'] = fn

    def on_brightness_stop(self, fn):
        self._callbacks['on_brightness_stop'] = fn


class TRADFRI_REMOTE(MQTTDevice):
    def __init__(self, topic):
        MQTTDevice.__init__(self, 'E1810', topic, {
            'linkquality': None,
            'battery': None
        })
        self._callbacks = {
            'toggle': None,
            'arrow_left_click': None,
            'arrow_left_hold': None,
            'arrow_left_release': None,
            'arrow_right_click': None,
            'arrow_right_hold': None,
            'arrow_right_release': None,
            'brightness_up_click': None,
            'brightness_up_hold': None,
            'brightness_up_release': None,
            'brightness_down_click': None,
            'brightness_down_hold': None,
            'brightness_down_release': None
        }

    def payload(self, payload=None):
        if payload:
            self._payload = payload
            click = self._payload['action']
            if self._callbacks[click]:
                self._callbacks[click]()
        else:
            return self._payload

    def on_toggle(self, fn):
        self._callbacks['toggle'] = fn

    def on_arrow_left_click(self, fn):
        self._callbacks['arrow_left_click'] = fn

    def on_arrow_left_hold(self, fn):
        self._callbacks['arrow_left_hold'] = fn

    def on_arrow_left_release(self, fn):
        self._callbacks['arrow_left_release'] = fn
    
    def on_arrow_right_click(self, fn):
        self._callbacks['arrow_right_click'] = fn

    def on_arrow_right_hold(self, fn):
        self._callbacks['arrow_right_hold'] = fn

    def on_arrow_right_release(self, fn):
        self._callbacks['arrow_right_release'] = fn

    def on_brightness_up_click(self, fn):
        self._callbacks['brightness_up_click'] = fn

    def on_brightness_up_hold(self, fn):
        self._callbacks['brightness_up_hold'] = fn

    def on_brightness_up_release(self, fn):
        self._callbacks['brightness_up_release'] = fn

    def on_brightness_down_click(self, fn):
        self._callbacks['brightness_down_click'] = fn

    def on_brightness_down_hold(self, fn):
        self._callbacks['brightness_down_hold'] = fn

    def on_brightness_down_release(self, fn):
        self._callbacks['brightness_down_release'] = fn
