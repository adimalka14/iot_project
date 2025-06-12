import json
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSlot
from .base_window import BaseWindow
from ..core import config

class RelayWindow(BaseWindow):
    """Shows ON/OFF state coming from `config.RELAY_TOPIC`.

    ✱ IMPORTANT: we subscribe *after* MQTT is connected, otherwise paho
    ignores the request.
    """

    def __init__(self, mc):
        super().__init__("Relay", mc)
        self.label = QLabel("…waiting…")
        self.form.addRow("State", self.label)

        # Subscribe only when we know the connection is up
        mc.connected.connect(self._on_conn)
        mc.message_in.connect(self._on_msg)

    @pyqtSlot(bool)
    def _on_conn(self, ok: bool):
        if ok:
            self.mc.subscribe(config.RELAY_TOPIC)

    @pyqtSlot(str, str)
    def _on_msg(self, topic, payload):
        if topic != config.RELAY_TOPIC:
            return
        print("[RelayWindow] incoming →", payload)
        try:
            state = "ON" if json.loads(payload).get("value") == 1 else "OFF"
        except json.JSONDecodeError:
            state = "ON" if '"value":1' in payload.replace(" ", "") else "OFF"
        self.label.setText(state)
        self.label.setStyleSheet(f"background:{'#ff9999' if state=='ON' else '#cccccc'};")