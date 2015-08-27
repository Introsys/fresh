#! /usr/bin/python
'''
Created on May 27, 2015

@author: Andre Silva, Magno Guedes
@mail: andre.silva@introsys.eu, magno.guedes@introsys.eu
'''

import sys #@UnusedImport
import sqlite3
import logging #@UnusedImport
from datetime import date, datetime #@UnusedImport


class DatabaseHandler(object):
  '''
  classdocs
  '''


  def __init__(self, dbfile):
    ''' '''
    self.db = dbfile
    
  # --------------------------------------------------------------------------
  
    
    
  def list_devices(self):
      ''' '''
      db = sqlite3.connect(self.db)  # @UndefinedVariable
      cursor = db.cursor()
      cursor.execute('''
          SELECT * 
          FROM nodes
      ''')
      
      result = cursor.fetchall()
      
      db.close()
      
      return result
  
  # --------------------------------------------------------------------------


  def get_deivce(self, device_id):
      ''' '''
      db = sqlite3.connect(self.db) # @UndefinedVariable
      cursor = db.cursor()
      
      cursor.execute('''
          SELECT * 
          FROM nodes 
          WHERE device_id = ? ''', (device_id,))
      
      result = cursor.fetchone()
      
      return result
      
      db.close()

  
  ''' 
  DEVICE SCHEMA
  id                    - UNIQUE IDENTIFIER
  device_id             - TEXT - unique identifier for the device
  subscription_timeout  - TEXT - timeout of the subscription
  subscription_id       - TEXT - unique identifier of the subscription
  description           - TEXT - string value
  added_date            - TEXT - ISO8601 string ("YYYY-MM-DD HH:MM:SS.SSS")
  last_update           - TEXT - ISO8601 string ("YYYY-MM-DD HH:MM:SS.SSS")
  is_active             - BOOL
  '''
  def update_device_description(self, device_id, newDescription = ""):
      ''' '''
      
      db = sqlite3.connect(self.db) # @UndefinedVariable
      cursor = db.cursor()    
      
      date = datetime.now()
      date.isoformat("T")
      
      cursor.execute('''
          UPDATE nodes
          SET description= ?, last_update= ?
          WHERE device_id = ?
      ''',
      (newDescription, date, device_id))
      
      db.commit()
      db.close()


      
  def add_device(self, device_id, subscription_id, subscription_timeout, description, is_active):
      ''' '''
      db = sqlite3.connect(self.db) # @UndefinedVariable
      cursor = db.cursor()
      
      date = datetime.now()
      date.isoformat("T") 
      
      cursor.execute(''' 
          INSERT INTO nodes (device_id, subscription_id, subscription_timeout, description, added_date, last_update, is_active)
          VALUES(?,?,?,?,?,?,?)
          ''',
          (device_id, subscription_id,  subscription_timeout, description, date, date, is_active))
      

      db.commit()
      db.close()


  def remove_device(self, device_id):
      ''' '''
      db = sqlite3.connect(self.db) # @UndefinedVariable
      cursor = db.cursor()
      
      date = datetime.now()
      date.isoformat("T")
      
      cursor.execute('''
          DELETE 
          FROM nodes
          WHERE device_id = ?
      ''',
      (device_id,))
      
      db.commit()
      db.close()


  def dict_factory(self, cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# TODO  
###############################################################################
#     
#     def list_zones(self):
#         ''' '''
#         db = sqlite3.connect('freshdb') # @UndefinedVariable
#         cursor = db.cursor()
#         
#         cursor.execute('''
#             
#         ''')
#         
#         db.close()
# 
# 
#     def add_zone(self):
#         ''' '''
#         db = sqlite3.connect('freshdb') # @UndefinedVariable
#         cursor = db.cursor()
#         
#         cursor.execute('''
#             
#         ''')
#         
#         db.close()
# 
# 
#     def update_zone(self):
#         ''' '''
#         db = sqlite3.connect('freshdb') # @UndefinedVariable
#         cursor = db.cursor()
#         
#         cursor.execute('''
#             
#         ''')
#         
#         db.close()
# 
# 
#     def remove_zone(self):
#         ''' '''
#         db = sqlite3.connect('freshdb') # @UndefinedVariable
#         cursor = db.cursor()
#         
#         cursor.execute('''
#             
#         ''')
#         
#         db.close()
###############################################################################