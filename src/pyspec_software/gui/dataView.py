from PyQt5.QtWidgets import QWidget, QLineEdit, QSlider
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread, QMutex
from pyqtgraph import PlotItem
import os
from PyQt5 import uic
import numpy as np
import logging
from pyspec_software.tools.Worker import Worker
import csv
from scipy.signal import *
import math
import threading

log = logging.getLogger(__name__)

dataViewUiPath = os.path.dirname(os.path.realpath(__file__)) + "\\dataViewUi.ui"
Ui_dataView, QtBaseClass = uic.loadUiType(dataViewUiPath)

SIGNAL_PLOT_TOGGLED = "plot.toggled.indicator"


class DataView(QWidget, Ui_dataView):
    SIGNAL_toggled_plot_indicator = "indicator"
    s_messageBar = pyqtSignal(str)
    s_data_ready = pyqtSignal()
    s_data_plot_ready = pyqtSignal(dict)

    def __init__(self, model=None, controller=None):
        super(DataView, self).__init__()
        self.setupUi(self)
        self.search_devices()
        self.setup_buttons()
        self.connect_buttons()
        self.connect_signals()
        self.create_plots()
        self.initialize_view()
        self.connect_threads()
        
        self.dataArray = [[]]
        self.formattedDataDict = {}

    def search_devices(self):
        deviceList = self.visaDevice.refresh_resource_list()
        self.cb_device.clear()
        self.cb_device.addItems(deviceList)

    def try_device_connection(self):
        try:
            deviceName = self.cb_device.currentText()
            self.visaDevice.change_instrument(deviceName)
            self.s_messageBar.emit("connection to {} succesful".format(deviceName))

        except Exception as e:
            print(e)
            self.s_messageBar.emit(str(e))

    def initialize_view(self):
        pass

    def setup_buttons(self):
        pass

    def connect_buttons(self):
        self.pb_connect.clicked.connect(lambda: self.try_device_connection())
        self.pb_startAcquisition.clicked.connect(lambda: self.start_acquisition_thread())
        self.pb_search.clicked.connect(lambda: self.search_devices())
        self.s_data_ready.connect(lambda: self.data_analysis())
        self.s_data_plot_ready.connect(self.update_graph)

    def connect_threads(self):
        pass

    def connect_signals(self):
        pass
