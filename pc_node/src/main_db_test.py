#! /usr/bin/python
'''
Created on May 27, 2015

@author: andre
'''

import logging
from database.database_handler import DatabaseHandler
from database.database_manager import DatabaseManager

'''DATABASE MAIN TEST'''

if __name__ == '__main__':
    
    #logging.basicConfig(filename='log/database.log',level=logging.DEBUG)
    #logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
    
    try:   
      
      # Logging format 
      log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
      # File rotation           
      fh = logging.handlers.RotatingFileHandler('~/.log/fresh.log', maxBytes=200, backupCount=5)      
      fh.setLevel(logging.DEBUG)
      fh.setFormatter(log_format)
      # Console handler
      ch = logging.StreamHandler()
      ch.setLevel(logging.DEBUG)
      ch.setFormatter(log_format)
      
      
      root_log = logging.getLogger('') # Root logger      
      root_log.addHandler(fh)
      root_log.addHandler(ch)
      
      db_log = logging.getLogger('db')
      db_log.addHandler(fh)
      db_log.addHandler(ch)
      
      orion_log = logging.getLogger('orion')
      orion_log.addHandler(fh)
      orion_log.addHandler(ch)
      
  
  
    except IOError as e:
      root_log.error('I/O error({0}): {1}'.format(e.errno, e.strerror))
    
    print 'run ...'
    dm = DatabaseManager(None)
    dm.create_database()
