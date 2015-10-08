'''
Created on Aug 25, 2015

@author: andre
'''
from PyQt4 import QtCore
from datetime import datetime


class Device(QtCore.QObject):
  ''' TODO - Description '''  

  __slots__ = ('id', 'element', 'attributes', 
               'diagnostic', 'attributes_list_complete', 
               'lastUpdateTimestamp', )
  
  def __init__(self, parent=None):
    super(Device, self).__init__(parent)
    self.id = ""
    self.element = dict()
    self.attributes = dict()
    self.diagnostic = dict()
    self.attributes_list_complete = False # this control flag changes when all the attributes are collected
    self.lastUpdateTimestamp = datetime.now()
#EOF