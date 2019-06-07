from devices.MQTTDevice import MQTTDevice


class Philips_Hue_Color(MQTTDevice):
    def __init__(self, topic, fn_publish):
        MQTTDevice.__init__(self, '9290012573A', topic, {
            'state': 'off',
            'brightness': 0,
            'color': {'x': 0.0, 'y': 0.0},
            "color_temp": 153
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

    def color_temp(self, color_temp=None):
        if color_temp:
            color_temp = max(153, min(color_temp, 500))
            self._payload['color_temp'] = color_temp
            self._publish('{}/set'.format(self._topic), '{{"color_temp": "{}"}}'.format(color_temp))
        else:
            return self._payload['brightness']

    def is_on(self):
        return self._payload['state'].lower() == 'on'

    def is_off(self):
        return self._payload['state'].lower() == 'off'
