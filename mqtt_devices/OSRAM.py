from mqtt_devices.MQTTDevice import MQTTDevice


class OSRAM_SMART_PLUG(MQTTDevice):
    def __init__(self, topic, fn_publish):
        MQTTDevice.__init__(self, 'AB3257001NJ', topic, {
            'linkquality': None,
            'state': 'off'
        })
        self._publish = fn_publish

    def on(self):
        self._payload['state'] = 'on'
        self._publish('{}/set'.format(self._topic), '{"state": "on"}')
    
    def off(self):
        self._payload['state'] = 'off'
        self._publish('{}/set'.format(self._topic), '{"state": "off"}')

    def is_on(self):
        return self._payload['state'].lower() == 'on'

    def is_off(self):
        return self._payload['state'].lower() == 'off'
