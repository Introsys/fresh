'''
Created on Aug 25, 2015

@author: andre
'''
from PyQt4 import QtCore


class Device(QtCore.QObject):
  ''' TODO - Description '''  
  
  def __init__(self, parent=None):
    super(Device, self).__init__(parent)
    self.id = ""
    self.element = dict()
    self.attributes = dict()
    self.diagnostic = dict()
    self.control_flag = True # this control flag changes when all the attributes are collected
    self.attributes_list_complete = False # all attributes have been collected
    
#EOF