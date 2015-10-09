#! /usr/bin/python
'''
Created on May 26, 2015

@author: Andre Silva, Magno Guedes
@mail: andre.silva@introsys.eu, magno.guedes@introsys.eu
'''

import sqlite3 
import logging
from PyQt4.QtCore import QDir, QFile


class DatabaseManager(object):

  def __init__(self):
    ''' Constructor '''
    
    self.dbfile = None
    self.db_file_path = None
    self.d_log = logging.getLogger('DB') # this can be called in any place
  # --------------------------------------------------------------------------


  def create_database (self, dbfile = "freshdb"):
    ''' This function will create the database and directory if they not exist
    return 0 if created with success
    return 1 if error creating database
    return 2 if database already exists '''
    
    db = None
    self.db_path = QDir.toNativeSeparators("{home}/.fresh/data".format(home=QDir.homePath()).__str__())
    self.db_file_path = QDir.toNativeSeparators("{file_path}/{file}".format(file_path=self.db_path, file=dbfile)).__str__()
    
    # Create the directory if not exists
    if not QDir(self.db_path).exists():
      QDir.mkdir(self.db_path)
      self.d_log.debug('Created the Dir {dir}'.format(dir=self.db_path))
      
    # Create the database file
    if not QFile(self.db_file_path).exists():
      self.d_log.debug("Created database file {file}".format(file=self.db_file_path))
      try:
        self.d_log.debug("Creating database")
        db = sqlite3.connect(self.db_file_path) # @UndefinedVariable
        cursor = db.cursor()
        cursor.execute('pragma foreign_keys=ON') # save keeping enables foreing keys 
        ''' 
        DEVICE SCHEMA
        id                    - UNIQUE IDENTIFIER
        device_addr           - TEXT - unique identifier for the device
        device_id             - TEXT - Symbolic identifier
        device_type           - TEXT - device type
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
            device_addr TEXT NOT NULL,
            device_id TEXT NOT NULL,
            device_type TEXT NOT NULL,
            subscription_id TEXT NOT NULL,
            subscription_timeout TEXT NOT NULL,
            description TEXT,
            added_date TEXT,
            last_update TEXT,
            is_active INTEGER
            )''')
        
        db.commit()
        self.d_log.info("Database created with success")
        return 1 # created with success
      except sqlite3.Error as e:        # @UndefinedVariable
        self.d_log.error("Database Error: {0}".foramt(e.args[0]))
        return 0 # Error creating database
      finally:
        if db:
          db.close() ## save keeping - close the database connection
    else:
      self.d_log.debug("Database already exists")
      return 2 # database already exists
# --------------------------------------------------------------------------
  
  
  def destroy_database(self, dbfile="freshdb"):
    ''' this will remove the file from the system the directory will still exist '''
    db_file_path = QDir.toNativeSeparators("{file_path}/{file}".format(file_path=self.db_path, file=dbfile)).__str__()
    try:
      return QFile(db_file_path).remove()
    except:
      return 0
  # --------------------------------------------------------------------------
    

# EOF ------------------------------------------------------------------------------------------------------------