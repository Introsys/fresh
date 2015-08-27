#! /usr/bin/python
'''
Created on May 15, 2015

@author: Magno Guedes, Andre Silva
@mail: magno.guedes@introsys.eu, andre.silva@introsys.eu
'''
import sys
import serial
import json
import time
import copy
from threading import Thread
from PyQt4.QtCore import QMutex, QMutexLocker #@UnusedImport
from PyQt4.QtCore import QObject, SIGNAL #@UnusedImport
from xbee import ZigBee
from orion_client import OrionClient
from PyQt4.QtCore import QTimer #@UnusedImport
from PyQt4 import QtCore
from PyQt4.Qt import pyqtSlot
from mutex import mutex #@UnusedImport
from communication.device import Device #@UnusedImport


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


class Gateway(QtCore.QObject):
  ''' TODO - Description'''
  mutex = QtCore.QMutex()
  
  closeDevice               = QtCore.pyqtSignal(name="closeDevice") 
  newSensorNode             = QtCore.pyqtSignal(object, name="newSensorNode")
  updateDevicesList         = QtCore.pyqtSignal(object, name="updateDevicesList")
  sensorNodeAttributeUpdate = QtCore.pyqtSignal(object, name="sensorNodeAttributeUpdate")
  notifyWidgetDeviceStatus  = QtCore.pyqtSignal(bool, name="notifyWidgetDeviceStatus")
  notifyWidgetServerStatus  = QtCore.pyqtSignal(bool, name="notifyWidgetServerStatus")
  notifyWidgetNotification  = QtCore.pyqtSignal(QtCore.QString, name="notifyWidgetNotification")
  

  def __init__(self, parent = None):
    ''' TODO - Description '''
    
    super(Gateway, self).__init__()
    
    self.__parent = parent
    self.port = None
    self.baudrate = None
    self.opened = False
    self.devices = None
    self.serial = None
    self.xbee = None
    self.orion = None
    
    QtCore.QObject.connect(self, QtCore.SIGNAL("notifyWidgetDeviceStatus(bool)"), self.__parent.notifyDeviceStatusToWidget)
    QtCore.QObject.connect(self, QtCore.SIGNAL("notifyWidgetServerStatus(bool)"), self.__parent.notifyServerStatusToWidget)
    QtCore.QObject.connect(self, QtCore.SIGNAL("notifyWidgetNotification(QString)"), self.__parent.notifyNotificationsToWidget)
    
    
    # connects to the networkWidget
    QtCore.QObject.connect(self, QtCore.SIGNAL("updateDevicesList(PyQt_PyObject)"), 
                           self.__parent.parentWidget.networkWidget.helper, QtCore.SLOT("updateSensorList(PyQt_PyObject)"))
    
    # connects to the networkWidget
    QtCore.QObject.connect(self, QtCore.SIGNAL("newSensorNode(PyQt_PyObject)"), 
                           self.__parent.parentWidget.networkWidget.helper, QtCore.SLOT("sensorNodeDiscovered(PyQt_PyObject)"))
    
    
    
    
    # connects for the detailsWidget
    QtCore.QObject.connect(self, QtCore.SIGNAL("newSensorNode(PyQt_PyObject)"),
                           self.__parent.parentWidget.detailsWidget.helper, QtCore.SLOT("addSensorNodeToDetails(PyQt_PyObject)"))
    
    QtCore.QObject.connect(self, QtCore.SIGNAL("sensorNodeAttributeUpdate(PyQt_PyObject)"),
                           self.__parent.parentWidget.detailsWidget.helper, QtCore.SLOT("showSensorNodeAttributes(PyQt_PyObject)"))
    
    self.devices = dict()
    
    self.t_diag = None
    self.t_orion = None

     

  # -----------------------------------------------------------------------------
  def open(self, orion_ip, orion_port, username, password, 
                        keystone_ip, keystone_port, keystone_url, tennant_name,
                        tennant_id, domain, token_path, port, baudrate):
    ''' '''
    #Connection to orion server
    self.orion_ip = orion_ip
    self.orion_port = orion_port
    self.username = username
    self.password = password
    self.keystone_ip = keystone_ip
    self.keystone_port = keystone_port
    self.keystone_url = keystone_url
    self.tenant_name = tennant_name
    self.tenant_id  = tennant_id
    self.domain = domain
    self.token_path = token_path



    # connection to Xbee coordinator
    self.port = port
    self.baudrate = baudrate
    
    # USB serial listener - scans for the Xbee coordinator
    self.thread = OpenUsbPort(self.port, self.baudrate, self)
    
    # connects
    self.connect(self.thread, self.thread.msgNotify, self.receiveMsgFromOpenUsbPort)
    self.connect(self.thread, self.thread.startSendingDatatoOrion, self.startSendingDatatoOrion)   
    
    # start listener Thread - no blocking GUI mechanism
    self.thread.start()
    
    
  # -----------------------------------------------------------------------------
  @pyqtSlot(str)
  def receiveMsgFromOpenUsbPort(self, sigstr):
    self.notifyWidgetNotification.emit(sigstr)
    
    
  @pyqtSlot(serial.Serial)  
  def startSendingDatatoOrion(self, serial):
    try:
      self.serial = serial
      if self.serial:
        if self.serial.isOpen():
          self.mutex.lock()
          self.opened = True
          self.mutex.unlock()
          
          self.xbee = ZigBee(self.serial, callback=self.read_xbee, escaped=True)
          
          self.orion = OrionClient(self.orion_ip, self.orion_port, self.username, self.password, 
                                   self.keystone_ip, self.keystone_port, self.keystone_url, 
                                   self.tenant_name, self.tenant_id, self.domain, self.token_path, parent=self)
          
          self.t_diag = Thread(target=self.query_remote_diag, name="xbee_dig")  # IMPORTANT
          self.t_orion = Thread(target=self.update_orion, name="orion")         # IMPORTANT
          
          time.sleep(0.1)       # save
          self.t_diag.start()
          time.sleep(0.1)       # save
          self.t_orion.start()
          time.sleep(0.1)       # save
          
          self.notifyWidgetDeviceStatus.emit(True)
    except:       
      e = sys.exc_info()[0] 
      print str(e)
      #raise
  
  
  
  @pyqtSlot()
  def sendSubscritionToCygnus(self):
    ''' '''
    # TODO - thread
  
    
  @pyqtSlot()
  def sendUnSubscritionToCygnus(self):
    ''' '''
    # TODO - thread
    
    

  # -----------------------------------------------------------------------------
  def close(self):
    ''' TODO - Description '''    
  
    if self.serial and self.serial.isOpen():
      self.xbee.halt()      
      self.serial.close()

    else:
      self.closeDevice.emit()    
      
    self.notifyWidgetDeviceStatus.emit(False)
    self.mutex.lock()
    self.opened = False
    self.mutex.unlock()
    

  # -----------------------------------------------------------------------------
  def read_xbee(self, data):
    ''' TODO - Description '''
    
    try:
      addr = data['source_addr_long'].encode('hex')
      if data['id'] =='rx':
        # -------------------------------------------------------------
        if 'element' in data['rf_data']:
          #print "element" # DEBUG
          if not self.devices.has_key(addr):
            jsonObj = json.loads(data.get('rf_data'))
            newDevice = Device()
            newDevice.id = addr
            newDevice.element = jsonObj['element']
            self.devices[addr] = newDevice         
                 
          elif self.devices.has_key(addr) and self.devices[addr].control_flag:
            #print "added the sensor {0}".format(addr)
            self.devices[addr].control_flag = False
            self.devices[addr].attributes_list_complete = True
            #self.newSensorNode.emit(copy.deepcopy(self.devices[addr])) # Send signal with new device
            self.newSensorNode.emit(self.devices[addr]) # Send signal with new device
          elif self.devices.has_key(addr) and self.devices[addr].attributes_list_complete:
            self.updateDevicesList.emit(self.devices)
        
        # -------------------------------------------------------------
        elif 'attribute' in data['rf_data'] and self.devices.has_key(addr):
          #print "attributes" # DEBUG
          jsonObj = json.loads(data.get('rf_data'))
          self.devices[addr].attributes[jsonObj['attribute']['name']] = jsonObj['attribute']
      # ---------------------------------------------------------------
      elif data['id'] == 'remote_at_response' and self.devices.has_key(addr):
        if data['frame_id'] == 'D': #diagnostic msgs
          if data['command'] == str('TP'):
            self.devices[addr].diagnostic['Temp'] = int(data['parameter'].encode('hex'), 16)
          elif str(data['command']) == 'DB':
            self.devices[addr].diagnostic['Sign'] = int(data['parameter'].encode('hex'), 16)
          elif str(data['command']) == '%V':
            self.devices[addr].diagnostic['Volt'] = (int(data['parameter'].encode('hex'), 16))*(1200/1024)
    
      self.sensorNodeAttributeUpdate.emit(self.devices) # send signal to real time viewer
      #print self.devices
      #print "devices are {0}".format(len(self.devices))
    except:
      e = sys.exc_info()[0]
      print str(e)
      #raise

  # -----------------------------------------------------------------------------
  def query_remote_diag(self):
    ''' TODO - Description '''
    while self.opened:  
      for addr in self.devices.keys():
        try:
          haddr = ''.join([chr(int(''.join(c), 16)) for c in zip(addr[0::2], addr[1::2])])
          self.mutex.lock()
          self.xbee.send('remote_at', 
                         frame_id='D', 
                         command='TP', 
                         dest_addr_long=haddr)
          time.sleep(0.1)
          self.xbee.send('remote_at', 
                         frame_id='D', 
                         command='DB', 
                         dest_addr_long=haddr)
          time.sleep(0.1)
          self.xbee.send('remote_at', 
                         frame_id='D', 
                         command='%V', 
                         dest_addr_long=haddr)
          self.mutex.unlock()
        except:
          e = sys.exc_info()[0]
          print str(e)
          #raise
          
      time.sleep(5)

  
  def xbee_discovery_process(self):
    ''' ''' 
    # TODO
   
    
    
  # -----------------------------------------------------------------------------
  def update_orion(self):
    ''' TODO - Description '''
    if self.orion:
      while self.opened:
        for addr in self.devices.keys():
          self.orion.createContext(self.devices[addr].element['type'],
                                   self.devices[addr].element['id'],
                                   self.devices[addr].attributes.values())
          
        time.sleep(1)

  def cygnus_subscribe(self, addr):
    ''' '''
    if self.orion:
      return self.orion.persistDataToHDFS(self.devices[addr].element['type'], 
                                          self.devices[addr].element['id'],
                                          self.devices[addr].attributes.values())
      
  def cygnus_unsubscribe(self, subscriptionId):
    ''' '''
    if self.orion:
      return self.orion.removeHDFSSubscription(subscriptionId)

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# 
class OpenUsbPort(QtCore.QThread):
  ''' '''
  mutex = QtCore.QMutex()
  
  def __init__(self, port, baudrate, parent = None):
    ''' '''
    
    QtCore.QThread.__init__(self)
    self._parent = parent
    self.port = port
    self.baudrate = baudrate
    self.tryingToOpen = True
    self.ser = None
    
    self.msgNotify = QtCore.SIGNAL("msgNotify")
    self.startSendingDatatoOrion = QtCore.SIGNAL("startSendingDatatoOrion")
    
    self.connect(self._parent, QtCore.SIGNAL("closeDevice()"), self.stop)
  
  # --------------------------------------------------------------------------
  def run(self):
    ''' '''
    while self.tryingToOpen:
      try:
        #print 'Opening serial port {0} ({1})...'.format(str(self.port), str(self.baudrate)) # DEBUG
        self.ser = serial.Serial(str(self.port), str(self.baudrate))
        self.mutex.lock()
        self.tryingToOpen = False;
        self.mutex.unlock()
        self.emit(self.startSendingDatatoOrion, self.ser)
        self.emit(self.msgNotify,"Serial Port Open With Success")
        #print 'Success!' # DEBUG
      except serial.SerialException as e:
        #print "ERRO : {0}".format(str(e)) # DEBUG
        self.emit(self.msgNotify,"ERRO : {0}".format(str(e)))
        self.mutex.lock()
        self.tryingToOpen = True;
        self.mutex.unlock()
      except ValueError as e:
        self.mutex.lock()
        self.tryingToOpen = True;
        self.mutex.unlock()
        self.emit(self.msgNotify, "ERRO : {0}".format(str(e)))
        #print "ERRO : {0}".format(str(e)) # DEBUG
      except: # just in case
        e = sys.exc_info()[0]
        self.mutex.lock()
        self.tryingToOpen = True;
        self.mutex.unlock()
        self.emit(self.msgNotify,  "Ops... something went wrong!{0}".format(str(e)))
        #print "Ops... something went wrong!{0}".format(str(e)) # DEBUG
      finally:
        time.sleep(2)
    self.terminate() # This will kill this thread
    
    
  # --------------------------------------------------------------------------
  # SLOTS
  @pyqtSlot()
  def stop(self):
    ''' 
    Stop the running thread if no serial port device found at the moment
    There is no terminate at the close because the run function is responsible 
    for terminating the process at the conclusion of the thread work
    '''
    if self.tryingToOpen:
      self.mutex.lock()
      self.tryingToOpen = False
      self.mutex.unlock()
