#! /usr/bin/python
'''
Created on May 15, 2015

@author: Magno Guedes, Andre Silva
@mail: magno.guedes@introsys.eu, andre.silva@introsys.eu
'''
import logging
import sys
import os
from PyQt4 import QtGui
from logging import handlers #@UnusedImport
from gui.MainWindow import Ui_MainWindow


# -----------------------------------------------------------------------------
# MAIN
if __name__ == '__main__':

    # --------------------------------
  try:   
    
    # Logging format 
    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # File rotation
    filename = '~/.log/fresh.log'
    if not os.path.exists(os.path.dirname(filename)):
      os.makedirs(os.path.dirname(filename))
      with open(filename, "w") as f:
        f.write("# LOG FILE #")
    
    fh = logging.handlers.RotatingFileHandler(filename, 
                                              maxBytes=200, 
                                              backupCount=5)      
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
    print 'I/O error({0}): {1}'.format(e.errno, e.strerror)
    #raise
  
  # --------------------------------
  

  
  app = QtGui.QApplication(sys.argv)
  ex = Ui_MainWindow()
  ex.show()
  sys.exit(app.exec_())
  
  
# EOF