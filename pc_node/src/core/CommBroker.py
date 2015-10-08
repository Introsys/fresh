#! /usr/bin/python
'''
Created on May 15, 2015

@author: Magno Guedes, Andre Silva
@mail: magno.guedes@introsys.eu, andre.silva@introsys.eu
'''
import sys
import json
import logging
import time
from threading import Thread
from PyQt4 import QtCore
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot, QMutex, QThread, QMutexLocker
from PyQt4.QtCore import SLOT, SIGNAL
from xbee import ZigBee
from core.OrionNGSIApi import OrionNGSIApi
from PyQt4.QtCore import QTimer #@UnusedImport

from core.Device import Device #@UnusedImport
from core.USBComm import USBComm 
from datetime import datetime


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


class CommBroker(QtCore.QThread):
  ''' 
  TODO - Description
  '''
  
  mutex = QMutex()
  
  # -----------------------------------------------------------------------------
  # SIGNALS
  # -----------------------------------------------------------------------------
  
  addDevice     = pyqtSignal('QString', name='addDevice')
  removeDevice  = pyqtSignal('QString', name='removeDevice')
  updateDevice  = pyqtSignal('QString', name='updateDevice')
  
  subscribeResult    = pyqtSignal(bool, 'QString', 'QString', 'QString', name='subscribeResult')
  unsubscribeResult  = pyqtSignal(bool, 'QString', name='unsubscribeResult')
  sendMsgToStatusBar = pyqtSignal('QString', name="sendMsgToStatusBar")
  
  
  isUsbPortOpen   = pyqtSignal(bool, name='isUsbPortOpen')
  isOrionLive     = pyqtSignal(bool, name='isOrionLive')
  closeUsbDevice  = pyqtSignal(name='closeUsbDevice')

  
  
  def __init__(self):
    ''' 
    TODO - Description 
    '''
    QThread.__init__(self)
    self.f_log = logging.getLogger('App') # this can be called in any place
    self.f_log.debug("Object CommBroker Created")
    self.timerReconnectToOrion = QTimer()
    self.timerReconnectToOrion.setSingleShot(True)
    self.timerReconnectToOrion.setInterval(2000)
    
    QObject.connect(self.timerReconnectToOrion, SIGNAL("timeout()"), self, SLOT("tryToReconnect()"))
     
    with QMutexLocker(self.mutex):
      
      self.__is_running = True  # Control for the main thread
      self.__opened = False
      
      # Objects
      self.__serial = None
      
      # threads
      self.__t_xbee = None
      self.__t_usbCom = None
      self.__t_xbee_diag = None
      self.__t_update_orion = None
      
      # value in seconds
      self.device_timeout = 60
      
      self.devices = dict()
  # -----------------------------------------------------------------------------
  
     
  def __del__(self):
    '''
    TODO - Description
    '''
    self.destroyed.emit(self)
    self.f_log.debug('Object CommBroker Destroyed')
  # -----------------------------------------------------------------------------

  
  def run(self):
    ''' 
    TODO - Description
    '''
    # TODO - This should use a thread pool for reusing the created threads - ThreadPoolExecutor
    try:
      while self.__is_running:
        with QMutexLocker(self.mutex):
          if not self.__serial and (not self.__opened) and (not self.__t_usbCom.isRunning()):
            self.__t_usbCom.start()
          elif self.__serial and (not self.__opened):          
            self.__t_xbee = ZigBee(self.__serial, callback=self.__read_xbee, escaped=True)
            time.sleep(0.1)                    
            self.__opened = True            
            self.__t_xbee_diag.start()
            time.sleep(0.1)
            self.__t_update_orion.start()
            time.sleep(0.1)
          if self.__opened and not self.__t_xbee.isAlive():          
            self.__serial.close()
            self.__serial = None
            self.__opened = False
            time.sleep(2)
            self.__t_xbee_diag    = Thread(target=self.__query_remote_diag, name="xbee_dig")   
            self.__t_update_orion = Thread(target=self.__update_orion, name="update_orion")              
            self.__t_usbCom       = USBComm(self.port, self.baudrate)  
            QObject.connect(self.__t_usbCom, SIGNAL("statusNotification(QString)"), self, SLOT("receiveUSBPortNotification(QString)"))
            QObject.connect(self.__t_usbCom, SIGNAL("portAvailable(PyQt_PyObject)"), self, SLOT("getUsbPort(PyQt_PyObject)"))  
        time.sleep(0.1)
    except:
      e = sys.exc_info()[0] 
      self.f_log.error('ERRO {0}'.format(str(e)))
      raise
    
    
    finally:
      print "----------------------------------------------------------------------------------"
      self.__serial = None
      self.__opened = False
      
      if self.__t_xbee:
        self.__t_xbee.halt()
      if self.__serial:
        self.__serial.close()
      self.emit(SIGNAL("quit()"), self.__t_usbCom)
      self.finished.emit()
  # -----------------------------------------------------------------------------  

  
  def open(self, orion_ip, orion_port, token, port, baudrate):
    ''' 
    TODO - DESCRIPTION
    '''
    try:
      # Connection to Xbee coordinaton
      
      self.orionIp = orion_ip
      self.orionPort = orion_port
      self.authToken = token
      self.port = port
      self.baudrate = baudrate
      
      
      # Threads
      self.__t_usbCom = USBComm(self.port, self.baudrate)
      self.__t_xbee_diag = Thread(target=self.__query_remote_diag, name="xbee_dig")   
      self.__t_update_orion = Thread(target=self.__update_orion, name="update_orion")          
                
      # Connects
      QObject.connect(self.__t_usbCom, SIGNAL("statusNotification(QString)"), self, SLOT("receiveUSBPortNotification(QString)"))
      QObject.connect(self.__t_usbCom, SIGNAL("portAvailable(PyQt_PyObject)"), self, SLOT("getUsbPort(PyQt_PyObject)"))
      
      
      
      # Starts the thread
      self.start() 
    except:
      e = sys.exc_info()[0] 
      self.f_log.error('ERRO {0}'.format(str(e)))
      raise  
  # -----------------------------------------------------------------------------

  
  # -----------------------------------------------------------------------------
  # Threads
  # -----------------------------------------------------------------------------
  
  
  def __read_xbee(self, data):
    ''' 
      Threaded method for read the data from the nodes
      The thread is created by the Xbee API 
    '''
    with QMutexLocker(self.mutex):
      try:
        addr = data['source_addr_long'].encode('hex')
        if data['id'] =='rx':
          if 'element' in data['rf_data']:
            if not self.devices.has_key(addr):
              jsonObj = json.loads(data.get('rf_data'))
              newDevice = Device()
              newDevice.id = addr
              newDevice.element = jsonObj['element']
              self.devices[addr] = newDevice         
            elif self.devices.has_key(addr) and not self.devices[addr].attributes_list_complete:
              self.devices[addr].attributes_list_complete = True
              # New sensor discovered and with all their attributes  
              # A Signal is emit to the Controller to display the changes in the UI
              self.addDevice.emit(addr)
            elif self.devices.has_key(addr) and self.devices[addr].attributes_list_complete:
              # Device last update
              # Used also to check the idle time
              self.devices[addr].lastUpdateTimestamp = datetime.now()
          elif 'attribute' in data['rf_data'] and self.devices.has_key(addr):
            jsonObj = json.loads(data.get('rf_data'))
            self.devices[addr].attributes[jsonObj['attribute']['name']] = jsonObj['attribute']
            # Emit a signal the sensor date as been updated
            self.updateDevice.emit(addr)
        elif data['id'] == 'remote_at_response' and self.devices.has_key(addr):
          try:
            if data['frame_id'] == 'D': #diagnostic msgs
              if data['command'] == str('TP'):
                self.devices[addr].diagnostic['Temp'] = int(data['parameter'].encode('hex'), 16)
              elif str(data['command']) == 'DB':
                self.devices[addr].diagnostic['Sign'] = int(data['parameter'].encode('hex'), 16)
              elif str(data['command']) == '%V':
                self.devices[addr].diagnostic['Volt'] = (int(data['parameter'].encode('hex'), 16))*(1200/1024)
              # Emit a signal the sensor date as been updated              
              self.updateDevice.emit(addr)
          except KeyError as e:
            # If the device did not respond to the diagnostic command it should be down
            # and so we check the time elapsed from the last update and if its greater then the threshold
            # we remove the sensor node from the devices list
            self.f_log.info("Unable to connect to sensor node {device}".format(device=addr))
            self.__removeDevice(addr)
      except:
        e = sys.exc_info()[0]
        self.f_log.error('ERRO [XBEE] {0}'.format(str(e)))
        raise
  # -----------------------------------------------------------------------------  
  

  def __query_remote_diag(self):
    ''' Thread function for querying the nodes status '''
    while self.__serial and self.__opened:  
      with QMutexLocker(self.mutex):
        for addr in self.devices.keys():
          try:
            haddr = ''.join([chr(int(''.join(c), 16)) for c in zip(addr[0::2], addr[1::2])])
            self.__t_xbee.send('remote_at', 
                           frame_id='D', 
                           command='TP', 
                           dest_addr_long=haddr)
            time.sleep(0.1)
            self.__t_xbee.send('remote_at', 
                           frame_id='D', 
                           command='DB', 
                           dest_addr_long=haddr)
            time.sleep(0.1)
            self.__t_xbee.send('remote_at', 
                           frame_id='D', 
                           command='%V', 
                           dest_addr_long=haddr)
          except:
            e = sys.exc_info()[0]
            print str(e)
            raise
      time.sleep(2)
  # -----------------------------------------------------------------------------
  
   
  def __update_orion(self):
    ''' Thread to update the __orionClient every second '''
    try:
      orionClient = OrionNGSIApi(self.orionIp, self.orionPort, self.authToken)
      while self.__serial and self.__opened:
        for addr in self.devices.keys():
          orionClient.createContext(self.devices[addr].element['type'],
                                    self.devices[addr].element['id'],
                                    self.devices[addr].attributes.values())
        time.sleep(1)
    except:
      self.f_log.error('something nasty happened')
      self.timerReconnectToOrion.start()
      pass
  # -----------------------------------------------------------------------------
  
 
  # -----------------------------------------------------------------------------
  # PRIVATE METHODS
  # -----------------------------------------------------------------------------
 
  def __cygnusSubscribeContext(self, _addr):
    ''' 
      TODO - DESCRIPTION
    '''
    addr = _addr.__str__()
    orionClient = OrionNGSIApi(self.orionIp, self.orionPort, self.authToken)
    # This will hold until receive a response from the server
    result = orionClient.persistDataToHDFS(self.devices[addr].element['type'], 
                                                  self.devices[addr].element['id'],
                                                  self.devices[addr].attributes.values())

    print self.devices[addr].element['type']
    print self.devices[addr].element['id']


    if result['http_code'].__str__() == '200':
      self.f_log.info('HTTP Code: {0}  | Subscription sent successfully ID: {1} Time: {2} Device: {3}'.format(result['http_code'],
                                                                                                              result['subscription_id'],
                                                                                                              result['subscription_duration'],
                                                                                                              addr))
      self.subscribeResult.emit(True, addr, result['subscription_id'], result['subscription_duration'])
    else:
      self.subscribeResult.emit(False, addr, None, None)
      
      
    self.f_log.debug('Send a subscription resquest')
      
  # -----------------------------------------------------------------------------

  def __cygnusUnsubscribeContext(self, _subscriptionId, addr):
    ''' 
      TODO - DESCRIPTION
    '''
    subscriptionId = _subscriptionId.__str__() 
    orionClient = OrionNGSIApi(self.orionIp, self.orionPort, self.authToken)
    # This will hold until receive a response from the server
    result = orionClient.removeHDFSSubscription(subscriptionId)
    if (result['http_code'].__str__() == '200') and \
       (result['ngsi_code'].__str__() == '200'):
      self.unsubscribeResult.emit(True, addr)
      self.f_log.debug('Send a unsubscription request')  
    else:
      self.unsubscribeResult.emit(False, addr)
      self.f_log.debug('Send a unsubscription request')  
    
    
    
            
    
  # -----------------------------------------------------------------------------

  def __removeDevice(self, _addr):
    ''' 
      TODO - DESCRIPTION
    '''
    try: 
      addr = _addr.__str__()      
      elapsed_time = datetime.now() - self.devices[addr].lastUpdateTimestamp
      if elapsed_time.total_seconds() > self.device_timeout:
        self.devices.pop(addr)
        self.f_log.info("Remove device {device}".format(device=addr))
        self.removeDevice.emit(addr)
    except Exception as e:
      self.f_log.error("ERRO {0}".format(str(e)))
  # -----------------------------------------------------------------------------






  ''' BREAK '''




  # -----------------------------------------------------------------------------
  # SLOTS
  # -----------------------------------------------------------------------------
  
 
  @pyqtSlot(name="tryToReconnect")
  def tryToReconnect(self):
    if not self.__t_update_orion.is_alive():
      self.__t_update_orion = Thread(target=self.__update_orion, name="update_orion")   
      self.__t_update_orion.start()
    
  # -----------------------------------------------------------------------------


  @pyqtSlot(name="close")
  def close(self):
    ''' 
    TODO - Description 
    '''
    if self.isRunning():     
      with QMutexLocker(self.mutex):  
        if self.__serial and self.__serial.isOpen():
          self.__t_xbee.halt()      
          self.__serial.close()
          self.opened = False
        else:
          self.closeUsbDevice.emit()
        self.isUsbPortOpen.emit(False)
        self.__is_running = False  
  # -----------------------------------------------------------------------------
  
  @pyqtSlot('QString', name="receiveUSBPortNotification")
  def receiveUSBPortNotification(self, sigstr):
    #TODO
    self.sendMsgToStatusBar.emit(sigstr.__str__())
  # -----------------------------------------------------------------------------
  
  @pyqtSlot(object, name="getUsbPort")
  def getUsbPort(self, serial):
    with QMutexLocker(self.mutex):
      self.__serial = serial
  # -----------------------------------------------------------------------------

  @pyqtSlot(str, name='cygnusSubscribeContext')
  def cygnusSubscribeContext(self, addr):
    '''
      TODO - DESCRIPTION
    '''
    
    self.__t_subscribe = FunctionThreadHandler(self.__cygnusSubscribeContext, addr)
    self.__t_subscribe.start()
      
  # -----------------------------------------------------------------------------
  
  @pyqtSlot('QString', 'QString', name='cygnusUnsubscribeContext')
  def cygnusUnsubscribeContext(self, subscriptionId, addr):
    ''' 
      TODO - DESCRIPTION
    '''
    
    self.__t_unsubscribe = FunctionThreadHandler(self.__cygnusUnsubscribeContext, subscriptionId, addr)
    self.__t_unsubscribe.start()
  # -----------------------------------------------------------------------------




  @pyqtSlot(name='devicesHeatBeatCheck')
  def devicesHeatBeatCheck(self):
    '''
      Heart beat check
      it's another way to check if the devices are still alive
    '''
    with QMutexLocker(self.mutex):
      try:
        for device in self.devices.keys():
          self.__removeDevice(device)
      except Exception as e: 
        self.f_log.error("ERRO {0}".format(str(e)))
  # -----------------------------------------------------------------------------
  
  
# ------------------------------------------------------------------------------------------------------------



class FunctionThreadHandler(Thread):
  
  def __init__(self, target, *args):
    self._target = target
    self._args = args
    Thread.__init__(self)
  # -----------------------------------------------------------------------------
  
  
  def run(self):
    self._target(*self._args)
  # -----------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------




if __name__ == '__main__':
  pass




# EOF