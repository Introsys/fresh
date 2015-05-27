#! /usr/bin/python

from PyQt4 import QtCore, QtGui
from gateway import Gateway

class MainWindow(QtGui.QWidget):
  
  def __init__(self, parent=None):
  
    super(MainWindow, self).__init__(parent)
    
    mainLayout = QtGui.QGridLayout()
    
    #DEVICE LIST
    deviceListGroup = QtGui.QGroupBox('Device List')
    self.deviceListLayout = QtGui.QGridLayout()
    deviceListGroup.setLayout(self.deviceListLayout)
    deviceListScroll = QtGui.QScrollArea()
    deviceListScroll.setWidget(deviceListGroup)
    deviceListScroll.setWidgetResizable(True)
    deviceListScroll.setFrameStyle(0)
    deviceListScroll.setMinimumWidth(300)
    
    #DEVICE INFO
    deviceInfoGroup = QtGui.QGroupBox('Device Info')
    deviceInfoLayout = QtGui.QGridLayout()
    deviceInfoGroup.setLayout(deviceInfoLayout)
    #deviceInfoScroll = QtGui.QScrollArea()
    #deviceInfoScroll.setWidget(deviceListGroup)
    #deviceInfoScroll.setWidgetResizable(True)
    self.deviceInfoText = QtGui.QTextEdit()
    deviceInfoLayout.addWidget(self.deviceInfoText)
    
    
    
    #deviceListLabel0 = QtGui.QLabel("Device List")
    #deviceListLabel1 = QtGui.QLabel("Device List")
    #deviceListLabel2 = QtGui.QLabel("Device List")
    #deviceListLabel3 = QtGui.QLabel("Device List")
    #deviceListLabel4 = QtGui.QLabel("Device List")
    #self.deviceListLayout.addWidget(deviceListLabel0, 0, 0)
    #self.deviceListLayout.addWidget(deviceListLabel1, 1, 0)
    #self.deviceListLayout.addWidget(deviceListLabel2, 2, 0)
    #self.deviceListLayout.addWidget(deviceListLabel3, 3, 0)
    #self.deviceListLayout.addWidget(deviceListLabel4, 4, 0)
    
    

    
    mainLayout.addWidget(deviceListScroll, 0, 0, QtCore.Qt.AlignTop)
    mainLayout.addWidget(deviceInfoGroup, 0, 1, QtCore.Qt.AlignTop)

    self.setLayout(mainLayout)
    self.setWindowTitle("FRESH Gateway")
    
    self.gateway = Gateway(port='/dev/ttyUSB0', baudrate=9600, parent=self)
    self.connect(self.gateway, QtCore.SIGNAL('newDevice'),
                 self.callbackNewDevice)
    
  def closeEvent(self, event):
    print "Closing the app"
    self.gateway.close()
    self.deleteLater()
    
  def callbackNewDevice(self):
    
    name = self.gateway.devices.keys()[-1]
    row = self.deviceListLayout.rowCount()
    print 'New Device: %s (index %d)'%(name, row)
    
    newEdit = QtGui.QLineEdit(name)
    newEdit.setEnabled(False)
    newBtn = QtGui.QToolButton()
    newBtn.setFixedSize(26, 26)
    newBtn.setIconSize(QtCore.QSize(20, 20))
    newBtn.setIcon(QtGui.QIcon('question_mark.png'))
    newBtn.setObjectName(name)
    newBtn.clicked.connect(self.callbackInfoBtnClicked)
    
    
    self.deviceListLayout.addWidget(newEdit, row, 0)
    self.deviceListLayout.addWidget(newBtn, row, 1)
    
  def callbackInfoBtnClicked(self):
    
    device = self.sender().objectName()
    type = self.gateway.devices[str(device)].element['type']
    is_pattern = self.gateway.devices[str(device)].element['isPattern']
    id = self.gateway.devices[str(device)].element['id']
    print 'info btn clicked for device %s'%device
    
    self.deviceInfoText.clear()
    self.deviceInfoText.append('addr: %s'%device)
    self.deviceInfoText.append('type: %s'%type)
    self.deviceInfoText.append('id: %s'%id)
    
    self.deviceInfoText.append('')
    
    for attr in self.gateway.devices[str(device)].attributes:
      attr_obj = self.gateway.devices[str(device)].attributes[attr]
      self.deviceInfoText.append('%s: %s'%(attr_obj['name'],attr_obj['value']))
    
    self.deviceInfoText.append('')
    
    for diag in self.gateway.devices[str(device)].diagnostic:
      diag_obj = self.gateway.devices[str(device)].diagnostic[diag]
      self.deviceInfoText.append('%s: %s'%(diag, diag_obj))    

if __name__ == '__main__':
  
  import sys
  
  app = QtGui.QApplication(sys.argv)
  
  mainWindowWidget = MainWindow()
  mainWindowWidget.show()
  
  sys.exit(app.exec_())