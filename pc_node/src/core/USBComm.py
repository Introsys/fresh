#!/usr/bin/python


# TODO Author info


# Imports
import sys
import serial
import logging
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QMutexLocker, QMutex, QThread


class USBComm(QtCore.QThread):
  ''' 
  TODO - Description
  '''
  # --------------------------------------------------------------------------
  # SLOTS
  # --------------------------------------------------------------------------
  
  statusNotification = pyqtSignal('QString', name="statusNotification")
  portAvailable = pyqtSignal(object, name="portAvailable")


  # --------------------------------------------------------------------------
  # SLOTS
  # --------------------------------------------------------------------------
  
  @pyqtSlot(name="stop")
  def stop(self):
    ''' 
    Stop the running thread if no __serial port device found at the moment
    There is no terminate at the close because the run function is responsible 
    for terminating the process at the conclusion of the thread work
    '''
    self.quit()
  # ----------------------------------------------------------------------------------------------
  
  
  @pyqtSlot(name="quit")
  def quit(self):
    ''' 
    Same as quit() function
    '''
    if self.isRunning():
      with QMutexLocker(self.mutex):
        self.__tryingToOpen = False
  # --------------------------------------------------------------------------


  # --------------------------------------------------------------------------
  # Class Main Code
  # --------------------------------------------------------------------------

  def __init__(self, port, baudrate):
    ''' 
    TODO - Description
    '''
    QtCore.QThread.__init__(self)
    self.f_log = logging.getLogger('App') # this can be called in any place
    self.mutex = QMutex()
    with QMutexLocker(self.mutex):
      self.__tryingToOpen = True
      self.port = port
      self.baudrate = baudrate
      self.__serial = None
  # --------------------------------------------------------------------------  
  
  
  
  # Threat run function
  def run(self):
    ''' 
    Waits for a __serial port to be connected to the PC
    '''
    while self.__tryingToOpen:
      try:
        with QMutexLocker(self.mutex):
          self.__serial = serial.Serial(str(self.port), str(self.baudrate))
          self.__tryingToOpen = False;
        self.portAvailable.emit(self.__serial)
        self.statusNotification.emit('Serial Port Open With Success')
        self.f_log.info('Serial Port Open With Success')
      except serial.SerialException as e:
        self.statusNotification.emit('ERRO : {0}'.format(str(e)))
        self.f_log.error("ERRO : {0}".format(str(e)))
      except ValueError as e:
        self.statusNotification.emit('ERRO : {0}'.format(str(e)))
        self.f_log.error('ERRO : {0}'.format(str(e)))
      except: 
        e = sys.exc_info()[0]
        self.statusNotification.emit('ERRO: {0}'.format(str(e)))
        self.f_log.error('ERRO : {0}'.format(str(e)))
      finally:
        QThread.msleep(2000)
    self.finished.emit()
  # --------------------------------------------------------------------------
  
  
  def __del__(self):
    ''' 
    When the object goes out of scope the object will be destroyed and emit the
    destroyed signal()
    '''
    self.f_log.debug('USBComm object destroyed')
    self.destroyed.emit(self)
  # --------------------------------------------------------------------------


  def open(self):
    ''' 
    Same as start() method
    '''
    self.start()
  
  #EOF