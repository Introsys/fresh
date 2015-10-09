#!/usr/bin/python


# Form implementation generated from reading ui file 'GetDetails.ui'
#
# Created: Wed Aug 19 14:37:28 2015
#      by: PyQt4 UI code generator 4.10.4
#
# Please do not generate this file from the original WidgetViewDetails.ui
# or all the changes made to this document will be lost
# The Ui file serves only for making the template UI

import logging
from gui import Resources_rc
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal, pyqtSlot, QObject, SIGNAL, SLOT, QModelIndex


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  def _fromUtf8(s):
    return s

try:
  _encoding = QtGui.QApplication.UnicodeUTF8
  def _translate(context, text, disambig):
    return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
  def _translate(context, text, disambig):
    return QtGui.QApplication.translate(context, text, disambig)



# ----------------------------------------------------------------------------------------------
class Ui_WidgetViewDetails(QtGui.QWidget):

  
  sendMonitorSIM = pyqtSignal(object, name="sendMonitorSIM")
  askForDeviceDetails    = pyqtSignal(int, name="askForDeviceDetails")
  sendSelectedDevice     = pyqtSignal(int, name="sendSelectedDevice")
  
  
  
  def __init__(self, parent = None):
    super(Ui_WidgetViewDetails, self).__init__()
    self.f_log = logging.getLogger('App') # this can be called in any place
    self.setupUi(self)
    self.__parentWidget = parent
    Resources_rc.qInitResources()
    
    self.sim_sensors = QtGui.QStandardItemModel(self.lv_sensors)
    self.lv_sensors.setModel(self.sim_sensors)
    
    QObject.connect(self.lv_sensors, SIGNAL('clicked(QModelIndex)'), self, SLOT('deviceSelectedFromList(QModelIndex)'))
    
    
    
    # Attributes mapping 
    
    self.__attributesMap = {'SoilTemp': ('Soil Temperature', 'Celsius'),
                            'AirTemperature': ('Air Temperature', 'Celsius'),
                            'AirHumidity': ('Air Humidity', 'Percent'),
                            'CO2': ('CO2 level', 'ppm'),
                            'Moisture': ('Moisture', 'Percent'),
                            'PH': ('Ph level', 'ppm'),
                            'OD': ('Disolved Oxigen (DO)', 'ppm'),
                            'EC': ('Electrical Conductivity (EC)', 'ppm'),
                            'ORP': ('Oxidation Reduction Potential (ORP)', 'ppm'),
                            'R': ('RGB Red level', 'lx'),
                            'G': ('RGB Green level', 'lx'),
                            'B': ('RGB Blue level', 'lx'),
                            'lxr': ('Red light intensity', 'lx'),
                            'lxg': ('Green light intensity', 'lx'),
                            'lxb': ('Blue light intensity', 'lx'),
                            'lxtotal': ('Total light intensity', 'lx'),
                            'lxbeyond': ('Beyond visible spectrum', 'lx'),
                            'SoilHumidity': ('Soil Humidity', 'Percent'),
                            'SoilTemperature': ('Soil Temperature', 'Celsius'),
                            'AirTemperature': ('Air Temperature', 'Celsius'),
                            'AirHumidity': ('Air Humidity', 'Percent'),
                            'RTCTIME': ('Timestamp (from last reading)', '')
                      }    
    self.__digMap = {'Volt': ('Voltage','mV'), 'Temp': ('Temperature','Celsius'), 'Sign': ('Signal Strength','dB')}
    
  # --------------------------------------------------------------------------      
    
  
  def setupUi(self, WidgetViewDetails):
    ''' '''
    
    WidgetViewDetails.setObjectName(_fromUtf8("WidgetViewDetails"))
    WidgetViewDetails.resize(771, 448)
    
    self.horizontalLayout = QtGui.QHBoxLayout(WidgetViewDetails)
    self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
    
    
    # ------------------------------------------------------------------
    # Sensor List
    # TODO
    self.lv_sensors = QtGui.QListView(WidgetViewDetails)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(1)
    sizePolicy.setVerticalStretch(1)
    sizePolicy.setHeightForWidth(self.lv_sensors.sizePolicy().hasHeightForWidth())
    self.lv_sensors.setSizePolicy(sizePolicy)
    self.lv_sensors.setMinimumSize(QtCore.QSize(250, 0))
    self.lv_sensors.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    self.lv_sensors.setObjectName(_fromUtf8("lv_sensors"))
    self.horizontalLayout.addWidget(self.lv_sensors)
    
    
    
    # ------------------------------------------------------------------
    # Sensor details
    self.f_main = QtGui.QFrame(WidgetViewDetails)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(3)
    sizePolicy.setVerticalStretch(3)
    sizePolicy.setHeightForWidth(self.f_main.sizePolicy().hasHeightForWidth())
    self.f_main.setSizePolicy(sizePolicy)
    self.f_main.setFrameShape(QtGui.QFrame.NoFrame)
    self.f_main.setFrameShadow(QtGui.QFrame.Plain)
    self.f_main.setObjectName(_fromUtf8("f_main"))
    self.horizontalLayout.addWidget(self.f_main)
    self.sensor_details = QtGui.QTextEdit()
    self.sensor_details.setReadOnly(True)
    self.verticalLayout = QtGui.QHBoxLayout(self.f_main)
    self.verticalLayout.setSpacing(0)
    self.verticalLayout.setMargin(0)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    self.sensor_details.setSizePolicy(sizePolicy)
    self.verticalLayout.addWidget(self.sensor_details)



    
    self.retranslateUi(WidgetViewDetails)
    QtCore.QMetaObject.connectSlotsByName(WidgetViewDetails)
    
  # --------------------------------------------------------------------------

  
  def retranslateUi(self, WidgetViewDetails):
    ''' '''
    WidgetViewDetails.setWindowTitle(_translate("WidgetViewDetails", "Form", None))
  # --------------------------------------------------------------------------


  # -----------------------------------------------------------------------------
  # SLOTS
  # -----------------------------------------------------------------------------


  @pyqtSlot(name="monitorSIMRequest")
  def monitorSIMRequest(self):
    self.sendMonitorSIM.emit(self.sim_sensors)
  # --------------------------------------------------------------------------
      
  
  @pyqtSlot(QModelIndex, name="deviceSelectedFromList")
  def deviceSelectedFromList(self, index):
    self.askForDeviceDetails.emit(index.row())
  # --------------------------------------------------------------------------


  @pyqtSlot(object, name="displayDeviceDetails")
  def displayDeviceDetails(self, device):
    ''' 
      TODO - Description
    '''
    # THIS NEEDS TO BE IMPROVED
    try:
      low = device.id[0:7]
      high = device.id[8:16] 
      self.sensor_details.clear()
      self.sensor_details.append('[Sensor Header]')
      self.sensor_details.append('Mac Address: {0} {1}'.format(low.upper(),high.upper()))
      #self.sensor_details.append("Type: {0}".format(device.element['isPattern']))
      self.sensor_details.append('Sensor ID: {0}'.format(device.element['id']))
      self.sensor_details.append('\n[Sensor Data]')
      for attr in device.attributes:
        attr_obj = device.attributes[attr]
        self.sensor_details.append('{0}: {1} {2}'.format(self.__attributesMap[attr_obj['name']][0],attr_obj['value'],self.__attributesMap[attr_obj['name']][1]))
      self.sensor_details.append('\n[Sensor Diagnostic Info]')
      for diag in device.diagnostic:
        diag_obj = device.diagnostic[diag]
        self.sensor_details.append('{0}: {1} {2}'.format(self.__digMap[diag][0], diag_obj, self.__digMap[diag][1])) 
    except Exception as e:
      print str(e)
  # --------------------------------------------------------------------------
  
  
  @pyqtSlot(name="returnSelectedDevice")
  def returnSelectedDevice(self):
    ''' '''
    try:
      index = self.lv_sensors.selectedIndexes()
      if index:
        self.sendSelectedDevice.emit(index[0].row())
      else:
        self.sensor_details.clear()
    except Exception as e:
      print str(e)
  # --------------------------------------------------------------------------
  
  
  
  

#EOF