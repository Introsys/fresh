#! /usr/bin/python
'''
Created on May 26, 2015

@author: Andre Silva, Magno Guedes
@mail: andre.silva@introsys.eu, magno.guedes@introsys.eu
'''

import sqlite3 
import logging #@UnusedImport
import os
import sys
from exceptions import IOError, Exception  #@UnusedImport
from datetime import date, datetime #@UnusedImport

class DatabaseManager(object):

  def __init__(self):
    '''
    Constructor
    '''
    self.dbfile = None
    
  def create_database (self, dbfile = "freshdb"):
    '''
      WARNING: If the database already exists it will be deleted POSSIBLE DATA LOST
    '''    
    db = None
    self.dbfile = dbfile
        
    try:
      print 'create db'
      db = sqlite3.connect(dbfile) # @UndefinedVariable
      print 'db created'
      
      cursor = db.cursor()
      cursor.execute('pragma foreign_keys=ON') # save keeping enables foreing keys 
      
      ###################################################################
      
      
      # id_zone            - INTEGER (FOREIGN KEY)
      # id_zone INTEGER NOT NULL,
      ''' 
      DEVICE SCHEMA
      id                    - UNIQUE IDENTIFIER
      device_id             - TEXT - unique identifier for the device
      subscription_id       - TEXT - unique identifier of the subscription
      subscription_timeout  - TEXT - timeout of the subscription
      description           - TEXT - string value
      added_date            - TEXT - ISO8601 string ("YYYY-MM-DD HH:MM:SS.SSS")
      last_update           - TEXT - ISO8601 string ("YYYY-MM-DD HH:MM:SS.SSS")
      is_active             - BOOL
      '''
      cursor.execute('DROP TABLE IF EXISTS nodes;')
      cursor.execute(''' 
          CREATE TABLE IF NOT EXISTS nodes(
          id INTEGER PRIMARY KEY NOT NULL,
          device_id TEXT NOT NULL,
          subscription_id TEXT NOT NULL,
          subscription_timeout TEXT NOT NULL,
          description TEXT,
          added_date TEXT,
          last_update TEXT,
          is_active INTEGER
          )''')
      
      db.commit()
      
    except sqlite3.Error, e:        # @UndefinedVariable
      print "Database Error %s:" % e.args[0]
      sys.exit(1)
        
    finally:
      if db:
        db.close() ## save keeping - close the database connection
        print "database created"
  
  
  def destroy_database(self):
    '''this will remove the file from the system'''
    os.remove('data/{0}'.format(self.dbfile))
    
    

  