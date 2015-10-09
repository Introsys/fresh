#!/usr/bin/python


# Form implementation generated from reading ui file 'untitled.ui'
#
# Created: Tue Aug 18 19:47:53 2015
#      by: PyQt4 UI code generator 4.10.4
#
# Please do not generate this file from the original MainWindow.ui
# or all the changes made to this document will be lost
# The Ui file serves only for making the template UI


# System imports
import sys #@UnusedImport
import time
import Resources_rc
import logging

# Qt imports
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import QWidget, QSizePolicy, pyqtSlot, pyqtSignal #@UnusedImport

# Custom Widgets Imports
from NetworkManagement import Ui_WidgetNetMang
from SplashScreen import Ui_WidgetLogo
from gui.ViewDetails import Ui_WidgetViewDetails
from Preferences import Ui_Preferences
from Report import Ui_WidgetReport
from PyQt4.Qt import QMessageBox
from threading import current_thread



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





# Main Class
class Ui_MainWindow(QtGui.QMainWindow):

  # --------------------------------------------------------------------------
  # Declaration of custom signals for core with the helper class  
  openUSBDevice = QtCore.pyqtSignal(name = 'openUSBDevice')
  closeUSBDevice = QtCore.pyqtSignal(name = 'closeUSBDevice')
  connectToServer = QtCore.pyqtSignal(name = 'connectToServer')
  disconnectFromServer = QtCore.pyqtSignal(name ='disconnectFromServer')
  deviceOpened = QtCore.pyqtSignal(bool, name="deviceOpened")


  # --------------------------------------------------------------------------
  def __init__(self, controler = None):
    super(Ui_MainWindow, self).__init__()
    self.f_log = logging.getLogger('App') # this can be called in any place
    Resources_rc.qInitResources()
    self._controler = controler
    self.setupUi(self)
    self.device_is_open = False
    self.connected_to_server = False
    self.networkWidgetActive = False
    self.reportsWidgetActive = False
    self.viewdetailsWidgetActive = False
    self.preferencesWidgetActive = False
    self.setWindowTitle('Fresh - Greenhouse Data Visualizer')
    
    
    self.statusbar.showMessage("Welcome to the Fresh Greenhouse Management Application",3000)
  
  
  # --------------------------------------------------------------------------
  
  
  def setupUi(self, MainWindow):
    ''' This defines the primary layout of the MainWindow '''
    
    MainWindow.setObjectName(_fromUtf8('MainWindow'))
    MainWindow.resize(800, 600)
    MainWindow.setMinimumSize(QtCore.QSize(400, 400))
    MainWindow.setAnimated(False)
    MainWindow.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks)
    
    
    self.centralWidget = QtGui.QWidget(MainWindow)
    self.centralWidget.setMinimumSize(QtCore.QSize(300, 300))
    self.centralWidget.setObjectName(_fromUtf8('centralWidget'))
    
    
    self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
    self.verticalLayout.setSpacing(0)
    self.verticalLayout.setMargin(0)
    self.verticalLayout.setObjectName(_fromUtf8('verticalLayout'))
    
    # ------------------------------------------------------------------
    #    
    self.splashWidget = Ui_WidgetLogo()
    self.splashWidget.setObjectName(_fromUtf8('splashkWidget'))
    self.verticalLayout.addWidget(self.splashWidget)
    self.splashWidget.setVisible(True)  
         
    # ------------------------------------------------------------------
    #     
    MainWindow.setCentralWidget(self.centralWidget)
    self.toolBar = QtGui.QToolBar(MainWindow)
    self.toolBar.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 0);"))
    self.toolBar.setIconSize(QtCore.QSize(38, 38))
    self.toolBar.setFloatable(False)
    self.toolBar.setObjectName(_fromUtf8("toolBar"))
    MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
    
    # ------------------------------------------------------------------
    # ActionNetwork
    self.actionNetwork = QtGui.QAction(MainWindow)
    self.actionNetwork.setCheckable(True)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/network.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/network_color.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    self.actionNetwork.setIcon(icon)
    self.actionNetwork.setObjectName(_fromUtf8("actionNetwork"))
    
    # ------------------------------------------------------------------
    # ActionReports
    self.actionReports = QtGui.QAction(MainWindow)
    self.actionReports.setCheckable(True)
    icon1 = QtGui.QIcon()
    icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/reports.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/reports_color.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    self.actionReports.setIcon(icon1)
    self.actionReports.setObjectName(_fromUtf8("actionReports"))
    
    # ------------------------------------------------------------------
    # ActionViewDetails
    self.actionViewDetails = QtGui.QAction(MainWindow)
    self.actionViewDetails.setCheckable(True)
    icon2 = QtGui.QIcon()
    icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/details.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/details_color.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    self.actionViewDetails.setIcon(icon2)
    self.actionViewDetails.setObjectName(_fromUtf8("actionViewDetails"))
    
    # ------------------------------------------------------------------
    # ActionPreferences
    self.actionPreferences = QtGui.QAction(MainWindow)
    self.actionPreferences.setCheckable(True)
    icon3 = QtGui.QIcon()
    icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/preferences.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/preferences_color.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    self.actionPreferences.setIcon(icon3)
    self.actionPreferences.setObjectName(_fromUtf8("actionPreferences"))
    
    
    # ------------------------------------------------------------------
    # ActionQuit
    self.actionQuit = QtGui.QAction(MainWindow)
    self.actionQuit.setCheckable(True)
    icon4 = QtGui.QIcon()
    icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/quitapp.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/quitapp_color.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    self.actionQuit.setIcon(icon4)
    self.actionQuit.setIconVisibleInMenu(False)
    self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
    
    # ------------------------------------------------------------------
    # Spacer to align the preferences button on the right of the ToolBar
    spacer = QtGui.QWidget()
    spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    
    # ------------------------------------------------------------------
    # Add action buttons to the toolbar
    self.toolBar.addAction(self.actionNetwork)
    self.toolBar.addAction(self.actionReports)
    self.toolBar.addAction(self.actionViewDetails)
    self.toolBar.addWidget(spacer) # after this the buttons will be placed to the right
    self.toolBar.addAction(self.actionPreferences)
    self.toolBar.addAction(self.actionQuit)
    
    self.retranslateUi(MainWindow)
    QtCore.QMetaObject.connectSlotsByName(MainWindow) # automatically generated 
    
    # ------------------------------------------------------------------
    # Add buttons to the ActionGroup enabling auto-exclude when selection one action button
    self.navigation = QtGui.QActionGroup(self)
    self.navigation.setExclusive(True)
    self.navigation.addAction(self.actionNetwork)
    self.navigation.addAction(self.actionPreferences)
    self.navigation.addAction(self.actionReports)
    self.navigation.addAction(self.actionViewDetails)
    self.navigation.addAction(self.actionQuit)
    
    # ------------------------------------------------------------------
    # Status Bar
    self.statusbar = QtGui.QStatusBar(MainWindow)
    self.statusbar.setObjectName(_fromUtf8("StatusBar"))
    self.statusbar.setStyleSheet("QStatusBar{ padding-top: 5px; padding-right: 30px; padding-bottom: 2px; padding-left: 20px;}")
    self.setStatusBar(self.statusbar)
    
    self.pb_connect = QtGui.QPushButton("Disconnected") # Default  is disconnected
    self.pb_connect.setCheckable(True)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/off.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    #icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/on.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    self.pb_connect.setIcon(icon)
    self.pb_connect.setIconSize(QtCore.QSize(16, 16))
    font = QtGui.QFont()
    font.setPointSize(10)
    self.pb_connect.setFont(font)
    self.pb_connect.setFixedSize(QtCore.QSize(115,23))
    self.statusbar.addPermanentWidget(self.pb_connect, 0)
    self.statusbar.setSizeGripEnabled(False)
    
    self.pb_open_device = QtGui.QPushButton("Closed") # Default is closed
    self.pb_open_device.setCheckable(True)
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/off.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    #icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/on.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    self.pb_open_device.setIcon(icon)
    self.pb_open_device.setIconSize(QtCore.QSize(16, 16))
    font = QtGui.QFont()
    font.setPointSize(10)
    self.pb_open_device.setFont(font)
    self.pb_open_device.setFixedSize(QtCore.QSize(90,23))
    self.statusbar.addPermanentWidget(self.pb_open_device, 0)
    self.statusbar.setSizeGripEnabled(False)
    
    
    # ------------------------------------------------------------------
    # 
    self.networkWidget = Ui_WidgetNetMang(MainWindow)
    self.networkWidget.setObjectName(_fromUtf8("NetworkWidget"))
    self.verticalLayout.addWidget(self.networkWidget)
    self.networkWidget.setVisible(False)
    
    
    ##############MG####################
    self.reportWidget = Ui_WidgetReport(MainWindow)
    self.reportWidget.setObjectName(_fromUtf8("ReportWidget"))
    self.verticalLayout.addWidget(self.reportWidget)
    self.reportWidget.setVisible(False)
    
    # ------------------------------------------------------------------
    #
    self.detailsWidget = Ui_WidgetViewDetails(MainWindow)
    self.detailsWidget.setObjectName(_fromUtf8("DetailsWidget"))
    self.verticalLayout.addWidget(self.detailsWidget)
    self.detailsWidget.setVisible(False)
    
    # ------------------------------------------------------------------
    #
    self.preferencesWidget = Ui_Preferences(MainWindow)
    self.preferencesWidget.setObjectName(_fromUtf8("PreferencesWidget"))
    self.verticalLayout.addWidget(self.preferencesWidget)
    self.preferencesWidget.setVisible(False)
    
    
    # Center the window of the application on the center of the screen
    qr = self.frameGeometry()
    cp = QtGui.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())
    
    # ------------------------------------------------------------------
    # Connects
    self.actionNetwork.triggered.connect(self.showNetworkWidget)
    self.actionReports.triggered.connect(self.showReportsWidget)
    self.actionViewDetails.triggered.connect(self.showViewDetails)
    self.actionPreferences.triggered.connect(self.showPreferencesWidget)
   
    self.pb_connect.toggled.connect(self.connectToServerPressed)
    self.pb_open_device.toggled.connect(self.openDevicePressed)
    
    self.actionQuit.triggered.connect(self.close) # Default behavior to quit the App

  # --------------------------------------------------------------------------
  
      
  # --------------------------------------------------------------------------
  # SLOTS
  # --------------------------------------------------------------------------
  
  
  
  @pyqtSlot(int)
  @pyqtSlot(bool)
  def retranslateUi(self, status):
    ''' Translate the toolBar action buttons '''
    self.setWindowTitle(_translate("MainWindow", "MainWindow", None))
    self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
    self.actionNetwork.setText(_translate("MainWindow", "network", None))
    self.actionReports.setText(_translate("MainWindow", "Reports", None))
    self.actionViewDetails.setText(_translate("MainWindow", "ViewDetails", None))
    self.actionPreferences.setText(_translate("MainWindow", "preferences", None))
    self.actionQuit.setText(_translate("MainWindow", "Quit", None))
  # --------------------------------------------------------------------------


  @pyqtSlot(int)
  @pyqtSlot(bool)
  def showNetworkWidget(self, status):
    ''' Callback for the action button network'''
    if not self.networkWidgetActive:
      #print "network"
      self.splashWidget.setVisible(False)
      self.networkWidget.setVisible(True)
      self.detailsWidget.setVisible(False)
      self.preferencesWidget.setVisible(False)
      self.reportWidget.setVisible(False)      
          
      #TODO find a better way to do this verification 
      self.networkWidgetActive      = True
      self.reportsWidgetActive      = False
      self.viewdetailsWidgetActive  = False
      self.preferencesWidgetActive   = False
  # --------------------------------------------------------------------------
  
  
  @pyqtSlot(int)
  @pyqtSlot(bool)
  def showReportsWidget(self, status):
    ''' Callback for the action button reports'''
    if not self.reportsWidgetActive:
      #print "reports"
      self.splashWidget.setVisible(False)
      self.networkWidget.setVisible(False)
      self.detailsWidget.setVisible(False)
      self.preferencesWidget.setVisible(False)
      
      
      ##############MG####################
      self.reportWidget.setVisible(True)
      
      #TODO find a better way to do this verification 
      self.networkWidgetActive      = False
      self.reportsWidgetActive      = True
      self.viewdetailsWidgetActive  = False
      self.preferencesWidgetActive   = False
      

  @pyqtSlot(int)
  @pyqtSlot(bool)
  def showViewDetails(self, status):
    ''' Callback for the action button view details'''
    if not self.viewdetailsWidgetActive:
      #print "view details"
      self.splashWidget.setVisible(False)
      self.networkWidget.setVisible(False)
      self.detailsWidget.setVisible(True)
      self.preferencesWidget.setVisible(False)
      self.reportWidget.setVisible(False)

      #TODO find a better way to do this verification 
      self.networkWidgetActive      = False
      self.reportsWidgetActive      = False
      self.viewdetailsWidgetActive  = True
      self.preferencesWidgetActive   = False
  # --------------------------------------------------------------------------    
  
      
  @pyqtSlot(int)
  @pyqtSlot(bool)
  def showPreferencesWidget(self, status):
    ''' Callback for the action button preferences'''
    if not self.preferencesWidgetActive:
      #print "preferences"
      self.splashWidget.setVisible(False)
      self.networkWidget.setVisible(False)
      self.detailsWidget.setVisible(False)
      self.preferencesWidget.setVisible(True)
      self.reportWidget.setVisible(False)
      
      #TODO find a better way to do this verification 
      self.networkWidgetActive      = False
      self.reportsWidgetActive      = False
      self.viewdetailsWidgetActive  = False
      self.preferencesWidgetActive   = True
  # --------------------------------------------------------------------------
  
  
  
  
  
  
  @pyqtSlot(int)
  @pyqtSlot(bool)
  def connectToServerPressed(self, status):
    ''' '''
    if status:
      self.connectToServer.emit()
      self.pb_connect.setText("Connecting")
    else:
      self.disconnectFromServer.emit()
  # --------------------------------------------------------------------------

  
  @pyqtSlot(int)
  @pyqtSlot(bool)
  def openDevicePressed(self, status):
    if status:
      self.openUSBDevice.emit()
      self.pb_open_device.setText("Opening")
    else:
      self.closeUSBDevice.emit()
  # --------------------------------------------------------------------------






  
  @pyqtSlot('QString', name='updateStatusBarMessages')
  def updateStatusBarMessages(self, msg):
    ''' '''
    self.statusbar.showMessage(str(msg), 2000)
  # --------------------------------------------------------------------------
  
  
  
  
  
  
  
  @pyqtSlot(int)
  @pyqtSlot(bool)
  def updateDeviceStatus(self, status):
    ''' '''
    if status:
      icon = QtGui.QIcon()
      icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/on.png")))
      self.pb_open_device.setIcon(icon)
      self.pb_open_device.setText("Opened")
      self.deviceOpened.emit(True)
      
    else:
      icon = QtGui.QIcon()
      icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/off.png")))
      self.pb_open_device.setIcon(icon)
      self.pb_open_device.setText("Closed")
      self.deviceOpened.emit(False)
  # --------------------------------------------------------------------------
  
  
  @pyqtSlot(int)
  @pyqtSlot(bool)  
  def updateServerStatus(self, status):
    ''' '''
    if status:
      icon = QtGui.QIcon()
      icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/on.png")))
      self.pb_connect.setIcon(icon)
      self.pb_connect.setText("Connected")
    else:
      icon = QtGui.QIcon()
      icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/off.png")))
      self.pb_connect.setIcon(icon)
      self.pb_connect.setText("Disconnected")
  # --------------------------------------------------------------------------
  
  
  
  
  
  
  
  
  @pyqtSlot("QEvent")
  def closeEvent(self, event):
    self.f_log.debug('Closing the application Main Window')
    self.closeUSBDevice.emit()
    self.destroyed.emit(self)
    time.sleep(1) # give time to close the comm port if user do not close it
    event.accept() # let the window close
  # --------------------------------------------------------------------------


  @pyqtSlot(str, str, name="showMessageDialog")
  def showMessageDialog(self, msg_type, msg):
    
    print "showMessageDialog"
    
    # Warning
    if msg_type == 'w':
      print "warning"
      QMessageBox.warning(self, 
                          "Warning", 
                          msg, 
                          buttons=QMessageBox.Ok, 
                          defaultButton=QMessageBox.NoButton)
      
    # Information
    elif msg_type == 'i':
      print "information"
      QMessageBox.information(self, 
                              "Info", 
                              msg, 
                              buttons=QMessageBox.Ok, 
                              defaultButton=QMessageBox.NoButton)
      
    # Critical
    elif msg_type == 'c':
      print "critical"
      QMessageBox.critical(self, 
                           "Critical", 
                           msg, 
                           buttons=QMessageBox.Ok, 
                           defaultButton=QMessageBox.NoButton)
    
    # Nothing to do, the type is not correct
    else: 
      pass
      # TODO - something do do here
    
  @pyqtSlot()
  def testFunction(self):
    self.f_log.debug("I'm been called from MainWindow {0}".format(current_thread()))

  # ----------------------------------------------------------------------------------------------

# EOF ------------------------------------------------------------------------------------------------------------