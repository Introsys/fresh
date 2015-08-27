#!/usr/bin/python

# Form implementation generated from reading ui file 'NetworkManagement.ui'
#
# Created: Wed Aug 26 13:12:00 2015
#      by: PyQt4 UI code generator 4.10.4
# Please do not generate this file from the original NetworkManagement.ui
# or all the changes made to this document will be lost
# The Ui file serves only for making the template UI

import resources_rc
import simplejson as json
import os
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot #@UnusedImport
from communication.device import Device #@UnusedImport
from database.database_handler import DatabaseHandler #@UnusedImport
from database.database_manager import DatabaseManager #@UnusedImport


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
#
class Ui_WidgetNetMang(QtGui.QWidget):
  
  # ------------------------------------------------------------------
  #
  def __init__(self, parent = None):
    ''' '''
    super(Ui_WidgetNetMang, self).__init__()
    self.parentWidget = parent
    self.setupUi(self)
    self.helper = Ui_WidgetNetMangHelper(self)
    resources_rc.qInitResources()

    self.lv_model = QtGui.QStandardItemModel(parent=self.lv_sensors_av)
    self.lv_sensors_av.setModel(self.lv_model)
    

  
    # ------------------------------------------------------------------
    # Connects

    QtCore.QObject.connect(self.pb_add, QtCore.SIGNAL("clicked()"), 
                           self.helper, QtCore.SLOT("addSensor()"))
    
    QtCore.QObject.connect(self.pb_remove, QtCore.SIGNAL("clicked()"), 
                           self.helper, QtCore.SLOT("removeSensor()"))
    
    QtCore.QObject.connect(self.pb_edit, QtCore.SIGNAL("clicked()"), 
                           self.helper,  QtCore.SLOT("editSensor()"))
       
       
    
    QtCore.QObject.connect(self.lw_sensors_sub, QtCore.SIGNAL("itemClicked(QListWidgetItem *)"), 
                           self.helper,         QtCore.SLOT("itemSelectedFromList(QListWidgetItem *)"))
      
  
    # handle the dynamic allocation of new sensors to the list
    QtCore.QObject.connect(self.lv_model, QtCore.SIGNAL("rowsInserted(QModelIndex,int,int)"), self.lockUnlockAddButton)
    QtCore.QObject.connect(self.lv_model, QtCore.SIGNAL("rowsRemoved(QModelIndex,int,int)"), self.lockUnlockAddButton)
  
  
  # ------------------------------------------------------------------
  #
  
  def setupUi(self, WidgetNetMang):
    WidgetNetMang.setObjectName(_fromUtf8("WidgetNetMang"))
    WidgetNetMang.resize(800, 650)
    
    self.horizontalLayout_4 = QtGui.QHBoxLayout(WidgetNetMang)
    self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
    
    self.w_nodes_av = QtGui.QWidget(WidgetNetMang)
    self.w_nodes_av.setMinimumSize(QtCore.QSize(200, 0))
    self.w_nodes_av.setMaximumSize(QtCore.QSize(350, 16777215))
    self.w_nodes_av.setObjectName(_fromUtf8("w_nodes_av"))
    
    self.verticalLayout_4 = QtGui.QVBoxLayout(self.w_nodes_av)
    self.verticalLayout_4.setSpacing(5)
    self.verticalLayout_4.setMargin(0)
    self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
    
    # Left Table
    self.l_sensor_nodes_av = QtGui.QLabel(self.w_nodes_av)
    font = QtGui.QFont()
    font.setPointSize(12)
    self.l_sensor_nodes_av.setFont(font)
    self.l_sensor_nodes_av.setLayoutDirection(QtCore.Qt.LeftToRight)
    self.l_sensor_nodes_av.setAlignment(QtCore.Qt.AlignCenter)
    self.l_sensor_nodes_av.setObjectName(_fromUtf8("l_sensor_nodes_av"))
    self.verticalLayout_4.addWidget(self.l_sensor_nodes_av)
    self.lv_sensors_av = QtGui.QListView(self.w_nodes_av)
    self.lv_sensors_av.setObjectName(_fromUtf8("lv_sensors_av"))
    self.verticalLayout_4.addWidget(self.lv_sensors_av)
    
    # Left Table Menu
    self.f_menu_add = QtGui.QFrame(self.w_nodes_av)
    self.f_menu_add.setMinimumSize(QtCore.QSize(200, 40))
    self.f_menu_add.setMaximumSize(QtCore.QSize(350, 40))
    self.f_menu_add.setFrameShape(QtGui.QFrame.StyledPanel)
    self.f_menu_add.setObjectName(_fromUtf8("f_menu_add"))
    self.horizontalLayout_3 = QtGui.QHBoxLayout(self.f_menu_add)
    self.horizontalLayout_3.setSpacing(5)
    self.horizontalLayout_3.setMargin(5)
    self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
    spacerItem = QtGui.QSpacerItem(30, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_3.addItem(spacerItem)
    
    # Add Button
    self.pb_add = QtGui.QPushButton(self.f_menu_add)
    self.pb_add.setMinimumSize(QtCore.QSize(0, 30))
    self.pb_add.setMaximumSize(QtCore.QSize(100, 30))
    self.pb_add.setEnabled(False)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.pb_add.setIcon(icon)
    self.pb_add.setIconSize(QtCore.QSize(18, 18))
    self.pb_add.setObjectName(_fromUtf8("pb_add"))
    self.horizontalLayout_3.addWidget(self.pb_add)
    spacerItem1 = QtGui.QSpacerItem(30, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_3.addItem(spacerItem1)
    
    # ----------------------------------------------------------------------------------------------
    
    # Right Table
    self.verticalLayout_4.addWidget(self.f_menu_add)
    self.horizontalLayout_4.addWidget(self.w_nodes_av)
    self.w_nodes_sub = QtGui.QWidget(WidgetNetMang)
    self.w_nodes_sub.setObjectName(_fromUtf8("w_nodes_sub"))
    self.verticalLayout_3 = QtGui.QVBoxLayout(self.w_nodes_sub)
    self.verticalLayout_3.setSpacing(5)
    self.verticalLayout_3.setMargin(0)
    self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
    self.label_2 = QtGui.QLabel(self.w_nodes_sub)
    font = QtGui.QFont()
    font.setPointSize(12)
    self.label_2.setFont(font)
    self.label_2.setFrameShape(QtGui.QFrame.NoFrame)
    self.label_2.setAlignment(QtCore.Qt.AlignCenter)
    self.label_2.setObjectName(_fromUtf8("label_2"))
    self.verticalLayout_3.addWidget(self.label_2)
    self.lw_sensors_sub = QtGui.QListWidget(self.w_nodes_sub)
    self.lw_sensors_sub.setFrameShadow(QtGui.QFrame.Plain)
    self.lw_sensors_sub.setObjectName(_fromUtf8("lw_sensors_sub"))
    self.verticalLayout_3.addWidget(self.lw_sensors_sub)
    
    
    # Right Table Menu
    self.f_menu = QtGui.QFrame(self.w_nodes_sub)
    self.f_menu.setMinimumSize(QtCore.QSize(300, 40))
    self.f_menu.setMaximumSize(QtCore.QSize(16777215, 40))
    self.f_menu.setFrameShape(QtGui.QFrame.StyledPanel)
    self.f_menu.setObjectName(_fromUtf8("f_menu"))
    self.horizontalLayout_2 = QtGui.QHBoxLayout(self.f_menu)
    self.horizontalLayout_2.setSpacing(5)
    self.horizontalLayout_2.setMargin(5)
    self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
    spacerItem2 = QtGui.QSpacerItem(30, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_2.addItem(spacerItem2)
    
    # ------------------------------------------------------------------
    # Edit button
    self.pb_edit = QtGui.QPushButton(self.f_menu)
    self.pb_edit.setMinimumSize(QtCore.QSize(0, 30))
    self.pb_edit.setMaximumSize(QtCore.QSize(100, 30))
    self.pb_edit.setEnabled(False)
    icon1 = QtGui.QIcon()
    icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.pb_edit.setIcon(icon1)
    self.pb_edit.setIconSize(QtCore.QSize(18, 18))
    self.pb_edit.setObjectName(_fromUtf8("pb_edit"))
    self.horizontalLayout_2.addWidget(self.pb_edit)
    spacerItem3 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_2.addItem(spacerItem3)
    
    # ------------------------------------------------------------------
    # Remove button
    self.pb_remove = QtGui.QPushButton(self.f_menu)
    self.pb_remove.setMinimumSize(QtCore.QSize(0, 30))
    self.pb_remove.setMaximumSize(QtCore.QSize(100, 30))
    self.pb_remove.setEnabled(False)
    icon2 = QtGui.QIcon()
    icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.pb_remove.setIcon(icon2)
    self.pb_remove.setIconSize(QtCore.QSize(18, 16))
    self.pb_remove.setObjectName(_fromUtf8("pb_remove"))
    self.horizontalLayout_2.addWidget(self.pb_remove)
    spacerItem4 = QtGui.QSpacerItem(30, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_2.addItem(spacerItem4)
    self.verticalLayout_3.addWidget(self.f_menu)
    self.horizontalLayout_4.addWidget(self.w_nodes_sub)

    self.retranslateUi(WidgetNetMang)
    QtCore.QMetaObject.connectSlotsByName(WidgetNetMang)


  # ------------------------------------------------------------------
  #
  
  
  def retranslateUi(self, WidgetNetMang):
    WidgetNetMang.setWindowTitle(_translate("WidgetNetMang", "Form", None))
    self.l_sensor_nodes_av.setText(_translate("WidgetNetMang", "Sensor Nodes Available", None))
    self.pb_add.setText(_translate("WidgetNetMang", "Add", None))
    self.label_2.setText(_translate("WidgetNetMang", "Sensor Nodes Subscribed (History Data)", None))
    self.pb_edit.setText(_translate("WidgetNetMang", "Edit", None))
    self.pb_remove.setText(_translate("WidgetNetMang", "Remove", None))



  # --------------------------------------------------------------------------
  
  # --------------------------------------------------------------------------
  # Slots
    
  @pyqtSlot("QModelIndex,int,int")
  def lockUnlockAddButton(self, model_index, arga, argb):
    ''' unlock the add butto '''
    if not self.pb_add.isEnabled() and self.lv_model.rowCount() > 0:
      self.pb_add.setEnabled(True)
    elif self.pb_add.isEnabled() and self.lv_model.rowCount() < 0:
      self.pb_add.setEnabled(False)
  # --------------------------------------------------------------------------


  



# ----------------------------------------------------------------------------------------------
#
class Ui_WidgetNetMangHelper(QtCore.QObject):
  ''' '''
  
  notifyStatusBar = QtCore.pyqtSignal("QString", name="notifyStatusBar")

  def __init__(self, parent = None):
    super(Ui_WidgetNetMangHelper, self).__init__()
    self.parentWidget = parent
    self.lv_tableMap = dict()
    self.lw_tableMap = dict()
    
    self.databaseManager = DatabaseManager()
    dbfile = "freshdb"    
    if not os.path.isfile(dbfile):
      self.databaseManager.create_database(dbfile)
      print "new data base created"
    self.databaseHandler = DatabaseHandler(dbfile)
  
    subscriptions = self.databaseHandler.list_devices()
 
    if subscriptions:
      for device in subscriptions:
        #print "device Description {0}".format(device[4]) # NAME
        #print "device ID {0}".format(device[1]) # ID
        
        item_lw = QtGui.QListWidgetItem(str(device[4]))
        self.parentWidget.lw_sensors_sub.addItem(item_lw)
        self.lw_tableMap[item_lw] = device[1]
      
  
    QtCore.QObject.connect(self,                           QtCore.SIGNAL("notifyStatusBar(QString)"), 
                           self.parentWidget.parentWidget, QtCore.SLOT("updateStatusBarMessages(QString)"))
  # --------------------------------------------------------------------------
  
  @pyqtSlot()  
  def addSensor(self):
    
    ''' '''
    items_to_remove = []
    

    try:
      self.parentWidget.lv_sensors_av.setUpdatesEnabled(False)
      for row in range(self.parentWidget.lv_sensors_av.model().rowCount()):
          item = self.parentWidget.lv_sensors_av.model().item(row)
          if item.checkState() == QtCore.Qt.Checked:
            items_to_remove.append(row)
      for index in reversed(items_to_remove):
        item_lv = self.parentWidget.lv_sensors_av.model().item(index)
        item_lw = QtGui.QListWidgetItem(item_lv.text())
        device_id = self.lv_tableMap[item_lv]
        response = self.parentWidget.parentWidget.helper.gateway.cygnus_subscribe(device_id)
        if response: 
          json_response = json.loads(response)
          subscription_id = json_response['subscribeResponse']['subscriptionId']
          if subscription_id:
            #print "json_response add sensor {0} {1}".format(json_response, device_id)
            subscription_timeout = json_response['subscribeResponse']['duration']
            self.databaseHandler.add_device(device_id, subscription_id, subscription_timeout, device_id, True)
            self.parentWidget.lw_sensors_sub.addItem(item_lw)
            self.lw_tableMap[item_lw] = device_id
            self.parentWidget.lv_sensors_av.model().removeRow(index)
            self.lv_tableMap.pop(item_lv, None)
          else:
            self.notifyStatusBar.emit(QtCore.QString(response))
          self.parentWidget.lv_sensors_av.setUpdatesEnabled(True)
        else:
          self.notifyStatusBar.emit(QtCore.QString("Unable to connect to Server"))
    except IndexError as e:
      self.notifyStatusBar.emit(QtCore.QString("Erro: {0}".format(str(e))))
    except:
      e = sys.exc_info()[0]
      self.notifyStatusBar.emit(QtCore.QString("Erro: {0}".format(str(e))))
      
      
  # --------------------------------------------------------------------------

  @pyqtSlot(name="removeSensor")
  def removeSensor(self):
    ''' '''
    try:
      listItem = self.parentWidget.lw_sensors_sub.selectedItems()[0]
      device_id = self.lw_tableMap[listItem]
      index = self.parentWidget.lw_sensors_sub.row(listItem)
      device = self.databaseHandler.get_deivce(device_id)
      subscriptionId = device[2]
      #print "\nRemove sensor node: {0} with Subscription Id: {1}".format(device, subscriptionId)
      response = self.parentWidget.parentWidget.helper.gateway.cygnus_unsubscribe(subscriptionId)
      if response:
        json_response = json.loads(response)
        #print "Json Response {0}".format(json_response)
        if json_response['statusCode']['code'] == '200':
          self.parentWidget.lw_sensors_sub.removeItemWidget(listItem)
          self.parentWidget.lw_sensors_sub.takeItem(index)
          self.databaseHandler.remove_device(device_id)
          self.lw_tableMap.pop(listItem, None)
        else:
          self.notifyStatusBar.emit(QtCore.QString(response))
      else:
        self.notifyStatusBar.emit(QtCore.QString("Unable to connect to Server"))
        
      if self.parentWidget.lw_sensors_sub.count() == 0:
        self.parentWidget.pb_edit.setEnabled(False)
        self.parentWidget.pb_remove.setEnabled(False)
        #print len(self.lw_tableMap)
    except:
      e = sys.exc_info()[0]
      self.notifyStatusBar.emit(QtCore.QString("Erro: {0}".format(str(e))))
      
  # --------------------------------------------------------------------------

  @pyqtSlot(name="editSensor")
  def editSensor(self):
    ''' '''
    print len(self.lw_tableMap)
    
    item = self.parentWidget.lw_sensors_sub.selectedItems()[0]
    device_id = self.lw_tableMap[item]
         
    newDescription, ok = QtGui.QInputDialog.getText(self.parentWidget, 'Edit Descriptin', 
            'Please enter a new description:')
    if ok:
      item.setText(newDescription)
      self.databaseHandler.update_device_description(device_id, str(newDescription))

  # --------------------------------------------------------------------------

  @pyqtSlot("QListWidgetItem*",name="itemSelectedFromList")
  def itemSelectedFromList(self):
    ''' '''
    self.parentWidget.pb_edit.setEnabled(True)
    self.parentWidget.pb_remove.setEnabled(True)

  # --------------------------------------------------------------------------

  @pyqtSlot(object, name="updateSensorList")
  def updateSensorList(self, devices):
    ''' '''
    for key in devices.keys():
      device_id = key
      if not self.databaseHandler.get_deivce(device_id) and not device_id in self.lw_tableMap.values():
        print "Nao existe device na base de dados nem na lista"
        if not device_id in self.lv_tableMap.values():
          print "nao existe device na lista de devices"
          self.sensorNodeDiscovered(devices[device_id])
  # --------------------------------------------------------------------------

  @pyqtSlot(object, name="sensorNodeDiscovered")
  def sensorNodeDiscovered(self, device):
    '''  '''
    sensorNode = self.databaseHandler.get_deivce(device.id)
    if not sensorNode:
      dump = json.loads(json.dumps(device.element)) # DEBUG
      zone = dump['id']
      low = device.id[0:7]
      high = device.id[8:16] 
    
      item = QtGui.QStandardItem()
      item.setText("{0} - {1} {2}".format(zone, low.upper(), high.upper()))
      item.setEditable(False)
      item.setCheckable(True)
      self.parentWidget.lv_model.appendRow(item)
      self.lv_tableMap[item] = device.id
    else:
      print "no device found " # DEBUG
     
#     # DEBUG
#     print "\n"
#     print device.id
#     print "elements {0}".format(json.dumps(device.element))
#     print json.dumps(device.attributes)
#     print "\n"

  # --------------------------------------------------------------------------
  
    
    
    
#EOF