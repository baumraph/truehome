import json


class MQTTDevice:
    def __init__(self, model, topic, payload):
        self._model = model
        self._topic = topic
        self._payload = payload
        self._update = None
    
    def model(self):
        return self._model

    def topic(self):
        return self._topic

    def payload(self, payload=None):
        if payload:
            self._payload = payload
            if self._update:
                self._update()
        else:
            return json.dumps(self._payload)

    def on_update(self, fn):
        self._update = fn
    