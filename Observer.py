import paho.mqtt.client as mqtt
import json


class Observer:
    def __init__(self, ip, base_topic):
        self._ip = ip
        self._base_topic = base_topic
        self._devices = {}

    def run(self):
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_diconnect
        self._client.on_subscribe = self._on_subscribe
        self._client.on_message = self._on_message

        self._client.connect(self._ip)
        for _, device in self._devices.items():
            self._client.subscribe(device.topic())

        self._client.loop_forever()

    def add_device(self, device):
        self._devices[device.topic()] = device

    def publish(self, topic, payload):
        self._client.publish(topic, payload)

    def _on_connect(self, client, userdata, flags, rc):
        pass

    def _on_diconnect(self, client, userdata, rc):
        pass

    def _on_subscribe(self, client, userdata, mid, granted_ops):
        pass

    def _on_message(self, client, userdata, msg):
        if msg.topic in self._devices:
            payload = json.loads(msg.payload.decode('utf8'))
            self._devices[msg.topic].payload(payload)
