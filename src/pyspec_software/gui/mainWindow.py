from pyspec_software.gui.controlView import ControlView
from pyspec_software.gui.dataView import DataView
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QTabWidget, QAction
from PyQt5.QtCore import Qt, pyqtSlot
import logging
import os
from PyQt5 import uic

log = logging.getLogger(__name__)


MainWindowPath = os.path.dirname(os.path.realpath(__file__)) + '\\mainWindowUi.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(MainWindowPath)


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, model=None, controller=None):
        super(MainWindow, self).__init__()
        self.setAttribute(Qt.WA_AlwaysStackOnTop)
        self.setupUi(self)
        self.model = model

        self.create_views_and_dialogs()
        self.setup_window_tabs()
        self.setup_statusBar()
        self.setup_menuBar()
        self.connect_buttons()
        self.connect_signals()

    def setup_window_tabs(self):
        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)
        self.tabWidget.addTab(self.controlView, "Control View")
        self.tabWidget.addTab(self.dataView, "Data View")

    def setup_menuBar(self):
        pass

    def setup_statusBar(self):
        self.statusBarMessage = QLabel()
        self.statusbar.addWidget(self.statusBarMessage)
        self.controlView.device.s_pid_changed.connect(self.display_message)
        self.dataView.s_messageBar.connect(self.display_message)

    @pyqtSlot(str)
    def display_message(self, value):
        self.statusBarMessage.setText(value)

    def create_views_and_dialogs(self):
        self.controlView = ControlView()
        self.dataView = DataView()

    def connect_buttons(self):
        pass

    def connect_signals(self):
        pass

    def show_helpDialog(self):
        pass