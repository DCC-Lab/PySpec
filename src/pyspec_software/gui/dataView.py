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
        pass

    def try_device_connection(self):
        pass

    def initialize_view(self):
        pass

    def setup_buttons(self):
        pass

    def connect_buttons(self):
        pass
        # self.pb_connect.clicked.connect()
        # self.pb_startAcquisition.clicked.connect()
        # self.pb_search.clicked.connect()
        # self.s_data_ready.connect()
        # self.s_data_plot_ready.connect()

    def connect_threads(self):
        self.acqThread = QThread()
        self.acqWorker = Worker(self.acquisition_routine)
        self.acqWorker.moveToThread(self.acqThread)
        self.acqThread.started.connect(self.acqWorker.run)
        self.acqThread.finished.connect(lambda: self.s_messageBar.emit("acquisitionThread ended."))

        self.dataAnalysisThread = QThread()
        self.dataAnalysisWorker = Worker(self.data_analysis_routine)
        self.dataAnalysisWorker.moveToThread(self.dataAnalysisThread)
        self.dataAnalysisThread.started.connect(self.dataAnalysisWorker.run)
        self.dataAnalysisThread.finished.connect(lambda: self.s_messageBar.emit("dataAnalysisThread ended."))

    def acquisition_routine(self, *args, **kwargs):
        self.data_acquisition_routine()
        while self.chb_loop.isChecked():
            self.data_acquisition_routine()
        self.acqThread.terminate()

    def data_acquisition_routine(self, *args, **kwargs):
        log.info("Acquisition Begun...")

    def data_analysis_routine(self, *args, **kwargs):
        log.info("Data Analysis Begun...")

    def connect_signals(self):
        pass

    def clear_graph(self):
        self.allPlotsDict["plotDataItem"].clear()

    def create_plots(self):
        self.plotDict = {"plotItem": PlotItem(), "plotDataItem": None, "displayed": 1}
        self.pyqtgraphWidget.addItem(self.plotDict["plotItem"])
        self.plotDict["plotDataItem"] = self.plotDict["plotItem"].plot()

    @pyqtSlot(dict)
    def update_graph(self, data):
        self.plotDict["plotDataItem"].setData(**data)
        log.debug("Data confirmed")
