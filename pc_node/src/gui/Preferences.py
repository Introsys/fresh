#!/usr/bin/python

# Form implementation generated from reading ui file 'Preferences.ui'
#
# Created: Thu Aug 20 15:29:04 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

import sys
import logging
from PyQt4 import QtCore, QtGui
from gui import Resources_rc
from PyQt4.Qt import pyqtSlot, pyqtSignal 
from PyQt4.Qt import QRegExp, QRegExpValidator




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



class Ui_Preferences(QtGui.QWidget):
  ''' '''
  # --------------------------------------------------------------------------
  # SIGNALS
  # --------------------------------------------------------------------------
  
  savePreferences = QtCore.pyqtSignal(object, name="savePreferences") 
  loadOldPreferences = pyqtSignal(name="loadOldPreferences")
  loadDefaultPreferences = QtCore.pyqtSignal(name="loadDefaultPreferences")
  
       
  
  def __init__(self, parent = None):
    super(Ui_Preferences, self).__init__()
    self.f_log = logging.getLogger('App') # this can be called in any place
    self.setupUi(self)
    self._parentWidget = parent
    self.token_loded = False
    
    # Connect the Slots to the events of the GUI
    QtCore.QObject.connect(self.pb_token_file_path_dialog, QtCore.SIGNAL('clicked()'), self.openAccessTokenFile)
    QtCore.QObject.connect(self.pb_save, QtCore.SIGNAL('clicked()'), self.askToSavePreferences)
    QtCore.QObject.connect(self.pb_reset, QtCore.SIGNAL('clicked()'), self.askToLoadPreviousPreferences)
    QtCore.QObject.connect(self.pb_default, QtCore.SIGNAL('clicked()'), self.askToLoadDefaultPreferences)
       
  # --------------------------------------------------------------------------
  
  
  def setupUi(self, Preferences):
    Resources_rc.qInitResources()
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
    self.line_13 = QtGui.QFrame(self.w_network)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_13.sizePolicy().hasHeightForWidth())
    self.line_13.setSizePolicy(sizePolicy)
    self.line_13.setFrameShape(QtGui.QFrame.HLine)
    self.line_13.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_13.setObjectName(_fromUtf8("line_13"))
    self.gridLayout_2.addWidget(self.line_13, 9, 0, 1, 2)
    
    # ------------------------------------------------------------------
    self.l_cosmos_url = QtGui.QLabel(self.w_network)
    self.l_cosmos_url.setObjectName(_fromUtf8("l_cosmos_url"))
    self.gridLayout_2.addWidget(self.l_cosmos_url, 10, 0, 1, 1)
    self.le_cosmos_url = QtGui.QLineEdit(self.w_network)
    self.le_cosmos_url.setObjectName(_fromUtf8("le_cosmos_url"))
    self.gridLayout_2.addWidget(self.le_cosmos_url, 10, 1, 1, 1)

    # Separator
    self.line_14 = QtGui.QFrame(self.w_network)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_14.sizePolicy().hasHeightForWidth())
    self.line_14.setSizePolicy(sizePolicy)
    self.line_14.setFrameShape(QtGui.QFrame.HLine)
    self.line_14.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_14.setObjectName(_fromUtf8("line_14"))
    self.gridLayout_2.addWidget(self.line_14, 11, 0, 1, 2)
    
    # ------------------------------------------------------------------
    self.l_cosmos_auth_port = QtGui.QLabel(self.w_network)
    self.l_cosmos_auth_port.setObjectName(_fromUtf8("l_cosmos_auth_port"))
    self.gridLayout_2.addWidget(self.l_cosmos_auth_port, 12, 0, 1, 1)
    self.le_cosmos_auth_port = QtGui.QLineEdit(self.w_network)
    self.le_cosmos_auth_port.setObjectName(_fromUtf8("le_cosmos_auth_port"))
    self.gridLayout_2.addWidget(self.le_cosmos_auth_port, 12, 1, 1, 1)

    # Separator
    self.line_15 = QtGui.QFrame(self.w_network)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_15.sizePolicy().hasHeightForWidth())
    self.line_15.setSizePolicy(sizePolicy)
    self.line_15.setFrameShape(QtGui.QFrame.HLine)
    self.line_15.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_15.setObjectName(_fromUtf8("line_15"))
    self.gridLayout_2.addWidget(self.line_15, 13, 0, 1, 2)
    
    # ------------------------------------------------------------------
    self.l_cosmos_webhdfs_port = QtGui.QLabel(self.w_network)
    self.l_cosmos_webhdfs_port.setObjectName(_fromUtf8("l_cosmos_webhdfs_port"))
    self.gridLayout_2.addWidget(self.l_cosmos_webhdfs_port, 14, 0, 1, 1)
    self.le_cosmos_webhdfs_port = QtGui.QLineEdit(self.w_network)
    self.le_cosmos_webhdfs_port.setObjectName(_fromUtf8("le_cosmos_webhdfs_port"))
    self.gridLayout_2.addWidget(self.le_cosmos_webhdfs_port, 14, 1, 1, 1)
    
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
    self.gridLayout_2.addWidget(self.line_05, 15, 0, 1, 2)
    
    # ------------------------------------------------------------------
    self.l_auto_connect = QtGui.QLabel(self.w_network)
    self.l_auto_connect.setObjectName(_fromUtf8("l_auto_connect"))
    self.gridLayout_2.addWidget(self.l_auto_connect, 16, 0, 1, 1)
    self.cb_auto_connect = QtGui.QCheckBox(self.w_network)
    self.cb_auto_connect.setObjectName(_fromUtf8("cb_auto_connect"))  
    self.gridLayout_2.addWidget(self.cb_auto_connect, 16, 1, 1, 1)
    
    # Spacer
    spacerItem = QtGui.QSpacerItem(620, 233, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.gridLayout_2.addItem(spacerItem, 17, 0, 1, 2)
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
    self.line_16 = QtGui.QFrame(self.w_security)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_16.sizePolicy().hasHeightForWidth())
    self.line_16.setSizePolicy(sizePolicy)
    self.line_16.setFrameShape(QtGui.QFrame.HLine)
    self.line_16.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_16.setObjectName(_fromUtf8("line_16"))
    self.gridLayout.addWidget(self.line_16, 7, 0, 1, 2)
    
    # ------------------------------------------------------------------
    self.l_cosmos_user = QtGui.QLabel(self.w_security)
    self.l_cosmos_user.setObjectName(_fromUtf8("l_cosmos_user"))
    self.gridLayout.addWidget(self.l_cosmos_user, 8, 0, 1, 1)
    self.le_cosmos_user = QtGui.QLineEdit(self.w_security)
    self.le_cosmos_user.setObjectName(_fromUtf8("le_cosmos_user"))
    self.gridLayout.addWidget(self.le_cosmos_user, 8, 1, 1, 1)
    
    
    
    
    
    
    
    
    
    
    
    
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
    self.gridLayout.addWidget(self.line_09, 9, 0, 1, 2)
    
    # ------------------------------------------------------------------
    self.l_domain = QtGui.QLabel(self.w_security)
    self.l_domain.setObjectName(_fromUtf8("l_domain"))
    self.gridLayout.addWidget(self.l_domain, 10, 0, 1, 1)
    self.le_domain = QtGui.QLineEdit(self.w_security)
    self.le_domain.setObjectName(_fromUtf8("le_domain"))
    self.gridLayout.addWidget(self.le_domain, 10, 1, 1, 1)
        
    
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
    self.gridLayout.addWidget(self.line_10, 11, 0, 1, 2)
    
    # ------------------------------------------------------------------
    # Open Access Token File
    self.l_access_token_path = QtGui.QLabel(self.w_security)
    self.l_access_token_path.setObjectName(_fromUtf8("l_access_token_path"))
    self.gridLayout.addWidget(self.l_access_token_path, 12, 0, 2, 1)
    self.w_open_file = QtGui.QWidget(self.w_security)
    self.w_open_file.setMinimumSize(QtCore.QSize(0, 40))
    self.w_open_file.setObjectName(_fromUtf8("w_open_file"))
    self.horizontalLayout_2 = QtGui.QHBoxLayout(self.w_open_file)
    self.horizontalLayout_2.setMargin(0)
    self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
    self.le_access_token_file_path = QtGui.QLineEdit(self.w_open_file)
    self.le_access_token_file_path.setObjectName(_fromUtf8("le_access_token_file_path"))
    self.horizontalLayout_2.addWidget(self.le_access_token_file_path)
    self.pb_token_file_path_dialog = QtGui.QPushButton(self.w_open_file)
    self.pb_token_file_path_dialog.setText(_fromUtf8(""))
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/open_folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.pb_token_file_path_dialog.setIcon(icon)
    self.pb_token_file_path_dialog.setIconSize(QtCore.QSize(19, 19))
    self.pb_token_file_path_dialog.setShortcut(_fromUtf8(""))
    self.pb_token_file_path_dialog.setObjectName(_fromUtf8("pb_token_file_path_dialog"))
    self.horizontalLayout_2.addWidget(self.pb_token_file_path_dialog)
    self.gridLayout.addWidget(self.w_open_file, 13, 1, 1, 1)
    
    spacerItem1 = QtGui.QSpacerItem(100, 145, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.gridLayout.addItem(spacerItem1, 14, 0, 1, 2)
    self.tb_preferences.addTab(self.w_security, _fromUtf8(""))
    
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    
    # Tab Pane - Device
    self.w_device = QtGui.QWidget()
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.w_device.sizePolicy().hasHeightForWidth())
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
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    
    # Tab Pane - Report
    self.w_report = QtGui.QWidget()
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.w_report.sizePolicy().hasHeightForWidth())
    self.w_report.setSizePolicy(sizePolicy)
    
    self.w_report.setObjectName(_fromUtf8("w_report"))
    self.gridLayout = QtGui.QGridLayout(self.w_report)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    
    # ------------------------------------------------------------------
    self.l_default_expert_name = QtGui.QLabel(self.w_report)
    self.l_default_expert_name.setObjectName(_fromUtf8("l_default_expert_name"))
    self.gridLayout.addWidget(self.l_default_expert_name, 0, 0, 1, 1)
    self.le_default_expert_name = QtGui.QLineEdit(self.w_report)
    self.le_default_expert_name.setObjectName(_fromUtf8("le_default_expert_name"))
    self.gridLayout.addWidget(self.le_default_expert_name, 0, 1, 1, 1)
    
    # Separator
    self.line_40 = QtGui.QFrame(self.w_report)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_40.sizePolicy().hasHeightForWidth())
    self.line_40.setSizePolicy(sizePolicy)
    self.line_40.setFrameShape(QtGui.QFrame.HLine)
    self.line_40.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_40.setObjectName(_fromUtf8("line_40"))
    self.gridLayout.addWidget(self.line_40, 1, 0, 1, 2)
    
    # ------------------------------------------------------------------
    self.l_default_expert_email = QtGui.QLabel(self.w_report)
    self.l_default_expert_email.setObjectName(_fromUtf8("l_default_expert_email"))
    self.gridLayout.addWidget(self.l_default_expert_email, 2, 0, 1, 1)
    self.le_default_expert_email = QtGui.QLineEdit(self.w_report)
    self.le_default_expert_email.setEchoMode(QtGui.QLineEdit.Normal)
    self.le_default_expert_email.setObjectName(_fromUtf8("le_default_expert_email"))
    self.gridLayout.addWidget(self.le_default_expert_email, 2, 1, 1, 1)    
    

    # Separator
    self.line_41 = QtGui.QFrame(self.w_report)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_41.sizePolicy().hasHeightForWidth())
    self.line_41.setSizePolicy(sizePolicy)
    self.line_41.setFrameShape(QtGui.QFrame.HLine)
    self.line_41.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_41.setObjectName(_fromUtf8("line_41"))
    self.gridLayout.addWidget(self.line_41, 3, 0, 1, 2)



    # ------------------------------------------------------------------
    self.l_default_expert_address = QtGui.QLabel(self.w_report)
    self.l_default_expert_address.setObjectName(_fromUtf8("l_default_expert_address"))
    self.gridLayout.addWidget(self.l_default_expert_address, 4, 0, 1, 1)
    self.te_default_expert_address = QtGui.QTextEdit(self.w_report)
    self.te_default_expert_address.setObjectName(_fromUtf8("te_default_expert_address"))
    self.gridLayout.addWidget(self.te_default_expert_address, 4, 1, 1, 1)    
    
    
    # Separator
    self.line_42 = QtGui.QFrame(self.w_report)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_42.sizePolicy().hasHeightForWidth())
    self.line_42.setSizePolicy(sizePolicy)
    self.line_42.setFrameShape(QtGui.QFrame.HLine)
    self.line_42.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_42.setObjectName(_fromUtf8("line_42"))
    self.gridLayout.addWidget(self.line_42, 5, 0, 1, 2)

    
    
    
    # ------------------------------------------------------------------
    # Open Access Token File
    self.l_report_template_path = QtGui.QLabel(self.w_report)
    self.l_report_template_path.setObjectName(_fromUtf8("l_report_template_path"))
    self.gridLayout.addWidget(self.l_report_template_path, 6, 0, 2, 1)
    self.w_open_report_file = QtGui.QWidget(self.w_report)
    self.w_open_report_file.setMinimumSize(QtCore.QSize(0, 40))
    self.w_open_report_file.setObjectName(_fromUtf8("w_open_report_file"))
    self.horizontalLayout_2 = QtGui.QHBoxLayout(self.w_open_report_file)
    self.horizontalLayout_2.setMargin(0)
    self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
    self.le_report_file_path = QtGui.QLineEdit(self.w_open_report_file)
    self.le_report_file_path.setObjectName(_fromUtf8("le_report_file_path"))
    self.horizontalLayout_2.addWidget(self.le_report_file_path)
    
    self.pb_template_file_path_dialog = QtGui.QPushButton(self.w_open_report_file)
    self.pb_template_file_path_dialog.setText(_fromUtf8(""))
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/open_folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.pb_template_file_path_dialog.setIcon(icon)
    self.pb_template_file_path_dialog.setIconSize(QtCore.QSize(19, 19))
    self.pb_template_file_path_dialog.setShortcut(_fromUtf8(""))
    self.pb_template_file_path_dialog.setObjectName(_fromUtf8("pb_template_file_path_dialog"))
    self.horizontalLayout_2.addWidget(self.pb_template_file_path_dialog)
    self.gridLayout.addWidget(self.w_open_report_file, 6, 1, 1, 1)
    
    # Separator
    self.line_43 = QtGui.QFrame(self.w_report)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line_43.sizePolicy().hasHeightForWidth())
    self.line_43.setSizePolicy(sizePolicy)
    self.line_43.setFrameShape(QtGui.QFrame.HLine)
    self.line_43.setFrameShadow(QtGui.QFrame.Sunken)
    self.line_43.setObjectName(_fromUtf8("line_43"))
    self.gridLayout.addWidget(self.line_43, 7, 0, 1, 2)
    
    
    
    spacerItem1 = QtGui.QSpacerItem(100, 145, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.gridLayout.addItem(spacerItem1, 12, 0, 1, 2)    
    self.tb_preferences.addTab(self.w_report, _fromUtf8(""))
    
    
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
    iconS = QtGui.QIcon()
    iconS.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.pb_save.setIcon(iconS)
    self.pb_save.setIconSize(QtCore.QSize(18, 18))
    self.pb_save.setObjectName(_fromUtf8("pb_save"))
    self.horizontalLayout.addWidget(self.pb_save)
    
    # Button Undo
    self.pb_reset = QtGui.QPushButton(self.f_menu)
    self.pb_reset.setMinimumSize(QtCore.QSize(0, 30))
    iconU = QtGui.QIcon()
    iconU.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/undo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.pb_reset.setIcon(iconU)
    self.pb_reset.setIconSize(QtCore.QSize(18, 18))
    self.pb_reset.setObjectName(_fromUtf8("pb_reset"))
    self.horizontalLayout.addWidget(self.pb_reset)
    
    # Button Default
    self.pb_default = QtGui.QPushButton(self.f_menu)
    self.pb_default.setMinimumSize(QtCore.QSize(0, 30))
    iconD = QtGui.QIcon()
    iconD.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/default.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.pb_default.setIcon(iconD)
    self.pb_default.setIconSize(QtCore.QSize(18, 18))
    self.pb_default.setObjectName(_fromUtf8("pb_default"))
    self.horizontalLayout.addWidget(self.pb_default)
    
    # Menu Spacer - Right 
    spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout.addItem(spacerItem3)
    
    self.verticalLayout.addWidget(self.f_menu)
    self.retranslateUi(Preferences)
    self.tb_preferences.setCurrentIndex(0) 
    
    
    
    QtCore.QMetaObject.connectSlotsByName(Preferences)
  # --------------------------------------------------------------------------
  
  
  def retranslateUi(self, Preferences):
    ''' '''
    Preferences.setWindowTitle(_translate("Preferences", "Preferences", None))
    self.l_keystone_url.setText(_translate("Preferences", "KeyStone URL", None))
    self.l_keystone_ip.setText(_translate("Preferences", "KeyStone IP", None))
    self.l_keystone_port.setText(_translate("Preferences", "KeyStone Port", None))
    self.l_orion_ip.setText(_translate("Preferences", "Orion IP", None))
    self.l_orion_port.setText(_translate("Preferences", "Orion Port", None))
    self.l_cosmos_url.setText(_translate("Preferences", "Cosmos IP", None))
    self.l_cosmos_auth_port.setText(_translate("Preferences", "Cosmos Auth port", None))
    self.l_cosmos_webhdfs_port.setText(_translate("Preferences", "Cosmos Web HDFS port", None))
    self.tb_preferences.setTabText(self.tb_preferences.indexOf(self.w_network), _translate("Preferences", "Network", None))
    self.l_username.setText(_translate("Preferences", "Username", None))
    self.l_password.setText(_translate("Preferences", "Password", None))
    self.l_tennant_name.setText(_translate("Preferences", "Tenant Name", None))
    self.l_tennant_id.setText(_translate("Preferences", "Tenant ID", None))
    self.l_cosmos_user.setText(_translate("Preferences", "Cosmos User", None))
    self.l_domain.setText(_translate("Preferences", "Domain", None))
    self.l_access_token_path.setText(_translate("Preferences", "Access Token Path", None))
    self.tb_preferences.setTabText(self.tb_preferences.indexOf(self.w_security), _translate("Preferences", "Security", None))
    self.pb_save.setText(_translate("Preferences", "Save", None))
    self.pb_reset.setText(_translate("Preferences", "Reset", None))
    self.pb_default.setText(_translate("Preferences", "Default", None))
    self.l_username.setText(_translate("Preferences", "Username", None))
    self.tb_preferences.setTabText(self.tb_preferences.indexOf(self.w_device), _translate("Preferences", "Device", None))
    self.l_device_port.setText(_translate("Preferences", "Device Port", None))
    self.l_baudrate.setText(_translate("Preferences", "Device Baudrate", None))
    self.l_auto_connect.setText(_translate("Preferences", "Auto Connect to Server", None))
    self.l_auto_open_device.setText(_translate("Preferences", "Auto Open Device", None))
    self.tb_preferences.setTabText(self.tb_preferences.indexOf(self.w_report), _translate("Preferences", "Reports", None))
    self.l_default_expert_address.setText(_translate("Preferences", "Expert Default Address", None))
    self.l_default_expert_email.setText(_translate("Preferences", "Expert Default Email", None))
    self.l_default_expert_name.setText(_translate("Preferences", "Expert Default Name", None))
    self.l_report_template_path.setText(_translate("Preferences", "Report Template Path", None))
    
  # --------------------------------------------------------------------------
  


  # --------------------------------------------------------------------------
  # Slots
  # --------------------------------------------------------------------------
  
  
  @pyqtSlot()  
  def openAccessTokenFile(self):
    ''' '''
    try:
      fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home', "Access Token (*.token);; All Files (*)")
      if fname :       
        self.le_access_token_file_path.setText(fname)
        
    except:
      print "Error", sys.exc_info()[0] # DEBUG
      raise
  # --------------------------------------------------------------------------
  
  
  @pyqtSlot(name="askToSavePref")
  def askToSavePreferences(self):
    ''' '''
    reply = QtGui.QMessageBox.question(self, 'Message',
    "Are you sure you want to save the preferences?", QtGui.QMessageBox.No | 
    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

    if reply == QtGui.QMessageBox.Yes:
      preferences = PreferecesDict(self.le_orion_ip.text(), 
                                   self.le_orion_port.text(), 
                                   self.le_username.text(), 
                                   self.le_password.text(), 
                                   self.le_keystone_ip.text(), 
                                   self.le_keystone_port.text(), 
                                   self.le_keystone_url.text(), 
                                   self.le_tenant_id.text(), 
                                   self.le_tenant_name.text(), 
                                   self.le_domain.text(), 
                                   self.le_device_port.text(), 
                                   self.le_baudrate.text(),
                                   self.le_access_token_file_path.text())
      self.savePreferences.emit(preferences)
  # --------------------------------------------------------------------------
  
  
  @pyqtSlot(name="askToLoadPreviousPreferences")
  def askToLoadPreviousPreferences(self):
    ''' '''
    reply = QtGui.QMessageBox.question(self, 'Message',
    "Are you sure you want to load old preferences?", QtGui.QMessageBox.No | 
    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

    if reply == QtGui.QMessageBox.Yes:
      self.loadOldPreferences.emit()    
  # --------------------------------------------------------------------------    
  
  
  @pyqtSlot(name="askToLoadDefaultPreferences")
  def askToLoadDefaultPreferences(self):
    ''' '''
    reply = QtGui.QMessageBox.question(self, 'Message',
    "Are you sure you want to load the defualt preferences?", QtGui.QMessageBox.No | 
    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

    if reply == QtGui.QMessageBox.Yes:
      self.loadDefaultPreferences.emit()
  # --------------------------------------------------------------------------  
    
      
  @pyqtSlot(object, name="displayChangedPreferences")
  def displayChangedPreferences(self, preferences):
    
    self.le_orion_ip.setText(preferences.orionIp)
    self.le_orion_port.setText(preferences.orionPort)
    self.le_username.setText(preferences.username)
    self.le_password.setText(preferences.password)
    self.le_keystone_ip.setText(preferences.keystoneIp)
    self.le_keystone_port.setText(preferences.keystonePort)
    self.le_keystone_url.setText(preferences.keystoneUrl)
    self.le_tenant_id.setText(preferences.tenantId)
    self.le_tenant_name.setText(preferences.tenantName)
    self.le_domain.setText(preferences.domain)
    self.le_device_port.setText(preferences.devicePort)
    self.le_baudrate.setText(preferences.baudrate)
    self.cb_auto_connect.setChecked(0)
    self.cb_auto_open_device.setChecked(0)    
  # --------------------------------------------------------------------------

    
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------


class PreferecesDict():
  ''' '''
  def __init__(self, orion_ip="", orion_port="", username="", password="", keystone_ip="", keystone_port="",\
                keystone_url="", tenant_id="", tenant_name="", domain="", device_port="", baudrate="",\
                token_path=""):  
    self.orionIp = orion_ip
    self.orionPort = orion_port
    self.username = username
    self.password = password
    self.keystoneIp = keystone_ip
    self.keystonePort = keystone_port
    self.keystoneUrl = keystone_url
    self.tenantId = tenant_id
    self.tenantName = tenant_name
    self.domain = domain
    self.devicePort = device_port
    self.baudrate = baudrate
    self.tokenPath = token_path
  # --------------------------------------------------------------------------
  
# ----------------------------------------------------------------------------------------------
#EOF