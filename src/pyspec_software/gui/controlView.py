from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QIntValidator, QDoubleValidator
from pyqtgraph import PlotItem
import os
from pyqtgraph import mkPen, mkColor
import numpy as np
from PyQt5 import uic
import logging

log = logging.getLogger(__name__)

controlViewUiPath = os.path.dirname(os.path.realpath(__file__)) + "\\controlViewUi.ui"
Ui_controlView, QtBaseClass = uic.loadUiType(controlViewUiPath)

SIGNAL_PLOT_TOGGLED = "plot.toggled.indicator"


class ControlView(QWidget, Ui_controlView):
    SIGNAL_toggled_plot_indicator = "indicator"

    def __init__(self, model=None, controller=None):
        super(ControlView, self).__init__()

        self.device = None
        self.allPlotsDict = {}
        self.selectedType = "tri"
        self.setupUi(self)
        self.setup_buttons()
        self.connect_buttons()
        self.connect_signals()
        self.create_plots()
        self.initialize_view()

    def initialize_view(self):
        self.le_P.setText("0.5")
        self.le_D.setText("0")
        self.le_I.setText("1")

    def setup_buttons(self):
        # self.le_P.setValidator(QDoubleValidator())
        # self.le_D.setValidator(QDoubleValidator())
        # self.le_I.setValidator(QDoubleValidator())

        self.le_min.setValidator(QDoubleValidator())
        self.le_max.setValidator(QDoubleValidator())
        self.le_nbOfPoints.setValidator(QIntValidator())

        self.le_P.setMaxLength(5)
        self.le_I.setMaxLength(5)
        self.le_D.setMaxLength(5)

    def connect_buttons(self):
        log.debug("Connecting simulationView GUI...")
        # MAIN BUTTONS
        self.pb_launchCommand.clicked.connect(lambda: self.device.start_thread_routine())
        self.pb_stopCommand.clicked.connect(lambda: self.device.stop_command_routine())
        self.pb_clearGraph.clicked.connect(self.clear_graph)
        self.pb_read.clicked.connect(lambda: self.device.launch_read_without_command())
        self.pb_resetConnection.clicked.connect(self.reset_connection)
        self.pb_kill.clicked.connect(lambda: self.device.stop_routine())

        # BASCI PARAMETERS
        self.pb_send_PID.clicked.connect(lambda:self.device.set_pid_parameters(float(self.le_P.text()), float(self.le_I.text()),float(self.le_D.text())))

        # LIVE PARAMETERS
        self.le_cmdWaitTime.textChanged.connect(lambda: self.device.set_waitTime(int(self.le_cmdWaitTime.text())))
        self.cb_loop.toggled.connect(lambda: self.set_loop_enabled(self.cb_loop.checkState()))
        self.le_max.textChanged.connect(lambda: self.generate_command_list(self.le_min.text(), self.le_max.text(), self.le_nbOfPoints.text()))
        self.le_min.textChanged.connect(lambda: self.generate_command_list(self.le_min.text(), self.le_max.text(), self.le_nbOfPoints.text()))
        self.le_nbOfPoints.textChanged.connect(lambda: self.generate_command_list(self.le_min.text(), self.le_max.text(), self.le_nbOfPoints.text()))


        log.debug("Connections Established")

    def reset_connection(self):
        self.device.reset_connection()
        self.clear_graph()


    def set_loop_enabled(self, value):
        if value == 2:
            value = 1
        self.device.set_enabled_loop(value)

    def generate_command_list(self, min, max, nbOfPoints):
        if self.selectedType == "tri":
            commandList = list(np.linspace(float(min), float(max), int(nbOfPoints)))
            commandList2 = (list(np.linspace(float(max), float(min), int(nbOfPoints))))
            commandList += commandList2[1:]

            print(commandList)
            self.update_command_list(commandList)

    def update_command_list(self, commandList):
        self.device.save_command(commandList)

    def clear_graph(self):
        self.allPlotsDict["plot"]["temperature"].clear()
        self.device.clear_data()

    def connect_signals(self):
        log.debug("Connecting simulationView Signals...")
#        self.device.s_data_changed.connect(self.update_graph)

    def create_plots(self):
        self.allPlotsDict["plot"] = {"plotItem": PlotItem(), "displayed": 1}
        #self.allPlotsDict["plot"]["plotItem"].setXRange(0, 30000)
        red = mkColor('r')
        blue = mkColor('b')
        green = mkColor('g')
        dataPlotItem = self.allPlotsDict["plot"]["plotItem"].plot(pen=mkPen(red, width=2))
        self.allPlotsDict["plot"]["voltage"] = dataPlotItem
        dataPlotItem = self.allPlotsDict["plot"]["plotItem"].plot(pen=mkPen(blue, width=2))
        self.allPlotsDict["plot"]["current"] = dataPlotItem
        dataPlotItem = self.allPlotsDict["plot"]["plotItem"].plot(pen=mkPen(green, width=2))
        self.allPlotsDict["plot"]["temperature"] = dataPlotItem

        self.pyqtgraphWidget.addItem(self.allPlotsDict["plot"]["plotItem"])

    @pyqtSlot(dict)
    def update_graph(self, simPlotData):
        # print(simPlotData)
        for indicator in ['voltage', 'current', 'temperature']:
            kwargs = simPlotData[indicator]
            #print(kwargs['x'])
            if kwargs['x'] and len(kwargs['x']) >= 1000:
                self.clear_graph()
            self.allPlotsDict["plot"][indicator].setData(**kwargs)
        log.debug("Data confirmed")
