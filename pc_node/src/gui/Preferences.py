#!/usr/bin/python

# Form implementation generated from reading ui file 'Preferences.ui'
#
# Created: Thu Aug 20 15:29:04 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui
import resources_rc
import os.path
import shutil
import logging
import yaml
import simplejson as json
from PyQt4.QtCore import QObject, pyqtSlot #@UnusedImport
from bzrlib.osutils import dirname #@UnusedImport




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
class Ui_Preferences(QtGui.QWidget):
  ''' '''
  # --------------------------------------------------------------------------
  # Declaration of custom signals for communication with the helper class
  savePreferencesToFile = QtCore.pyqtSignal() 
  loadPreferencesFromFile = QtCore.pyqtSignal()
     
  # --------------------------------------------------------------------------
  def __init__(self, parent = None):
    super(Ui_Preferences, self).__init__()
    self.__parentWidget = parent
    self.auth_token = ""
    resources_rc.qInitResources()
    self.setupUi(self)
    self.helper = Ui_PreferencesHelper(self)
    self.token_loded = False

    QtCore.QObject.connect(self.pb_open_file_dialog, QtCore.SIGNAL('clicked()'), self.openAccessTokenFile)
    QtCore.QObject.connect(self.pb_reset, QtCore.SIGNAL('clicked()'), self.loadPreferences)
    QtCore.QObject.connect(self.pb_save, QtCore.SIGNAL('clicked()'), self.savePreferences)

  # --------------------------------------------------------------------------
  def setupUi(self, Preferences):
    
    # ------------------------------------------------------------------
    Preferences.setObjectName(_fromUtf8("Preferences"))
    Preferences.resize(600, 500)
    
    
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(Preferences.sizePolicy().hasHeightForWidth())
    Preferences.setSizePolicy(sizePolicy)
    
    
    self.verticalLayout = QtGui.QVBoxLayout(Preferences)
    self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
    
    # ------------------------------------------------------------------
    # TabWidget
    self.tb_preferences = QtGui.QTabWidget(Preferences)
    self.tb_preferences.setObjectName(_fromUtf8("tb_preferences"))
    
    
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Tab Pane - Network
    self.w_network = QtGui.QWidget()
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.w_network.sizePolicy().hasHeightForWidth())
    self.w_network.setSizePolicy(sizePolicy)
    self.w_network.setObjectName(_fromUtf8("w_network"))
    self.gridLayout_2 = QtGui.QGridLayout(self.w_network)
    self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
    self.l_keystone_url = QtGui.QLabel(self.w_network)
    self.l_keystone_url.setObjectName(_fromUtf8("l_keystone_url"))
    self.gridLayout_2.addWidget(self.l_keystone_url, 0, 0, 1, 1)
    self.le_keystone_url = QtGui.QLineEdit(self.w_network)
    self.le_keystone_url.setObjectName(_fromUtf8("le_keystone_url"))
    self.gridLayout_2.addWidget(self.le_keystone_url, 0, 1, 1, 1)
    
    
    # Separator
    self.line_01 = QtGui.QFrame(self.w_network)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_01.sizePolicy().hasHeightForWidth())
    self.line_01.setSizePolicy(sizePolicy)
    self.line_01.setFrameShape(QtGui.QFrame.HLine)
    self.line_01.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_01.setObjectName(_fromUtf8("line_01"))
    self.gridLayout_2.addWidget(self.line_01, 1, 0, 1, 2)
    
    
    # ------------------------------------------------------------------
    self.l_keystone_ip = QtGui.QLabel(self.w_network)
    self.l_keystone_ip.setObjectName(_fromUtf8("l_keystone_ip"))
    self.gridLayout_2.addWidget(self.l_keystone_ip, 2, 0, 1, 1)
    self.le_keystone_ip = QtGui.QLineEdit(self.w_network)
    self.le_keystone_ip.setObjectName(_fromUtf8("le_keystone_ip"))
    self.gridLayout_2.addWidget(self.le_keystone_ip, 2, 1, 1, 1)
    
    # Separator
    self.line_02 = QtGui.QFrame(self.w_network)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_02.sizePolicy().hasHeightForWidth())
    self.line_02.setSizePolicy(sizePolicy)
    self.line_02.setFrameShape(QtGui.QFrame.HLine)
    self.line_02.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_02.setObjectName(_fromUtf8("line_02"))
    self.gridLayout_2.addWidget(self.line_02, 3, 0, 1, 2)
    
    # ------------------------------------------------------------------
    self.l_keystone_port = QtGui.QLabel(self.w_network)
    self.l_keystone_port.setObjectName(_fromUtf8("l_keystone_port"))
    self.gridLayout_2.addWidget(self.l_keystone_port, 4, 0, 1, 1)
    self.le_keystone_port = QtGui.QLineEdit(self.w_network)
    self.le_keystone_port.setObjectName(_fromUtf8("le_keystone_port"))
    self.gridLayout_2.addWidget(self.le_keystone_port, 4, 1, 1, 1)
    
    # Separator
    self.line_03 = QtGui.QFrame(self.w_network)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_03.sizePolicy().hasHeightForWidth())
    self.line_03.setSizePolicy(sizePolicy)
    self.line_03.setFrameShape(QtGui.QFrame.HLine)
    self.line_03.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_03.setObjectName(_fromUtf8("line_03"))
    self.gridLayout_2.addWidget(self.line_03, 5, 0, 1, 2)
    
    # ------------------------------------------------------------------
    self.l_orion_ip = QtGui.QLabel(self.w_network)
    self.l_orion_ip.setObjectName(_fromUtf8("l_orion_ip"))
    self.gridLayout_2.addWidget(self.l_orion_ip, 6, 0, 1, 1)
    self.le_orion_ip = QtGui.QLineEdit(self.w_network)
    self.le_orion_ip.setObjectName(_fromUtf8("le_orion_ip"))
    self.gridLayout_2.addWidget(self.le_orion_ip, 6, 1, 1, 1)
    
    # Separator
    self.line_04 = QtGui.QFrame(self.w_network)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_04.sizePolicy().hasHeightForWidth())
    self.line_04.setSizePolicy(sizePolicy)
    self.line_04.setFrameShape(QtGui.QFrame.HLine)
    self.line_04.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_04.setObjectName(_fromUtf8("line_04"))
    self.gridLayout_2.addWidget(self.line_04, 7, 0, 1, 2)
    
    # ------------------------------------------------------------------
    self.l_orion_port = QtGui.QLabel(self.w_network)
    self.l_orion_port.setObjectName(_fromUtf8("l_orion_port"))
    self.gridLayout_2.addWidget(self.l_orion_port, 8, 0, 1, 1)
    self.le_orion_port = QtGui.QLineEdit(self.w_network)
    self.le_orion_port.setObjectName(_fromUtf8("le_orion_port"))
    self.gridLayout_2.addWidget(self.le_orion_port, 8, 1, 1, 1)
     
  
    
    # Separator
    self.line_05 = QtGui.QFrame(self.w_network)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_05.sizePolicy().hasHeightForWidth())
    self.line_05.setSizePolicy(sizePolicy)
    self.line_05.setFrameShape(QtGui.QFrame.HLine)
    self.line_05.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_05.setObjectName(_fromUtf8("line_05"))
    self.gridLayout_2.addWidget(self.line_05, 9, 0, 1, 2)
    
    # ------------------------------------------------------------------
    self.l_auto_connect = QtGui.QLabel(self.w_network)
    self.l_auto_connect.setObjectName(_fromUtf8("l_auto_connect"))
    self.gridLayout_2.addWidget(self.l_auto_connect, 10, 0, 1, 1)
    self.cb_auto_connect = QtGui.QCheckBox(self.w_network)
    self.cb_auto_connect.setObjectName(_fromUtf8("cb_auto_connect"))  
    self.gridLayout_2.addWidget(self.cb_auto_connect, 10, 1, 1, 1)
    
    # Spacer
    spacerItem = QtGui.QSpacerItem(620, 233, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.gridLayout_2.addItem(spacerItem, 11, 0, 1, 2)
    self.tb_preferences.addTab(self.w_network, _fromUtf8(""))
    
    
    
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Tab Pane - Security
    self.w_security = QtGui.QWidget()
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.w_security.sizePolicy().hasHeightForWidth())
    self.w_security.setSizePolicy(sizePolicy)
    self.w_security.setObjectName(_fromUtf8("w_security"))
    self.gridLayout = QtGui.QGridLayout(self.w_security)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.l_username = QtGui.QLabel(self.w_security)
    self.l_username.setObjectName(_fromUtf8("l_username"))
    self.gridLayout.addWidget(self.l_username, 0, 0, 1, 1)
    self.le_username = QtGui.QLineEdit(self.w_security)
    self.le_username.setObjectName(_fromUtf8("le_username"))
    self.gridLayout.addWidget(self.le_username, 0, 1, 1, 1)
    
    # Separator
    self.line_06 = QtGui.QFrame(self.w_security)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_06.sizePolicy().hasHeightForWidth())
    self.line_06.setSizePolicy(sizePolicy)
    self.line_06.setFrameShape(QtGui.QFrame.HLine)
    self.line_06.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_06.setObjectName(_fromUtf8("line_06"))
    self.gridLayout.addWidget(self.line_06, 1, 0, 1, 2)
    
    # ------------------------------------------------------------------
    self.l_password = QtGui.QLabel(self.w_security)
    self.l_password.setObjectName(_fromUtf8("l_password"))
    self.gridLayout.addWidget(self.l_password, 2, 0, 1, 1)
    self.le_password = QtGui.QLineEdit(self.w_security)
    self.le_password.setEchoMode(QtGui.QLineEdit.Password)
    self.le_password.setObjectName(_fromUtf8("le_password"))
    self.gridLayout.addWidget(self.le_password, 2, 1, 1, 1)
    
    # Separator
    self.line_07 = QtGui.QFrame(self.w_security)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_07.sizePolicy().hasHeightForWidth())
    self.line_07.setSizePolicy(sizePolicy)
    self.line_07.setFrameShape(QtGui.QFrame.HLine)
    self.line_07.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_07.setObjectName(_fromUtf8("line_07"))
    self.gridLayout.addWidget(self.line_07, 3, 0, 1, 2)
    
    # ------------------------------------------------------------------
    self.l_tennant_name = QtGui.QLabel(self.w_security)
    self.l_tennant_name.setObjectName(_fromUtf8("l_tennant_name"))
    self.gridLayout.addWidget(self.l_tennant_name, 4, 0, 1, 1)
    self.le_tenant_name = QtGui.QLineEdit(self.w_security)
    self.le_tenant_name.setObjectName(_fromUtf8("le_tenant_name"))
    self.gridLayout.addWidget(self.le_tenant_name, 4, 1, 1, 1)
    
    # Separator
    self.line_08 = QtGui.QFrame(self.w_security)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_08.sizePolicy().hasHeightForWidth())
    self.line_08.setSizePolicy(sizePolicy)
    self.line_08.setFrameShape(QtGui.QFrame.HLine)
    self.line_08.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_08.setObjectName(_fromUtf8("line_08"))
    self.gridLayout.addWidget(self.line_08, 5, 0, 1, 2)
   
    # ------------------------------------------------------------------
    self.l_tennant_id = QtGui.QLabel(self.w_security)
    self.l_tennant_id.setObjectName(_fromUtf8("l_tennant_id"))
    self.gridLayout.addWidget(self.l_tennant_id, 6, 0, 1, 1)
    self.le_tenant_id = QtGui.QLineEdit(self.w_security)
    self.le_tenant_id.setObjectName(_fromUtf8("le_tenant_id"))
    self.gridLayout.addWidget(self.le_tenant_id, 6, 1, 1, 1)
    
    
    # Separator
    self.line_09 = QtGui.QFrame(self.w_security)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_09.sizePolicy().hasHeightForWidth())
    self.line_09.setSizePolicy(sizePolicy)
    self.line_09.setFrameShape(QtGui.QFrame.HLine)
    self.line_09.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_09.setObjectName(_fromUtf8("line_09"))
    self.gridLayout.addWidget(self.line_09, 7, 0, 1, 2)
    
    # ------------------------------------------------------------------
    self.l_domain = QtGui.QLabel(self.w_security)
    self.l_domain.setObjectName(_fromUtf8("l_domain"))
    self.gridLayout.addWidget(self.l_domain, 8, 0, 1, 1)
    self.le_domain = QtGui.QLineEdit(self.w_security)
    self.le_domain.setObjectName(_fromUtf8("le_domain"))
    self.gridLayout.addWidget(self.le_domain, 8, 1, 1, 1)
    
    # Separator
    self.line_10 = QtGui.QFrame(self.w_security)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_10.sizePolicy().hasHeightForWidth())
    self.line_10.setSizePolicy(sizePolicy)
    self.line_10.setFrameShape(QtGui.QFrame.HLine)
    self.line_10.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_10.setObjectName(_fromUtf8("line_10"))
    self.gridLayout.addWidget(self.line_10, 9, 0, 1, 2)
    
    
    
    # ------------------------------------------------------------------
    # Open Access Token File
    self.l_access_token_path = QtGui.QLabel(self.w_security)
    self.l_access_token_path.setObjectName(_fromUtf8("l_access_token_path"))
    self.gridLayout.addWidget(self.l_access_token_path, 10, 0, 2, 1)
    self.w_open_file = QtGui.QWidget(self.w_security)
    self.w_open_file.setMinimumSize(QtCore.QSize(0, 40))
    self.w_open_file.setObjectName(_fromUtf8("w_open_file"))
    self.horizontalLayout_2 = QtGui.QHBoxLayout(self.w_open_file)
    self.horizontalLayout_2.setMargin(0)
    self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
    self.le_access_token_file_path = QtGui.QLineEdit(self.w_open_file)
    self.le_access_token_file_path.setObjectName(_fromUtf8("le_access_token_file_path"))
    self.horizontalLayout_2.addWidget(self.le_access_token_file_path)
    self.pb_open_file_dialog = QtGui.QPushButton(self.w_open_file)
    self.pb_open_file_dialog.setText(_fromUtf8(""))
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/open_folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.pb_open_file_dialog.setIcon(icon)
    self.pb_open_file_dialog.setIconSize(QtCore.QSize(19, 19))
    self.pb_open_file_dialog.setShortcut(_fromUtf8(""))
    self.pb_open_file_dialog.setObjectName(_fromUtf8("pb_open_file_dialog"))
    self.horizontalLayout_2.addWidget(self.pb_open_file_dialog)
    
    self.gridLayout.addWidget(self.w_open_file, 11, 1, 1, 1)
    spacerItem1 = QtGui.QSpacerItem(100, 145, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.gridLayout.addItem(spacerItem1, 12, 0, 1, 2)
    self.tb_preferences.addTab(self.w_security, _fromUtf8(""))
    
    
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Tab Pane - Device
    self.w_device = QtGui.QWidget()
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.w_security.sizePolicy().hasHeightForWidth())
    self.w_device.setSizePolicy(sizePolicy)
    self.w_device.setObjectName(_fromUtf8("w_device"))
    self.gridLayout = QtGui.QGridLayout(self.w_device)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    
    # ------------------------------------------------------------------
    self.l_device_port = QtGui.QLabel(self.w_device)
    self.l_device_port.setObjectName(_fromUtf8("l_device_port"))
    self.gridLayout.addWidget(self.l_device_port, 0, 0, 1, 1)
    self.le_device_port = QtGui.QLineEdit(self.w_device)
    self.le_device_port.setObjectName(_fromUtf8("le_device_port"))
    self.gridLayout.addWidget(self.le_device_port, 0, 1, 1, 1)
    
    # Separator
    self.line_11 = QtGui.QFrame(self.w_device)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_11.sizePolicy().hasHeightForWidth())
    self.line_11.setSizePolicy(sizePolicy)
    self.line_11.setFrameShape(QtGui.QFrame.HLine)
    self.line_11.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_11.setObjectName(_fromUtf8("line_11"))
    self.gridLayout.addWidget(self.line_11, 1, 0, 1, 2)
    
    # ------------------------------------------------------------------
    self.l_baudrate = QtGui.QLabel(self.w_device)
    self.l_baudrate.setObjectName(_fromUtf8("l_baudrate"))
    self.gridLayout.addWidget(self.l_baudrate, 2, 0, 1, 1)
    self.le_baudrate = QtGui.QLineEdit(self.w_device)
    self.le_baudrate.setEchoMode(QtGui.QLineEdit.Normal)
    self.le_baudrate.setObjectName(_fromUtf8("le_baudrate"))
    self.gridLayout.addWidget(self.le_baudrate, 2, 1, 1, 1)    
    

    # Separator
    self.line_12 = QtGui.QFrame(self.w_device)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_12.sizePolicy().hasHeightForWidth())
    self.line_12.setSizePolicy(sizePolicy)
    self.line_12.setFrameShape(QtGui.QFrame.HLine)
    self.line_12.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_12.setObjectName(_fromUtf8("line_12"))
    self.gridLayout.addWidget(self.line_12, 3, 0, 1, 2)



    # ------------------------------------------------------------------
    self.l_auto_open_device = QtGui.QLabel(self.w_device)
    self.l_auto_open_device.setObjectName(_fromUtf8("l_autoOpenDevice"))
    self.gridLayout.addWidget(self.l_auto_open_device, 4, 0, 1, 1)
    self.cb_auto_open_device = QtGui.QCheckBox(self.w_device)
    self.cb_auto_open_device.setLayoutDirection(QtCore.Qt.LeftToRight)
    self.gridLayout.addWidget(self.cb_auto_open_device, 4, 1, 1, 1)
    
    
    
    spacerItem1 = QtGui.QSpacerItem(100, 145, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.gridLayout.addItem(spacerItem1, 12, 0, 1, 2)    
    self.tb_preferences.addTab(self.w_device, _fromUtf8(""))
    self.verticalLayout.addWidget(self.tb_preferences)
    
    
    
    # ------------------------------------------------------------------
    # Menu
    self.f_menu = QtGui.QFrame(Preferences)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.f_menu.sizePolicy().hasHeightForWidth())
    self.f_menu.setSizePolicy(sizePolicy)
    self.f_menu.setMinimumSize(QtCore.QSize(100, 40))
    self.f_menu.setMaximumSize(QtCore.QSize(16777215, 40))
    self.f_menu.setFrameShape(QtGui.QFrame.StyledPanel)
    self.f_menu.setFrameShadow(QtGui.QFrame.Raised)
    self.f_menu.setObjectName(_fromUtf8("f_menu"))
    
    # Layout
    self.horizontalLayout = QtGui.QHBoxLayout(self.f_menu)
    self.horizontalLayout.setSpacing(5)
    self.horizontalLayout.setMargin(5)
    self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
    
    # Menu Spacer - Left
    spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout.addItem(spacerItem2)
    
    # Button Save
    self.pb_save = QtGui.QPushButton(self.f_menu)
    self.pb_save.setMinimumSize(QtCore.QSize(0, 30))
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.pb_save.setIcon(icon)
    self.pb_save.setIconSize(QtCore.QSize(18, 18))
    self.pb_save.setObjectName(_fromUtf8("pb_save"))
    self.horizontalLayout.addWidget(self.pb_save)
    
    # Button Undo
    self.pb_reset = QtGui.QPushButton(self.f_menu)
    self.pb_reset.setMinimumSize(QtCore.QSize(0, 30))
    icon1 = QtGui.QIcon()
    icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/undo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.pb_reset.setIcon(icon1)
    self.pb_reset.setIconSize(QtCore.QSize(18, 18))
    self.pb_reset.setObjectName(_fromUtf8("pb_reset"))
    self.horizontalLayout.addWidget(self.pb_reset)
    
    # Menu Spacer - Right 
    spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout.addItem(spacerItem3)
    
    self.verticalLayout.addWidget(self.f_menu)
    self.retranslateUi(Preferences)
    self.tb_preferences.setCurrentIndex(0) 
    
    
    # TODO remove this
    self.le_access_token_file_path.setText("/home/andre/.fresh.token") 
    
    
    QtCore.QMetaObject.connectSlotsByName(Preferences)
    
    # ------------------------------------------------------------------
    # Connects
    

    
    
    
    


  # --------------------------------------------------------------------------
  def retranslateUi(self, Preferences):
    ''' '''
    Preferences.setWindowTitle(_translate("Preferences", "Preferences", None))
    self.l_keystone_url.setText(_translate("Preferences", "KeyStone URL", None))
    self.l_keystone_ip.setText(_translate("Preferences", "KeyStone IP", None))
    self.l_keystone_port.setText(_translate("Preferences", "KeyStone Port", None))
    self.l_orion_ip.setText(_translate("Preferences", "Orion IP", None))
    self.l_orion_port.setText(_translate("Preferences", "Orion Port", None))
    self.tb_preferences.setTabText(self.tb_preferences.indexOf(self.w_network), _translate("Preferences", "Network", None))
    self.l_username.setText(_translate("Preferences", "Username", None))
    self.l_password.setText(_translate("Preferences", "Password", None))
    self.l_tennant_name.setText(_translate("Preferences", "Tenant Name", None))
    self.l_tennant_id.setText(_translate("Preferences", "Tenant ID", None))
    self.l_domain.setText(_translate("Preferences", "Domain", None))
    self.l_access_token_path.setText(_translate("Preferences", "Access Token Path", None))
    self.tb_preferences.setTabText(self.tb_preferences.indexOf(self.w_security), _translate("Preferences", "Security", None))
    self.pb_save.setText(_translate("Preferences", "Save", None))
    self.pb_reset.setText(_translate("Preferences", "Reset", None))
    self.l_username.setText(_translate("Preferences", "Username", None))
    self.tb_preferences.setTabText(self.tb_preferences.indexOf(self.w_device), _translate("Preferences", "Device", None))
    self.l_device_port.setText(_translate("Preferences", "Device Port", None))
    self.l_baudrate.setText(_translate("Preferences", "Device Baudrate", None))
    self.l_auto_connect.setText(_translate("Preferences", "Auto Connect to Server", None))
    self.l_auto_open_device.setText(_translate("Preferences", "Auto Open Device", None))
  
  
  # --------------------------------------------------------------------------
  def getToken(self):
    return str(self.auth_token) # this cast is needed since the token is a json object = dict

  
  # --------------------------------------------------------------------------
  # Slots
  
  # --------------------------------------------------------------------------
  def openAccessTokenFile(self):
    ''' '''
    try:
      fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home', "Access Token (*.token);; All Files (*)")
      if fname :       
        self.le_access_token_file_path.setText(fname)
        
    except:
      print "Error", sys.exc_info()[0] # DEBUG
      #raise
  
  
  @pyqtSlot()
  def loadPreferences(self):
    ''' '''
    reply = QtGui.QMessageBox.question(self, 'Message',
    "Are you sure you want to load old preferences?", QtGui.QMessageBox.No | 
    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

    if reply == QtGui.QMessageBox.Yes:
      self.loadPreferencesFromFile.emit()
    else:
      pass    
  
    
  @pyqtSlot()
  def savePreferences(self):
    ''' '''
    reply = QtGui.QMessageBox.question(self, 'Message',
    "Are you sure you want to save the preferences?", QtGui.QMessageBox.No | 
    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

    if reply == QtGui.QMessageBox.Yes:
      self.savePreferencesToFile.emit()
    else:
      pass
    



class Ui_PreferencesHelper(QtCore.QObject):
  ''' '''
  def __init__(self, parent = None):
    ''' '''
    super(Ui_PreferencesHelper, self).__init__()
    self.parentWidget = parent
    self.o_log = logging.getLogger('orion')
    self.cfg_loded = False
    self.token_loded = False
    self.token_file = self.parentWidget.le_access_token_file_path.text()
    self.cfg_file = ".fresh.cfg" # .fresh.cfg is the default file
    self.cfg_file_backup = ".fresh.cfg.bak"
    
    
    self.connect(self.parentWidget, QtCore.SIGNAL("savePreferencesToFile()"), self.savePreferencesToFile)
    self.connect(self.parentWidget, QtCore.SIGNAL("loadPreferencesFromFile()"), self.loadPreferencesFromBackup)
    
    try:
      # Load config file
      mode = 'r' if os.path.exists(self.cfg_file) else'w'
      with open(self.cfg_file, mode) as cfg_content:
        cfg = yaml.load(cfg_content)
        if not cfg:        
          self.o_log.error('Configuration file is empty!')
        else:
          self.parentWidget.le_orion_ip.setText(cfg['orion_ip'])
          self.parentWidget.le_orion_port.setText(cfg['orion_port'])
          self.parentWidget.le_username.setText(cfg['username'])
          self.parentWidget.le_password.setText(cfg['password'])
          self.parentWidget.le_keystone_ip.setText(cfg['keystone_ip'])
          self.parentWidget.le_keystone_port.setText(cfg['keystone_port'])
          self.parentWidget.le_keystone_url.setText(cfg['keystone_url'])
          self.parentWidget.le_tenant_id.setText(cfg['tenant_name'])
          self.parentWidget.le_tenant_name.setText(cfg['tenant_id'])
          self.parentWidget.le_domain.setText(cfg['domain'])
          self.parentWidget.le_device_port.setText(cfg['device_port'])
          self.parentWidget.le_baudrate.setText(cfg['device_baudrate'])
          self.parentWidget.cb_auto_connect.setChecked((cfg['auto_connect']) in ['true', 'TRUE', '1', 't', 'y', 'yes'])
          self.parentWidget.cb_auto_open_device.setChecked((cfg['auto_open_device']) in ['true', 'TRUE', '1', 't', 'y', 'yes'])     
          
          self.cfg_loded = True

      # -------------------------------------------------------
      
      # Load token if exists already
      mode = 'r' if os.path.exists(self.token_file) else 'w'
      with open(self.token_file, mode) as token_content:
          content = token_content.read()
          if not content:
            self.o_log.error('Token file is empty!')
            self.parentWidget.auth_token = None
            self.parentWidget.token_loded = False;
            self.token_loded = False
          else:
            self.auth_ref = json.loads(content)
            self.parentWidget.auth_token = self.auth_ref 
            self.o_log.info('Token was loded with success')
            self.parentWidget.token_loded = True 
            self.token_loded = True  
      
      # -------------------------------------------------------
  
    except IOError as e:
      print 'I/O error({0}): {1}'.format(e.errno, e.strerror)
    except KeyError as e:
      print 'The configuration file is missing the {0} field.'.format(str(e))
    except IndexError as e:
      print 'Error {0}'.format(str(e))
    except: # catch *all* exceptions
      e = sys.exc_info()[0]
      print e
      #raise
    
  # --------------------------------------------------------------------------
  # Slots
  @pyqtSlot()
  def savePreferencesToFile(self):
    ''' '''
    
    try:
      shutil.copy(self.cfg_file, self.cfg_file_backup)
      self.cfg = None
      with open(self.cfg_file, 'r') as cfg_content:
        self.cfg = yaml.load(cfg_content)
        if not self.cfg:        
          self.o_log.error('Problems with the file!')
        else:
          self.cfg['orion_ip'] = str(self.parentWidget.le_orion_ip.text())
          self.cfg['orion_port'] = str(self.parentWidget.le_orion_port.text())
          self.cfg['username'] = str(self.parentWidget.le_username.text())
          self.cfg['password'] = str(self.parentWidget.le_password.text())
          self.cfg['keystone_ip'] = str(self.parentWidget.le_keystone_ip.text())
          self.cfg['keystone_port'] = str(self.parentWidget.le_keystone_port.text())
          self.cfg['keystone_url'] = str(self.parentWidget.le_keystone_url.text())
          self.cfg['tenant_name'] = str(self.parentWidget.le_tenant_name.text())
          self.cfg['tenant_id'] = str(self.parentWidget.le_tenant_id.text())
          self.cfg['domain'] = str(self.parentWidget.le_domain.text())
          self.cfg['device_port'] = str(self.parentWidget.le_device_port.text())
          self.cfg['device_baudrate'] = str(self.parentWidget.le_baudrate.text())
          self.cfg['auto_connect'] = self.parentWidget.cb_auto_connect.isChecked()
          self.cfg['auto_open_device'] = self.parentWidget.cb_auto_open_device.isChecked()
            
        with open(self.cfg_file, 'w') as cfg_content:
          yaml.safe_dump(self.cfg, cfg_content, default_flow_style=False, allow_unicode=True)
    except IOError as e:
      print "Error {0}".format(e.strerror) # DEBUG
    except e:
      print "Erro {0}".format(str(e)) # Just in case
      #raise
     
  @pyqtSlot()
  def loadPreferencesFromBackup(self):
    ''' '''
    
    try:
      # Load config file
      mode = 'r' if os.path.exists(self.token_file) else 'w'
      with open(self.cfg_file_backup, mode) as cfg_content:
        cfg = yaml.load(cfg_content)
        if not cfg:        
          self.o_log.error('Backup Configuration file is empty!')
        else:
          self.parentWidget.le_orion_ip.setText(cfg['orion_ip'])
          self.parentWidget.le_orion_port.setText(cfg['orion_port'])
          self.parentWidget.le_username.setText(cfg['username'])
          self.parentWidget.le_password.setText(cfg['password'])
          self.parentWidget.le_keystone_ip.setText(cfg['keystone_ip'])
          self.parentWidget.le_keystone_port.setText(cfg['keystone_port'])
          self.parentWidget.le_keystone_url.setText(cfg['keystone_url'])
          self.parentWidget.le_tenant_id.setText(cfg['tenant_name'])
          self.parentWidget.le_tenant_name.setText(cfg['tenant_id'])
          self.parentWidget.le_domain.setText(cfg['domain'])
          self.parentWidget.le_device_port.setText(cfg['device_port'])
          self.parentWidget.le_baudrate.setText(cfg['device_baudrate'])
          self.parentWidget.cb_auto_connect.setChecked(cfg['auto_connect'])
          self.parentWidget.cb_auto_open_device.setChecked(cfg['auto_open_device'])
          
          self.cfg_loded = True
    
    except IOError as e:
      print "Error {0}".format(e.strerror) # DEBUG
      
    except e:
      print "Erro {0}".format(str(e)) # Just in case
      #raise
     

#EOF