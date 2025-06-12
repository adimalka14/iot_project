from PyQt5.QtWidgets import QPushButton, QLineEdit
from .base_window import BaseWindow
from ..core import config

class ButtonWindow(BaseWindow):
    def __init__(self, mc):
        super().__init__("Button", mc)
        self.topic = QLineEdit(config.BUTTON_TOPIC)
        self.push  = QPushButton("PUBLISH 1")
        self.push.setStyleSheet("background:#808080;")
        self.form.addRow("Topic", self.topic)
        self.form.addRow("Send",  self.push)
        self.push.clicked.connect(self._on_click)

    def _on_click(self):
        self.mc.publish(self.topic.text(), '{"value":1}')