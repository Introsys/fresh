#! /usr/bin/python
'''
Created on May 26, 2015

@author: Andre Silva, Magno Guedes
@mail: andre.silva@introsys.eu, magno.guedes@introsys.eu
'''

import sqlite3
import logging
import os

from exceptions import IOError, Exception
from datetime import date, datetime

class DatabaseManager(object):

  def __init__(self):
    '''
    Constructor
    '''
    
  def create_database (self):
    '''
      WARNING: If the database already exists it will be deleted POSSIBLE DATA LOST
    '''    
    db = None
        
    try:
      print 'create db'
      db = sqlite3.connect('freshdb')
      print 'db created'
      self.logger.info("data base create with success")
      
      
      cursor = db.cursor()
      cursor.execute('pragma foreign_keys=ON') # save keeping enables foreing keys 
      
      ###################################################################
      
      ''' 
      DEVICE SCHEMA
      id             - UNIQUE IDENTIFIER
      description    - TEXT - string value
      id_zone        - INTEGER (FOREIGN KEY)
      rssi           - REAL - float value
      supply_voltage - REAL - float value
      temperature    - REAL - float value
      added_date     - TEXT - ISO8601 string ("YYYY-MM-DD HH:MM:SS.SSS")
      last_update    - TEXT - ISO8601 string ("YYYY-MM-DD HH:MM:SS.SSS")
      is_active      - BOOL
      '''
      cursor.execute('DROP TABLE IF EXISTS device;')
      cursor.execute(''' 
          CREATE TABLE IF NOT EXISTS device(
          id INTEGER PRIMARY KEY NOT NULL,
          description TEXT,
          id_zone INTEGER NOT NULL,
          id_device_buffer INTEGER NOT NULL,
          rssi REAL,
          supply_voltage REAL,
          temperature REAL,
          added_date TEXT,
          last_update TEXT,
          is_active INTEGER,
          FOREIGN KEY(id_zone) REFERENCES zone(id)
          FOREIGN KEY(id_device_buffer) REFERENCES device_buffer(id)
          );        
      ''')
      
      ###################################################################
      
      '''
      ZONE SCHEMA
      id             - UNIQUE IDENTIFIER
      description    - TEXT - string value
      id_culture     - 
      is_active      - BOOL
      '''
      cursor.execute('DROP TABLE IF EXISTS zone;')
      cursor.execute(''' 
          CREATE TABLE IF NOT EXISTS zone(
          id INTEGER PRIMARY KEY NOT NULL, 
          description TEXT,
          id_culture INTEGER NOT NULL,
          is_active INTEGER,
          FOREIGN KEY(id_culture) REFERENCES culture(id)
          );
      ''')
      
      ###################################################################
      
      '''
      CULTURE SCHEMA
      id             - UNIQUE IDENTIFIER
      description    - TEXT - string value
      is_active      - BOOL
      '''
      cursor.execute('DROP TABLE IF EXISTS culture;')
      cursor.execute('''
          CREATE TABLE IF NOT EXISTS culture(
          id INTEGER PRIMARY KEY NOT NULL,
          description TEXT,
          is_active INTEGER
          );
      ''')
      
      ###################################################################
      
      '''
      DEVICE_BUFFER SCHEMA
      id             - UNIQUE IDENTIFIER
      msg            - TEXT - JSON object
      last_update    - TEXT - ISO8601 string ("YYYY-MM-DD HH:MM:SS.SSS")
      ''' 
      cursor.execute('DROP TABLE IF EXISTS device_buffer;')           
      cursor.execute(''' 
          CREATE TABLE IF NOT EXISTS parameter(
          id INTEGER PRIMARY KEY NOT NULL, 
          msg TEXT,
          last_update TEXT
          );
      ''')
      
      
    except sqlite3.Error, e:

      print "Database Error %s:" % e.args[0]
      #sys.exit(1)
        
    finally:
      if db:
          db.close() ## save keeping - close the database connection
  
    
  def destroy_database(self):
    '''this will remove the file from the system'''
    os.remove('data/freshdb')
    
    

  