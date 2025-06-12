import random, json
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QTimer
from .base_window import BaseWindow
from ..core import config

class DhtWindow(BaseWindow):
    def __init__(self, mc):
        super().__init__("DHT", mc)
        self.topic  = config.DHT_TOPIC
        self.t_box  = QLineEdit(); self.t_box.setReadOnly(True)
        self.h_box  = QLineEdit(); self.h_box.setReadOnly(True)
        self.form.addRow("Temp (°C)", self.t_box)
        self.form.addRow("Hum (%)",  self.h_box)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._publish_fake)
        self.timer.start(config.UPDATE_RATE_MS)

    def _publish_fake(self):
        temp = round(22 + random.random()*1.5, 1)
        hum  = round(70 + random.random()*5 , 1)
        self.t_box.setText(str(temp))
        self.h_box.setText(str(hum))
        self.mc.publish(self.topic, json.dumps({"temperature": temp, "humidity": hum}))