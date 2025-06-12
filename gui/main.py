import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ..core.mqtt_client import MqttClient
from .button_window import ButtonWindow
from .dht_window import DhtWindow
from .relay_window import RelayWindow

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IoT Dashboard")
        self.mc = MqttClient()
        self.addDockWidget(0x1, ButtonWindow(self.mc))  # Qt.TopDockWidgetArea
        self.addDockWidget(0x1, DhtWindow(self.mc))
        self.addDockWidget(0x1, RelayWindow(self.mc))
        self.mc.connect()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main(); win.show()
    sys.exit(app.exec_())