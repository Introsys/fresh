#! /usr/bin/python

import serial
import json
import time

from threading import Thread

from PyQt4.QtCore import QObject, SIGNAL

from xbee import ZigBee

import orion_client

class Gateway(QObject):

  def __init__(self, port, baudrate, parent=None):
    
    super(Gateway, self).__init__(parent)
    
    try:
      print 'Opening serial port %s (%d)...'%(port, baudrate)
      self.ser = serial.Serial(port, baudrate)
      print 'Success!'
      print 'Getting access to ZigBee module...'
      self.xbee = ZigBee(self.ser, callback=self.read_xbee, escaped=True)
      print 'Success!'
    except:
      print "Ops... something went wrong!"
      raise
      
    self.opened = True;
    
    self.devices = dict()
    
    t_diag = Thread(target=self.query_remote_diag)
    t_diag.start()
    
    t_orion = Thread(target=self.update_orion)
    t_orion.start()
    
      
  def read_xbee(self, data):
    
    print data
    addr = data['source_addr_long'].encode('hex')
    
    if data['id'] =='rx':
      if 'element' in data['rf_data']:
        if not self.devices.has_key(addr):
          jsonObj = json.loads(data.get('rf_data'))
          newDevice = Device()
          newDevice.element = jsonObj['element']
          self.devices[addr] = newDevice
          self.emit(SIGNAL('newDevice'))
      
      elif 'attribute' in data['rf_data'] and self.devices.has_key(addr):
        jsonObj = json.loads(data.get('rf_data'))
        self.devices[addr].attributes[jsonObj['attribute']['name']] = jsonObj['attribute']
    
    elif data['id'] == 'remote_at_response' and self.devices.has_key(addr):
      if data['frame_id'] == 'D': #diagnostic msgs
        if data['command'] == str('TP'):
          self.devices[addr].diagnostic['Temp'] = int(data['parameter'].encode('hex'), 16)
        elif str(data['command']) == 'DB':
          self.devices[addr].diagnostic['Sign'] = int(data['parameter'].encode('hex'), 16)
        elif str(data['command']) == '%V':
          self.devices[addr].diagnostic['Volt'] = (int(data['parameter'].encode('hex'), 16))*(1200/1024)
        
        
      
    
    #if 'at_response' in data.values():
    #print 'Temperature: %s C'%(data.get('parameter').encode('hex'))
    #print '64-bit source addr: %s' %data.get('source_addr_long').encode('hex')
    #print '16-bit source addr: %s' %data.get('source_addr').encode('hex')
    #print 'RF data: %s' %data.get('rf_data').replace('\n', '')
    
    '''
    while True:
      print 'listening to xbee'
      try:
        res = self.xbee.wait_read_frame()
        print res['source_addr_long']
      except KeyboardInterrupt:
        print 'failed'
        time.sleep(1)
        self.ser.close()
        break
    '''
  
  def query_remote_diag(self):
    
    while self.opened:
      for addr in self.devices.keys():
        try:
          haddr = ''.join([chr(int(''.join(c), 16)) for c in zip(addr[0::2], addr[1::2])])
          self.xbee.send('remote_at', frame_id='D', command='TP', dest_addr_long=haddr)
          time.sleep(0.1)
          self.xbee.send('remote_at', frame_id='D', command='DB', dest_addr_long=haddr)
          time.sleep(0.1)
          self.xbee.send('remote_at', frame_id='D', command='%V', dest_addr_long=haddr)
        except:
          pass
      time.sleep(5)
  
  def update_orion(self):
    
    while self.opened:
      for addr in self.devices.keys():
        
        orion_client.createContext(self.devices[addr].element['type'],
                                   self.devices[addr].element['id'],
                                   self.devices[addr].attributes.values())
      time.sleep(1)
  
  def close(self):
    
    self.opened = False
    self.xbee.halt()
    self.ser.close()
  
class Device(QObject):
  
  def __init__(self, parent=None):
    
    super(Device, self).__init__(parent)
    
    self.element = dict()
    self.attributes = dict()
    self.diagnostic = dict()
    
    