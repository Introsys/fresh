#!/usr/bin/python


# Form implementation generated from reading ui file 'GetDetails.ui'
#
# Created: Wed Aug 19 14:37:28 2015
#      by: PyQt4 UI code generator 4.10.4
#
# Please do not generate this file from the original WidgetViewDetails.ui
# or all the changes made to this document will be lost
# The Ui file serves only for making the template UI

import resources_rc
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import pyqtSlot, QTimer
from PyQt4.QtCore import pyqtSignal #@UnusedImport
from PyQt4.QtGui import QListWidgetItem #@UnusedImport
import simplejson as json #@UnusedImport
import copy


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

  # --------------------------------------------------------------------------
  def __init__(self, parent = None):
    super(Ui_WidgetViewDetails, self).__init__()
    self.setupUi(self)
    self.__parentWidget = parent
    self.helper = Ui_WidgetViewDetailsHelper(self)
    resources_rc.qInitResources()
        
    QtCore.QObject.connect(self.lw_sensors, QtCore.SIGNAL("itemClicked(QListWidgetItem *)"), 
                           self.helper, QtCore.SLOT("itemSelectedFromList(QListWidgetItem *)"))
    

  # --------------------------------------------------------------------------
  def setupUi(self, WidgetViewDetails):
    ''' '''
    
    WidgetViewDetails.setObjectName(_fromUtf8("WidgetViewDetails"))
    WidgetViewDetails.resize(771, 448)
    
    self.horizontalLayout = QtGui.QHBoxLayout(WidgetViewDetails)
    self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
    self.lw_sensors = QtGui.QListWidget(WidgetViewDetails)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(1)
    sizePolicy.setVerticalStretch(1)
    sizePolicy.setHeightForWidth(self.lw_sensors.sizePolicy().hasHeightForWidth())
    
    # ------------------------------------------------------------------
    # Sensor List
    self.lw_sensors.setSizePolicy(sizePolicy)
    self.lw_sensors.setMinimumSize(QtCore.QSize(250, 0))
    self.lw_sensors.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    #self.lw_sensors.setMaximumSize(QtCore.QSize(300, 16777215))
    self.lw_sensors.setObjectName(_fromUtf8("lw_sensors"))
    self.horizontalLayout.addWidget(self.lw_sensors)
    
    
    
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
  # ----------------------------------------------------------------------------------------------




# ----------------------------------------------------------------------------------------------
class Ui_WidgetViewDetailsHelper(QtCore.QObject):
  ''' '''
  updateSensorNodeInfo = pyqtSignal("QListWidgetItem *", name="updateSensorNodeInfo")

  def __init__(self, parent = None):
    super(Ui_WidgetViewDetailsHelper, self).__init__()
    self.parentWidget = parent
    self.devicesDetails = dict()
    self.devicesItems = dict()
    self.timerUpdateInfo = QTimer(self)
    self.timerUpdateInfo.setSingleShot(True)
    
    QtCore.QObject.connect(self.timerUpdateInfo, QtCore.SIGNAL("timeout()"), self.refreshWidget)
    QtCore.QObject.connect(self, QtCore.SIGNAL("updateSensorNodeInfo(QListWidgetItem *)"), self.itemSelectedFromList)
    
  
  
  @pyqtSlot()
  def refreshWidget(self):
    ''' '''
    item = self.parentWidget.lw_sensors.selectedItems()[0]
    self.updateSensorNodeInfo.emit(item)
  
  
  @pyqtSlot("QListWidgetItem *")
  def itemSelectedFromList(self, item):
    ''' '''
    _id = self.devicesItems[item]
    _device = self.devices[_id]
    low = _device.id[0:7]
    high = _device.id[8:16] 
    self.parentWidget.sensor_details.clear()
    self.parentWidget.sensor_details.append("Address: {0}-{1}".format(low,high))
    self.parentWidget.sensor_details.append("Type: {0}".format(_device.element['isPattern']))
    self.parentWidget.sensor_details.append("Id: {0}".format(_device.element['id']))
    
    for attr in _device.attributes:
      attr_obj = _device.attributes[attr]
      self.parentWidget.sensor_details.append("{0}: {1}".format(attr_obj['name'],attr_obj['value']))
    
    self.parentWidget.sensor_details.append('\n\n')
    
    for diag in _device.diagnostic:
      diag_obj = _device.diagnostic[diag]
      self.parentWidget.sensor_details.append("{0}: {1}".format(diag, diag_obj)) 
    
    self.timerUpdateInfo.start(2000)
  

  @pyqtSlot(object, name="addSensorNodeToDetails")
  def addSensorNodeToDetails(self, device):
    ''' '''
    dump = json.loads(json.dumps(device.element)) # DEBUG
    zone = dump['id']
    low = device.id[0:7]
    high = device.id[8:16] 
    
    #print dump
    #print device.id
    
    item = QtGui.QListWidgetItem("{0} - {1} {2}".format(zone, low.upper(), high.upper()))
    self.parentWidget.lw_sensors.addItem(item)
    self.devicesItems[item] = device.id
    

  
  @pyqtSlot(object)
  def showSensorNodeAttributes(self, device):
    ''' '''
    self.devices = copy.deepcopy(device) # This is not optimal... this objects exists in three different places
    #self.devices = device # This is not optimal... this objects exists in three different places
    
  


#EOF