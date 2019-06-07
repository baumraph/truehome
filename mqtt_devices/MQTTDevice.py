import json
import datetime


class MQTTDevice:
    def __init__(self, model, topic, payload):
        self._model = model
        self._topic = topic
        self._payload = payload
        self._update = None
        self._last_update = datetime.datetime(1970, 1, 1)
    
    def model(self):
        return self._model

    def topic(self):
        return self._topic

    def payload(self, payload=None):
        if payload:
            self._payload = payload
            if self._update:
                self._update()
            self._last_update = datetime.datetime.now()
        else:
            return json.dumps(self._payload)

    def on_update(self, fn):
        self._update = fn
    
    def last_update(self):
        return self._last_update
