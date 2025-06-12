from PyQt5.QtWidgets import QWidget, QFormLayout, QDockWidget
from PyQt5.QtCore import pyqtSlot
from ..core.mqtt_client import MqttClient

class BaseWindow(QDockWidget):
    def __init__(self, title: str, mc: MqttClient, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle(title)
        self.mc = mc
        self.form = QFormLayout()
        container = QWidget()
        container.setLayout(self.form)
        self.setWidget(container)
        mc.connected.connect(self._on_conn_change)

    # unified visual feedback
    @pyqtSlot(bool)
    def _on_conn_change(self, ok: bool):
        self.setStyleSheet(f"background-color: {'#d4ffd4' if ok else '#ffd6d6'};")