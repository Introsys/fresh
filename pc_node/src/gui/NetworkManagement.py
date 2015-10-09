#!/usr/bin/python

# Form implementation generated from reading ui file 'NetworkManagement.ui'
#
# Created: Wed Aug 26 13:12:00 2015
#      by: PyQt4 UI code generator 4.10.4
# Please do not generate this file from the original NetworkManagement.ui
# or all the changes made to this document will be lost
# The Ui file serves only for making the template UI

import logging
from gui import Resources_rc
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot , pyqtSignal, SIGNAL, SLOT, QObject, Qt


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
class Ui_WidgetNetMang(QtGui.QWidget):
  
  
  
  sendAvailableSIM               =  pyqtSignal(object, name="sendAvailableSIM")
  sendSubscribeSIM               =  pyqtSignal(object, name="sendSubscribeSIM")
  
  addSelectedDevicesToSub        =  pyqtSignal(name="addSelectedDevicesToSub")
  
  removeSelectedDeviceFromSub    =  pyqtSignal(int, name="removeSelectedDeviceFromSub")
  editSelectedDeviceFromSub      =  pyqtSignal(int, 'QString', name="editSelectedDeviceFromSub")
  
  
  
  def __init__(self, parent = None):
    ''' '''
    super(Ui_WidgetNetMang, self).__init__()
    self.f_log = logging.getLogger('App') # this can be called in any place
    self.parentWidget = parent
    self.setupUi(self)
    Resources_rc.qInitResources()

    self.sim_sensors_av = QtGui.QStandardItemModel(parent=self.lv_sensors_av)
    self.lv_sensors_av.setModel(self.sim_sensors_av)
    
    self.sim_sensors_sub = QtGui.QStandardItemModel(self.lv_sensors_sub)
    self.lv_sensors_sub.setModel(self.sim_sensors_sub)
    
    QObject.connect(self.lv_sensors_av, SIGNAL('clicked(QModelIndex)'), self, SLOT('availableItemSelected(QModelIndex)'))
    QObject.connect(self.lv_sensors_sub, SIGNAL('clicked(QModelIndex)'), self, SLOT('subscribedItemSelected(QModelIndex)'))
    QObject.connect(self.pb_add, SIGNAL("clicked()"), self, SLOT("addButtonClicked()"))
    QObject.connect(self.pb_remove, SIGNAL("clicked()"), self, SLOT("removeButtonClicked()"))
    QObject.connect(self.pb_edit, SIGNAL("clicked()"), self, SLOT("editButtonClicked()"))
    
     
  # --------------------------------------------------------------------------
  
    
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
    
    # ------------------------------------------------------------------
    
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
    self.lv_sensors_sub = QtGui.QListView(self.w_nodes_sub)
    self.lv_sensors_sub.setFrameShadow(QtGui.QFrame.Plain)
    self.lv_sensors_sub.setObjectName(_fromUtf8("lv_sensors_sub"))
    self.verticalLayout_3.addWidget(self.lv_sensors_sub)
    
    
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
  # --------------------------------------------------------------------------
  

 
  def retranslateUi(self, WidgetNetMang):
    WidgetNetMang.setWindowTitle(_translate("WidgetNetMang", "Form", None))
    self.l_sensor_nodes_av.setText(_translate("WidgetNetMang", "Sensor Nodes Available", None))
    self.pb_add.setText(_translate("WidgetNetMang", "Add", None))
    self.label_2.setText(_translate("WidgetNetMang", "Sensor Nodes Subscribed (History Data)", None))
    self.pb_edit.setText(_translate("WidgetNetMang", "Edit", None))
    self.pb_remove.setText(_translate("WidgetNetMang", "Remove", None))
  # --------------------------------------------------------------------------
  
  
  
  
  '''
    Slots
  '''
    
  
    

  @pyqtSlot(name="lockUnlockAddButton")
  def lockUnlockAddButton(self):
    ''' 
      Lock Unlock the add button 
    '''
    if not self.pb_add.isEnabled() and self.sim_sensors_av.rowCount() > 0:
      self.pb_add.setEnabled(True)
    elif self.pb_add.isEnabled() and self.sim_sensors_av.rowCount() < 1:
      self.pb_add.setEnabled(False)
  # --------------------------------------------------------------------------
  

  @pyqtSlot(name="lockUnlockEditRemoveButton")
  def lockUnlockEditRemoveButton(self):
    ''' 
      Lock Unlock the edit and remove buttons 
    '''
    if not self.pb_edit.isEnabled() and not self.pb_remove.isEnabled() and self.sim_sensors_sub.rowCount() > 0:
      self.pb_edit.setEnabled(True)
      self.pb_remove.setEnabled(True)
    elif self.pb_edit.isEnabled() and self.pb_remove.isEnabled() and self.sim_sensors_sub.rowCount() < 1:
      self.pb_edit.setEnabled(False)
      self.pb_remove.setEnabled(False)

  # --------------------------------------------------------------------------


  @pyqtSlot(name="subscribeSIMRequest")
  def subscribeSIMRequest(self):
    self.sendSubscribeSIM.emit(self.sim_sensors_sub)
  # --------------------------------------------------------------------------  
  
  @pyqtSlot(name="availableSIMRequest")
  def availableSIMRequest(self):
    self.sendAvailableSIM.emit(self.sim_sensors_av)
  # --------------------------------------------------------------------------


  @pyqtSlot("QModelIndex", name="availableItemSelected")
  def availableItemSelected(self):
    '''
      Listener for when a item is selected on the available devices list
    '''
    self.lockUnlockAddButton()
  # --------------------------------------------------------------------------
  
  
  @pyqtSlot("QModelIndex", name="subscribedItemSelected")
  def subscribedItemSelected(self):
    '''
      Listener for when a item is selected on the subscription devices list
    '''
    self.lockUnlockEditRemoveButton()
  # --------------------------------------------------------------------------





  @pyqtSlot(name="addButtonClicked")
  def addButtonClicked(self):
    ''' 
      Returns a list of the index selected by the user
      The user can select more then one sensor node to add
    '''
    self.addSelectedDevicesToSub.emit()
    
    
  # --------------------------------------------------------------------------


  @pyqtSlot(name="editButtonClicked")
  def editButtonClicked(self):
    ''' 
      Returns the selected element of the list to be edited
      The user can only select one item at any given time
    '''
    if len(self.lv_sensors_sub.selectedIndexes()) > 0:
      newDescription, result = QtGui.QInputDialog.getText(self.parentWidget, 'Edit Descriptin', 'Please enter a new description:')
      if result:
        index = self.lv_sensors_sub.selectedIndexes()[0].row()
        self.editSelectedDeviceFromSub.emit(index, newDescription)
    else: 
      QtGui.QMessageBox.warning(self, "Warning", "Please select one element at least")
      
  # --------------------------------------------------------------------------

    
    
  # --------------------------------------------------------------------------
  
  
  @pyqtSlot(name="removeButtonClicked")
  def removeButtonClicked(self):
    ''' 
      Returns the selected element of the list to be removed
      The user can only select one item at any given time
    '''
    if len(self.lv_sensors_sub.selectedIndexes()) > 0:
      result = QtGui.QMessageBox.question(self, 'Confirmation', "Delete the selected item?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
      if result == QtGui.QMessageBox.Yes:
        self.removeSelectedDeviceFromSub.emit(self.lv_sensors_sub.selectedIndexes()[0].row())
    else: 
      QtGui.QMessageBox.warning(self, "Warning", "Please select one element at least")
      
  # --------------------------------------------------------------------------  

    
  
#EOF