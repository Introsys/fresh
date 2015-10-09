'''
Created on Sep 4, 2015

@author: andre
'''

import os
import sys
import logging
import shutil
import yaml
import simplejson as json 
import copy
from PyQt4 import QtCore
from PyQt4.Qt import pyqtSlot, pyqtSignal
from PyQt4.QtCore import QObject, QTimer, SLOT, SIGNAL, QMutexLocker, QMutex, Qt, QDir
from PyQt4.QtGui import QStandardItem
from core.CommBroker import CommBroker
from core.Authentication import Authentication
from gui.Preferences import PreferecesDict #@UnusedImport
from database.DatabaseHandler import DatabaseHandler #@UnusedImport
from database.DatabaseManager import DatabaseManager




class AppController(QtCore.QObject):  
  ''' TODO - Description '''
  
  # SIGNALS
  

  
  updateDeviceStatus = pyqtSignal(bool, name ='updateDeviceStatus')
  updateServerStatus = pyqtSignal(bool, name ='updateServerStatus')
  updatePreferencesValues = pyqtSignal(object, name='updatePreferencesValues')
  updateEditRemoveButtonStatus = pyqtSignal(name='updateEditRemoveButtonStatus')
  updateAddButtonStatus = pyqtSignal(name='updateAddButtonStatus')
  showDialogMessage = pyqtSignal(str, str, name='showDialogMessage')
  initiate = pyqtSignal(name='initiate')
  loadLastPreferences = pyqtSignal(name='loadLastPreferences')
  


  # Get the models from the tables
  getMonitorSIM = pyqtSignal(name='getMonitorSIM')
  getAvailableSIM = pyqtSignal(name='getAvailableSIM')
  getSubscribeSIM = pyqtSignal(name='getSubscribeSIM')


  # 
  showDeviceDetails = pyqtSignal(object,name='showDeviceDetails')
  getSelectedDevice = pyqtSignal(name='getSelectedDevice')
  
  

  subscribeRequest = pyqtSignal('QString', name='subscribeRequest')
  unsubscribeRequest = pyqtSignal('QString', 'QString', name='unsubscribeRequest')
  
  



  def __init__(self):
    ''' 
      Constructor - MainWindowControl initialization
    '''
    super(AppController, self).__init__()
    self.setObjectName("AppController")
    self.f_log = logging.getLogger('App') # this can be called in any place
    self.mutex = QMutex()
    self.__commBroker = CommBroker()
    
    # this holds the preferences from the user in memory 
    # the UI holds as well the preferences in the LineEdit object 
    # but his way we decouple the data from the UI and 
    # save read/write cycles to the file system (hard-drive)
    self.preferences = None
    self.token = None
    
    
    # Database manager and handler
    self.dbfile = "freshdb"
    self.databaseManager = DatabaseManager()  
    self.databaseManager.create_database(self.dbfile)
    self.databaseHandler = DatabaseHandler(self.databaseManager.db_file_path)
    
    
    
    # File handling - File Path for configurations files
    self.cfg_path = '{home}/.fresh/cfg'.format(home=QDir.homePath())
    self.cfg_file = QDir.toNativeSeparators('{file_path}/.fresh.cfg'.format(file_path=self.cfg_path)) # this is the runtime file
    self.cfg_file_backup = QDir.toNativeSeparators('{file_path}/.fresh.cfg.bak'.format(file_path=self.cfg_path)) # this is the rollback file
    self.cfg_file_default = QDir.toNativeSeparators('{file_path}/.fresh.cfg.default'.format(file_path=self.cfg_path)) # this is the default file
    try:
      # Create the directory if not exists
      if not QDir(self.cfg_path).exists():
        QDir().mkdir(self.cfg_path)
        self.f_log.debug("Created the Dir {dir}".foramt(dir=self.cfg_path))
    except Exception as e:
      self.f_log.error("ERRO {0}".format(str(e)))
    
    
    self.timerTryStartCommBroker = QTimer()
    self.timerTryStartCommBroker.setSingleShot(True)
    self.timerTryStartCommBroker.setInterval(1000)
    
    
    QObject.connect(self.timerTryStartCommBroker, SIGNAL("timeout()"), self, SLOT("tryStartCommBroker()"))    
    

    QObject.connect(self.__commBroker, SIGNAL("isOrionLive(bool)"), self, SLOT("orionStatus(bool)"))
    QObject.connect(self.__commBroker, SIGNAL("isUsbPortOpen(bool)"), self, SLOT("usbPortStatus(bool)"))
    
    
    QObject.connect(self.__commBroker, SIGNAL("addDevice(QString)"), self, SLOT("addedDevice(QString)"))
    QObject.connect(self.__commBroker, SIGNAL("removeDevice(QString)"), self, SLOT("removedDevice(QString)"))
    QObject.connect(self.__commBroker, SIGNAL("updateDevice(QString)"), self, SLOT("updatedDevice(QString)"))
    
    
    QObject.connect(self, SIGNAL("subscribeRequest(QString)"), self.__commBroker, SLOT("cygnusSubscribeContext(QString)"), Qt.QueuedConnection)
    QObject.connect(self, SIGNAL("unsubscribeRequest(QString, QString)"), self.__commBroker, SLOT("cygnusUnsubscribeContext(QString, QString)"), Qt.QueuedConnection)    
    
    
    QObject.connect(self.__commBroker, SIGNAL("subscribeResult(bool, QString, QString, QString)"), self, SLOT("handleSubscribeResult(bool, QString, QString, QString)"), Qt.QueuedConnection)
    QObject.connect(self.__commBroker, SIGNAL("unsubscribeResult(bool, QString)"), self, SLOT("handleUnsubscribeResult(bool, QString)"), Qt.QueuedConnection)
 

    self.sim_details = None
    self.sim_subscritons = None
    self.sim_available = None
    
    
    self.__detailsItemToDeviceMap = dict()
    self.__subsItemToDeviceMap = dict()
    self.__avItemToDeviceMap = dict()
    
    
    
  # --------------------------------------------------------------------------
    

  def __del__(self):
    self.destroyed.emit(self)
    self.f_log.debug('Object AppController Destroyed')
  # --------------------------------------------------------------------------


  # --------------------------------------------------------------------------
  # Private functions
  # --------------------------------------------------------------------------
  
  
  
  def __loadPreferences(self, source):    
    try:
      # Load config file
      mode = 'r' if os.path.exists(source) else 'w'
      with open(source, mode) as cfg_content:
        cfg = yaml.load(cfg_content)
        if not cfg:        
          raise RuntimeError('Configuration file {file} is empty!'.format(file=source))
        else:
          self.preferences = PreferecesDict(orion_ip = cfg['orion_ip'], 
                                            orion_port = cfg['orion_port'], 
                                            username = cfg['username'], 
                                            password = cfg['password'], 
                                            keystone_ip = cfg['keystone_ip'], 
                                            keystone_port = cfg['keystone_port'], 
                                            keystone_url = cfg['keystone_url'], 
                                            tenant_id = cfg['tenant_id'], 
                                            tenant_name = cfg['tenant_name'], 
                                            domain = cfg['domain'], 
                                            device_port = cfg['device_port'], 
                                            baudrate = cfg['device_baudrate'],
                                            token_path = cfg['token_path'])
          
                                      # TODO - Add new fields here
           
          self.updatePreferencesValues.emit(self.preferences)          
          self.cfg_loded = True
          self.f_log.info("Preferences Loaded")
    except IOError as e:
      self.f_log.error('Error Loading Preferences: {0}'.format(e.strerror))
      self.showDialogMessage.emit('w', "ERROR: {0}".format(e.strerror))
    except Exception as e:
      self.f_log.error('Error Loading Preferences: {0}'.format(e.message))
      self.showDialogMessage.emit('w', 'ERROR: {0}'.format(e.message))
    except:
      e = sys.exc_info()[0] 
      self.f_log.error('Error Loading Preferences: {0}'.format(str(e)))
      self.showDialogMessage.emit('c', "ERROR: {0}".format(str(e)))
      raise
    finally:
      if not self.preferences:
        self.preferences = PreferecesDict()
  # --------------------------------------------------------------------------


  # --------------------------------------------------------------------------
  # SLOTS
  # --------------------------------------------------------------------------
    
    
  @pyqtSlot(name='initiated')
  def initiated(self):
    self.__authBroker = Authentication(username = self.preferences.username,
                                       password = self.preferences.password,
                                       tenant_name = self.preferences.tenantName,
                                       keystone_url = self.preferences.keystoneUrl,
                                       domain = self.preferences.domain)
    
    QObject.connect(self.__authBroker, SIGNAL("tokenReceived(QString)"), self, SLOT("tokenStored(QString)"))
    
    self.__authBroker.getToken() # this will get the token from keystone and keep at self.token
    
    self.getSubscribeSIM.emit()
    self.getAvailableSIM.emit()
    self.getMonitorSIM.emit()

    
    self.timerTryStartCommBroker.start()
    
  
  
  
  # --------------------------------------------------------------------------

  
  
  @pyqtSlot(object, name='savePreferencesToFile')
  def savePreferencesToFile(self, pref):
    ''' '''
    
    try:
      shutil.copy(self.cfg_file, self.cfg_file_backup)
      self.cfg = None
      with open(self.cfg_file, 'r') as cfg_content:
        self.cfg = yaml.load(cfg_content)
        if not self.cfg:        
          self.f_log.error('Problems with the file!')
        else:
          self.cfg['orion_ip'] = str(pref.orionIp)
          self.cfg['orion_port'] = str(pref.orionPort)
          self.cfg['username'] = str(pref.username)
          self.cfg['password'] = str(pref.password)
          self.cfg['keystone_ip'] = str(pref.keystoneIp)
          self.cfg['keystone_port'] = str(pref.keystonePort)
          self.cfg['keystone_url'] = str(pref.keystoneUrl)
          self.cfg['tenant_name'] = str(pref.tenantId)
          self.cfg['tenant_id'] = str(pref.tenantName)
          self.cfg['domain'] = str(pref.domain)
          self.cfg['device_port'] = str(pref.devicePort)
          self.cfg['device_baudrate'] = str(pref.baudrate)
          self.cfg['auto_connect'] = 0
          self.cfg['auto_open_device'] = 0
          self.cfg['token_path'] = str(pref.tokenPath)
          self.preferences = pref
        with open(self.cfg_file, 'w') as cfg_content:
          yaml.safe_dump(self.cfg, cfg_content, default_flow_style=False, allow_unicode=True)
    except IOError as e:
      print "Error {0}".format(e.strerror) # DEBUG
    except:
      e = sys.exc_info()[0] 
      print "Erro {0}".format(str(e)) # Just in case
      raise
  # --------------------------------------------------------------------------
  
  @pyqtSlot(name="loadPreferencesFromLast")
  def loadPreferencesFromLast(self):
    self.__loadPreferences(self.cfg_file)
  # --------------------------------------------------------------------------
  
  @pyqtSlot(name='loadPreferencesFromBackup')
  def loadPreferencesFromBackup(self):
    ''' '''
    self.__loadPreferences(self.cfg_file_backup)
  # --------------------------------------------------------------------------
    
  @pyqtSlot(name='loadPreferencesFromDefault')
  def loadPreferencesFromDefault(self):
    self.__loadPreferences(self.cfg_file_default)
  # --------------------------------------------------------------------------

  @pyqtSlot('QString', name='tokenStored')
  def tokenStored(self, token):
    self.token = token.__str__()
    self.f_log.info('Token: {token}'.format(token=self.token))
  # --------------------------------------------------------------------------
    
  @pyqtSlot(name='tryStartCommBroker')
  def tryStartCommBroker(self):
    if self.token:
      self.__commBroker.open(self.preferences.orionIp, 
                             self.preferences.orionPort, 
                             self.token, 
                             self.preferences.devicePort, 
                             self.preferences.baudrate)
    else:
      self.timerTryStartCommBroker.start()
  # --------------------------------------------------------------------------
  
  @pyqtSlot(object, name="monitorSIMReceived")
  def monitorSIMReceived(self, listModel):
    with QMutexLocker(self.mutex):
      self.sim_details = listModel
  # --------------------------------------------------------------------------
    
  @pyqtSlot(object, name="availableSIMReceived")
  def availableSIMReceived(self, listModel):
    with QMutexLocker(self.mutex):
      self.sim_available = listModel
  # --------------------------------------------------------------------------
  
  @pyqtSlot(object, name="subscribeSIMReceived")
  def subscribeSIMReceived(self, listModel):
    '''
    Table Node Schema
    [0] id  [1] device_addr  [2] device_id  [3] device_type  [4] subscription_timeout             
    [5] subscription_id  [6] description [7] added_date  [8] last_update  [9] is_active             
    '''
    with QMutexLocker(self.mutex):
      self.sim_subscritons = listModel
      subscriptions = self.databaseHandler.list_devices()
      if subscriptions:
        for device in subscriptions:
          _description = device[6]
          _low = device[1][0:7]
          _high = device[1][8:16] 
          item = QStandardItem('{description} - [{addr_low} {addr_high}]'.format(description=_description, addr_low=_low, addr_high=_high))
          item.setCheckable(False)
          item.setEditable(False)
          
          self.sim_subscritons.appendRow(item)
          self.__subsItemToDeviceMap[item] = device[1]
          self.f_log.info('Added the {device} to the subscription device list'.format(device = device[0]))
      
  # --------------------------------------------------------------------------
  
  








  @pyqtSlot(int, name="askedForDeviceDetails")
  def askedForDeviceDetails(self, index):
    with QMutexLocker(self.__commBroker.mutex):
      item = self.sim_details.item(index)
      addr = self.__detailsItemToDeviceMap[item]
      self.showDeviceDetails.emit(copy.deepcopy(self.__commBroker.devices[addr]))
  # --------------------------------------------------------------------------
  











  '''  BREAK   '''
  @pyqtSlot('QString', name='addedDevice')
  def addedDevice(self, _addr):
    with QMutexLocker(self.__commBroker.mutex):
      addr = _addr.__str__()
      dump = json.loads(json.dumps(self.__commBroker.devices[addr].element)) # DEBUG
      _type = dump['id']
      _low = self.__commBroker.devices[addr].id[0:7]
      _high = self.__commBroker.devices[addr].id[8:16] 
      item = QStandardItem('{type} {addr_low} {addr_high}'.format(type=_type, addr_low=_low, addr_high=_high))
      item.setCheckable(False)
      item.setEditable(False)
      
      self.sim_details.appendRow(item)
      self.__detailsItemToDeviceMap[item] = addr
      
      if not self.databaseHandler.get_deivce(addr):
        item = QStandardItem('{type} - [{addr_low} {addr_high}]'.format(type=_type, addr_low=_low, addr_high=_high))
        item.setCheckable(True)
        item.setEditable(False)
        self.sim_available.appendRow(item)
        self.__avItemToDeviceMap[item] = addr
  
  # --------------------------------------------------------------------------
  


  
  @pyqtSlot('QString', name="removedDevice")
  def removedDevice(self, _addr):
    with QMutexLocker(self.__commBroker.mutex):
      addr = _addr.__str__()
      item = [key for key, value in self.__detailsItemToDeviceMap.iteritems() if value == addr][0]
      index = self.sim_details.indexFromItem(item)
      self.sim_details.removeRow(index.row())
      item = [key for key, value in self.__avItemToDeviceMap.iteritems() if value == addr][0]
      if item:
        index = self.sim_available.indexFromItem(item)
        self.sim_available.removeRow(index.row())
          
    self.updatedDevice()
  # --------------------------------------------------------------------------
  
  
  
  
  
  @pyqtSlot(name="updatedDevice")
  @pyqtSlot('QString', name='updatedDevice')
  def updatedDevice(self, _addr = None):
    self.getSelectedDevice.emit()
  # --------------------------------------------------------------------------
  
  
  
  
  
  @pyqtSlot(name="addDeviceSubscriptionToCosmos")
  def addDeviceSubscriptionToCosmos(self):
    ''' 
      TODO - Description
    '''
    with QMutexLocker(self.__commBroker.mutex):
      for index in range(self.sim_available.rowCount()):
        item = self.sim_available.item(index)
        if item.checkState() == Qt.Checked:
          addr = self.__avItemToDeviceMap[item]
          self.subscribeRequest.emit(addr)
          
    
        
  # --------------------------------------------------------------------------

  @pyqtSlot(int ,name="removeDeviceSubscriptionFromCosmos")
  def removeDeviceSubscriptionFromCosmos(self, index):
    '''
      TODO - Description
    '''
    with QMutexLocker(self.__commBroker.mutex):
      item = self.sim_subscritons.item(index)
      addr = self.__subsItemToDeviceMap[item]
      if addr:
        subscriptionID = self.databaseHandler.get_deivce(addr)[4]
        self.unsubscribeRequest.emit(subscriptionID, addr)
    
  # --------------------------------------------------------------------------
  
  @pyqtSlot(int , 'QString',name="editDeviceSubscriptionOnDatabase")
  def editDeviceSubscriptionOnDatabase(self, index, newDescription):
    '''
      TODO - Description
    '''
    item = self.sim_subscritons.item(index)
    addr = self.__subsItemToDeviceMap[item]
    _description = newDescription.__str__()
    if self.databaseHandler.get_deivce(addr):
      self.databaseHandler.update_device_description(addr, _description)
      item.setText('{description} - [{addr_low} {addr_high}]'.format(addr_low = addr[0:7], addr_high = addr[8:16], description = _description))
     
  # --------------------------------------------------------------------------
  
  
  
  
  
  @pyqtSlot(bool, "QString", "QString", "QString", name="handleSubscribeResult")
  def handleSubscribeResult(self, result, device_addr, subscription_id, subscription_duration):
    ''' 
      TODO - Description
    '''
    if result:
      addr = device_addr.__str__()
      item = [key for key, value in self.__avItemToDeviceMap.iteritems() if value == addr][0]
      if item: 
        _description = item.text().__str__()
        newItem = QStandardItem('{description} - [{addr_low} {addr_high}]'.format(addr_low = addr[0:7], addr_high = addr[8:16], description = _description))
        newItem.setCheckable(False)
        newItem.setEditable(False)
                
        with QMutexLocker(self.mutex):
          if not self.databaseHandler.get_deivce(addr):
            with QMutexLocker(self.__commBroker.mutex):
              self.databaseHandler.add_device(addr, 
                                          self.__commBroker.devices[addr].element['id'], 
                                          self.__commBroker.devices[addr].element['type'], 
                                          subscription_id.__str__(), 
                                          subscription_duration.__str__(), 
                                          _description, 
                                          True)
              
          index = self.sim_available.indexFromItem(item)
          self.__avItemToDeviceMap.pop(item)
          self.sim_available.removeRow(index.row())
          self.updateAddButtonStatus.emit()
                
          self.__subsItemToDeviceMap[newItem] = addr
          self.sim_subscritons.appendRow(newItem)
  # --------------------------------------------------------------------------
  

  @pyqtSlot(bool, "QString", name="handleUnsubscribeResult")
  def handleUnsubscribeResult(self, result, device_addr):
    ''' 
      TODO - Description
    '''
    
    addr = device_addr.__str__()
    with QMutexLocker(self.mutex):
      device = self.databaseHandler.get_deivce(addr)
      if result and device:
        self.databaseHandler.remove_device(addr)
        item = [key for key, value in self.__subsItemToDeviceMap.iteritems() if value == addr][0]
        self.__subsItemToDeviceMap.pop(item)
        index = self.sim_available.indexFromItem(item)
        self.sim_subscritons.removeRow(index.row())
        
        with QMutexLocker(self.__commBroker.mutex):
          if self.__commBroker.devices.has_key(addr) and not self.databaseHandler.get_deivce(addr):  
            newItem = QStandardItem('{device_id} - [{addr_low} {addr_high}]'.format(addr_low = addr[0:7], addr_high = addr[8:16], device_id = device[2]))
            newItem.setCheckable(True)
            newItem.setEditable(False)
            self.__avItemToDeviceMap[newItem] = addr
            self.sim_available.appendRow(newItem)
      
    self.updateEditRemoveButtonStatus.emit()
    
  # --------------------------------------------------------------------------  
  
  
  
  @pyqtSlot(bool, name="orionStatus")
  def orionStatus(self, status):
    pass
  
  
  @pyqtSlot(bool, name="usbPortStatus")
  def usbPortStatus(self):
    pass

  
  
  
  
  @pyqtSlot(str, int, name='connectToDevice')
  def connectToDevice(self, port, baudrate):
    pass
  # --------------------------------------------------------------------------


      

# EOF ------------------------------------------------------------------------------------------------------------