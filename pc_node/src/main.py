#! /usr/bin/python
'''
Created on May 15, 2015
@author: Magno Guedes, Andre Silva
@mail: magno.guedes@introsys.eu, andre.silva@introsys.eu
'''

import sys
import os
import logging
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, QObject, SLOT, SIGNAL
from logging import handlers 
from gui.MainWindow import Ui_MainWindow
from control.AppController import AppController



if __name__ == '__main__': 
  ''' main '''
  
  try:   
    # Logging format 
    #log_format = logging.Formatter('[%(name)s][%(levelname)s] : %(asctime)s (%(filename)s - %(funcName)s) - %(message)s') # FOR Debug
    log_format = logging.Formatter('[%(name)s][%(levelname)s] : %(asctime)s - %(message)s')
    # File rotation
    filename = '{0}/.fresh/logs/fresh.log'.format(QtCore.QDir.homePath())
    if not os.path.exists(os.path.dirname(filename)):
      os.makedirs(os.path.dirname(filename))
      with open(filename, "w") as f:
        f.write("# LOG FILE #")
    # File handler
    fh = handlers.RotatingFileHandler(filename, maxBytes=200, backupCount=5)     
    fh.setFormatter(log_format)
    fh.setLevel(logging.INFO)
    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(log_format)
    ch.setLevel(logging.DEBUG)
    # MainApplication logger
    orion_log = logging.getLogger('App')
    orion_log.setLevel(logging.DEBUG)
    orion_log.addHandler(fh)
    orion_log.addHandler(ch)
    # Database logger
    db_log = logging.getLogger('DB')
    db_log.setLevel(logging.DEBUG)
    db_log.addHandler(fh)
    db_log.addHandler(ch) 
  except IOError as e:
    print 'Unable to create a log File\nI/O error({0}): {1}'.format(e.errno, e.strerror)
    #raise
    pass
  # --------------------------------------------------------------------------
    
  app = QtGui.QApplication(sys.argv)
  mainWindow = Ui_MainWindow()
  control = AppController()
  
  # Create a parallel with event loop
  controlThread = QtCore.QThread()
  control.moveToThread(controlThread)

  # This signals handle the closing event of the application, destroying all the running threads of the application
  QObject.connect(mainWindow, SIGNAL("destroyed()"), controlThread, SLOT("quit()"), Qt.QueuedConnection )
  QObject.connect(mainWindow, SIGNAL("destroyed()"), app, SLOT("quit()"), Qt.QueuedConnection )
  QObject.connect(app, SIGNAL("quit()"), app, SLOT("deleteLater()"), Qt.QueuedConnection )
  QObject.connect(controlThread, SIGNAL("quit()"), controlThread, SLOT("deleteLater()"), Qt.QueuedConnection )
  
  
  
  
  # This signals handle the events originated from the control module and pass them to the UI
  QObject.connect(control, SIGNAL("loadLastPreferences()"), control, SLOT("loadPreferencesFromLast()"), Qt.QueuedConnection)
  QObject.connect(mainWindow.preferencesWidget, SIGNAL("savePreferences(PyQt_PyObject)"), control, SLOT("savePreferencesToFile(PyQt_PyObject)"), Qt.QueuedConnection)
  QObject.connect(mainWindow.preferencesWidget, SIGNAL("loadOldPreferences()"), control, SLOT("loadPreferencesFromBackup()"), Qt.QueuedConnection)
  QObject.connect(mainWindow.preferencesWidget, SIGNAL("loadDefaultPreferences()"), control, SLOT("loadPreferencesFromDefault()"), Qt.QueuedConnection)
  QObject.connect(control, SIGNAL("showDialogMessage(QString, QString)"), mainWindow, SLOT("showMessageDialog(QString, QString)"), Qt.QueuedConnection)
  QObject.connect(control, SIGNAL("updatePreferencesValues(PyQt_PyObject)"), mainWindow.preferencesWidget, SLOT("displayChangedPreferences(PyQt_PyObject)"))
  QObject.connect(control, SIGNAL("initiate()"), control, SLOT("initiated()"), Qt.QueuedConnection)
  
  
  
  # Exchange of the Table models from the GUI to the controller interface for data manipulation 
  # Device Monitor - Device Details Widget
  QObject.connect(control, SIGNAL("getMonitorSIM()"), mainWindow.detailsWidget, SLOT("monitorSIMRequest()"), Qt.QueuedConnection)
  QObject.connect(mainWindow.detailsWidget, SIGNAL("sendMonitorSIM(PyQt_PyObject)"), control, SLOT("monitorSIMReceived(PyQt_PyObject)"), Qt.QueuedConnection)
  [[]]
  # Available Sensors - Network Widget
  QObject.connect(control, SIGNAL("getAvailableSIM()"), mainWindow.networkWidget, SLOT("availableSIMRequest()"), Qt.QueuedConnection)
  QObject.connect(mainWindow.networkWidget, SIGNAL("sendAvailableSIM(PyQt_PyObject)"), control, SLOT("availableSIMReceived(PyQt_PyObject)"), Qt.QueuedConnection)
  
  # Subscribed Sensors - Network Widget
  QObject.connect(control, SIGNAL("getSubscribeSIM()"), mainWindow.networkWidget, SLOT("subscribeSIMRequest()"), Qt.QueuedConnection)
  QObject.connect(mainWindow.networkWidget, SIGNAL("sendSubscribeSIM(PyQt_PyObject)"), control, SLOT("subscribeSIMReceived(PyQt_PyObject)"), Qt.QueuedConnection)
  
  
  

  QObject.connect(mainWindow.detailsWidget, SIGNAL('askForDeviceDetails(int)'), control, SLOT('askedForDeviceDetails(int)'), Qt.QueuedConnection)
  QObject.connect(control, SIGNAL('showDeviceDetails(PyQt_PyObject)'), mainWindow.detailsWidget, SLOT('displayDeviceDetails(PyQt_PyObject)'), Qt.QueuedConnection)
  QObject.connect(control, SIGNAL('getSelectedDevice()'), mainWindow.detailsWidget, SLOT("returnSelectedDevice()"), Qt.QueuedConnection)  
  QObject.connect(mainWindow.detailsWidget, SIGNAL('sendSelectedDevice(int)'), control, SLOT("askedForDeviceDetails(int)"), Qt.QueuedConnection)




  QObject.connect(mainWindow.networkWidget, SIGNAL("addSelectedDevicesToSub()"), control, SLOT("addDeviceSubscriptionToCosmos()"), Qt.QueuedConnection)
  QObject.connect(mainWindow.networkWidget, SIGNAL("removeSelectedDeviceFromSub(int)"), control, SLOT("removeDeviceSubscriptionFromCosmos(int)"), Qt.QueuedConnection)
  QObject.connect(mainWindow.networkWidget, SIGNAL("editSelectedDeviceFromSub(int, QString)"), control, SLOT("editDeviceSubscriptionOnDatabase(int, QString)"), Qt.QueuedConnection)

  

  QObject.connect(control, SIGNAL('updateAddButtonStatus()'), mainWindow.networkWidget, SLOT('lockUnlockAddButton()'), Qt.QueuedConnection)
  QObject.connect(control, SIGNAL("updateEditRemoveButtonStatus()"), mainWindow.networkWidget, SLOT("lockUnlockEditRemoveButton()"), Qt.QueuedConnection)
  
  QObject.connect(control, SIGNAL('sendMsgToStatusBar()'), mainWindow.networkWidget, SLOT('updateStatusBarMessages(QString)'), Qt.QueuedConnection)


  
  # CONNECTION OF NEW SIGNALS FROM THE CONTROLLER TO THE GUI MUST GO HERE
  
  
  
  # start the control thread
  controlThread.start()

  # Shows the application MainWindow
  mainWindow.show() 
  
  # Load the default preferences to the GUI
  control.loadLastPreferences.emit()
  
  # Start other important functions 
  control.initiate.emit()
  
  # Starts the eventLoop for the MainThread 
  sys.exit(app.exec_())
  controlThread.quit()
  controlThread.wait()
# EOF ------------------------------------------------------------------------------------------------------------