from devices.MQTTDevice import MQTTDevice


class Xiaomi_Switch(MQTTDevice):
    def __init__(self, topic):
        MQTTDevice.__init__(self, 'WXKG01LM', topic, {
            'battery': None,
            'voltage': None
        })
        self._callbacks = {
            'single': None,
            'double': None,
            'triple': None,
            'quadruple': None,
            'many': None,
            'long': None,
            'long_release_click': None
        }

    def battery(self):
        return self._payload['battery']

    def voltage(self):
        return self._payload['voltage']

    def payload(self, payload=None):
        if payload:
            self._payload = payload
            click = self._payload['click']
            if self._callbacks[click]:
                self._callbacks[click]()
        else:
            return self._payload

    def on_single_click(self, fn):
        self._callbacks['single'] = fn

    def on_double_click(self, fn):
        self._callbacks['double'] = fn

    def on_triple_click(self, fn):
        self._callbacks['triple'] = fn

    def on_quadruple_click(self, fn):
        self._callbacks['quadruple'] = fn

    def on_many_click(self, fn):
        self._callbacks['many'] = fn

    def on_long_click(self, fn):
        self._callbacks['long'] = fn

    def on_long_release_click(self, fn):
        self._callbacks['long_release'] = fn

    
class Xiaomi_Temperature_Humidity(MQTTDevice):
    def __init__(self, topic):
        MQTTDevice.__init__(self, 'WSDCGQ01LM', topic, {
            'temperature': None,
            'humidity': None,
            'battery': None,
            'voltage': None
        })

    def temperature(self):
        return self._payload['temperature']

    def humidity(self):
        return self._payload['humidity']

    def battery(self):
        return self._payload['battery']

    def voltage(self):
        return self._payload['voltage']


class Xiaomi_Door_Window_Contact(MQTTDevice):
    def __init__(self, topic):
        MQTTDevice.__init__(self, 'MCCGQ01LM', topic, {
            'contact': None,
            'battery': None,
            'voltage': None
        })

    def is_opened(self):
        return self._payload['contact'] == 'false'

    def is_closed(self):
        return self._payload['contact'] == 'true'

    def battery(self):
        return self._payload['battery']

    def voltage(self):
        return self._payload['voltage']


class Xiaomi_Motion_Sensor(MQTTDevice):
    def __init__(self, topic):
        MQTTDevice.__init__(self, 'RTCGQ01LM', topic, {
            'occupancy': None,
            'battery': None,
            'voltage': None
        })

    def is_occupied(self):
        return self._payload['occupancy']

    def battery(self):
        return self._payload['battery']

    def voltage(self):
        return self._payload['voltage']
