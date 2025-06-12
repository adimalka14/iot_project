from PyQt5.QtCore import QObject, pyqtSignal
import paho.mqtt.client as mqtt
import random, uuid
from . import config

class MqttClient(QObject):
    message_in  = pyqtSignal(str, str)          # topic, payload
    connected   = pyqtSignal(bool)              # True ⇢ ok, False ⇢ lost

    def __init__(self, parent=None):
        super().__init__(parent)
        print(config.BROKER_IP, config.BROKER_PORT)
        cid = f"IOT_client-{uuid.uuid4()}-{random.randrange(1, 1e6):06d}"
        self._cli = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, cid, transport="websockets")
        self._cli.tls_set()
        self._cli.username_pw_set(config.USERNAME, config.PASSWORD)

        # paho → Qt bridges
        self._cli.on_connect    = self._on_connect
        self._cli.on_disconnect = self._on_disconnect
        self._cli.on_message    = self._on_message
        self._cli.on_log        = lambda c,u,l,b: print("MQTT:", b)

    # — public API —
    def connect(self):
        self._cli.connect(config.BROKER_IP, config.BROKER_PORT)
        self._cli.loop_start()

    def publish(self, topic: str, payload: str):
        self._cli.publish(topic, payload)

    def subscribe(self, topic: str):
        self._cli.subscribe(topic)

    # — paho callbacks —
    def _on_connect(self, *_):
        self.connected.emit(True)

    def _on_disconnect(self, *_):
        self.connected.emit(False)

    def _on_message(self, _c, _u, msg):
        print("GUI-MQTT got:", msg.topic, msg.payload)  # DEBUG
        self.message_in.emit(msg.topic, msg.payload.decode("utf‑8", "ignore"))