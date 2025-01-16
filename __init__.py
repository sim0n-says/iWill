import os
from PyQt5.QtWidgets import QAction, QMessageBox
from PyQt5.QtGui import QIcon

class iWill:
    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'iWill/icon.png')
        if not os.path.exists(icon_path):
            QMessageBox.critical(None, "Error", f"Icon file not found: {icon_path}")
            return
        self.action = QAction(QIcon(icon_path), "Inspecteur Will", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Inspecteur Will", self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("&Inspecteur Will", self.action)

    def run(self):
        from .iWill import ShapefileLoader
        self.dialog = ShapefileLoader()
        self.dialog.exec_()

def classFactory(iface):
    return iWill(iface)