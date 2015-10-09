#! /usr/bin/python
'''
Created on May 27, 2015

@author: Andre Silva, Magno Guedes
@mail: andre.silva@introsys.eu, magno.guedes@introsys.eu
'''

import sqlite3
import logging 
from datetime import date, datetime 


class DatabaseHandler(object):
  ''' Todo - Description '''


  def __init__(self, dbfile):
    ''' '''
    self.db = dbfile
    self.d_log = logging.getLogger('DB') # this can be called in any place
  # --------------------------------------------------------------------------
  
    
  def list_devices(self):
      ''' '''
      db = None
      try:
        db = sqlite3.connect(self.db)  # @UndefinedVariable
        cursor = db.cursor()
        cursor.execute('''
            SELECT * 
            FROM nodes
        ''')
        result = cursor.fetchall()        
        return result
      except sqlite3.Error as e:      # @UndefinedVariable
        self.d_log.error("Error listing devices: {0}".format(e.args[0]))
        return 0
      finally:
        if db:
          db.close()
  # --------------------------------------------------------------------------


  def get_deivce(self, device_addr):
    ''' '''
    db = None
    try:
      db = sqlite3.connect(self.db)   # @UndefinedVariable
      cursor = db.cursor()      
      cursor.execute('''
          SELECT * 
          FROM nodes 
          WHERE device_addr = ? ''', (device_addr,))
      result = cursor.fetchone()
      return result
    except sqlite3.Error as e:      # @UndefinedVariable
      self.d_log.error("Error getting device: {0}".format(e.args[0]))
      return 0
    finally:
      if db:
        db.close()
  # --------------------------------------------------------------------------        
      

  def update_device_description(self, device_addr, newDescription = ""):    
    ''' 
    DEVICE SCHEMA
    id                    - UNIQUE IDENTIFIER
    device_addr           - TEXT - unique identifier for the device
    device_id             - TEXT - unique identifier for the device
    device_type           - TEXT - unique identifier for the device
    subscription_id       - TEXT - unique identifier of the subscription
    subscription_timeout  - TEXT - timeout of the subscription
    description           - TEXT - string value
    added_date            - TEXT - ISO8601 string ("YYYY-MM-DD HH:MM:SS.SSS")
    last_update           - TEXT - ISO8601 string ("YYYY-MM-DD HH:MM:SS.SSS")
    is_active             - BOOL
    '''
    db = None
    try:
      db = sqlite3.connect(self.db) # @UndefinedVariable
      cursor = db.cursor()    
      date = datetime.now()
      date.isoformat("T")
      cursor.execute('''
          UPDATE nodes
          SET description= ?, last_update= ?
          WHERE device_addr = ?
      ''',
      (newDescription, date, device_addr))
      db.commit()      
      return 1
    except sqlite3.Error as e:      # @UndefinedVariable
      self.d_log.error("Error updating device: {0}".format(e.args[0]))
      return 0
    finally:
      if db:
        db.close()
  # --------------------------------------------------------------------------
      
  
  def add_device(self, device_addr, device_id, device_type, subscription_id, subscription_timeout, description, is_active):
    ''' '''
    db = None
    try:
      db = sqlite3.connect(self.db) # @UndefinedVariable
      cursor = db.cursor()
      date = datetime.now()
      date.isoformat("T") 
      cursor.execute(''' 
          INSERT INTO nodes (device_addr, device_id, device_type, subscription_id, subscription_timeout, description, added_date, last_update, is_active)
          VALUES(?,?,?,?,?,?,?,?,?)
          ''',
          (device_addr, device_id, device_type, subscription_id,  subscription_timeout, description, date, date, is_active))
      db.commit()
      return 1
    except sqlite3.Error as e:      # @UndefinedVariable
      self.d_log.error("Error adding device: {0}".format(e.args[0]))
      return 0
    finally:
      if db:
        db.close()
  # --------------------------------------------------------------------------


  def remove_device(self, device_addr):
    ''' '''
    db = None
    try:
      db = sqlite3.connect(self.db) # @UndefinedVariable
      cursor = db.cursor()
      date = datetime.now()
      date.isoformat("T")      
      cursor.execute('''
          DELETE 
          FROM nodes
          WHERE device_addr = ?
      ''',
      (device_addr,))
      db.commit()
      return 1
    except sqlite3.Error as e:      # @UndefinedVariable
      self.d_log.error("Error removing device: {0}".format(e.args[0]))
      return 0
    finally:
      if db:
        db.close()
  # --------------------------------------------------------------------------

  
  def dict_factory(self, cursor, row):
    ''' '''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
  # --------------------------------------------------------------------------



''' '''
# EOF ------------------------------------------------------------------------------------------------------------