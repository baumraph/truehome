from devices.MQTTDevice import MQTTDevice


class IKEA_TRADFRI_LED(MQTTDevice):
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
