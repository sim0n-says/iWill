import os
from PyQt5.QtWidgets import QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from .iWill import ShapefileLoader

class iWill:
    def __init__(self, iface):
        self.iface = iface
        self.dock_widget = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
        if not os.path.exists(icon_path):
            QMessageBox.critical(None, "Error", f"Icon file not found: {icon_path}")
            return
        self.action = QAction(QIcon(icon_path), "Inspecteur Will", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Inspecteur Will", self.action)

    def unload(self):
        if self.dock_widget:
            self.iface.removeDockWidget(self.dock_widget)
            self.dock_widget = None
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("&Inspecteur Will", self.action)

    def run(self):
        if not self.dock_widget:
            self.dock_widget = ShapefileLoader()
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        self.dock_widget.show()

def classFactory(iface):
    return iWill(iface)