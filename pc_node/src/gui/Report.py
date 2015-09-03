'''
Created on Aug 24, 2015

@author: msg
'''
from PyQt4 import QtCore
from PyQt4.Qt import pyqtSlot
from PyQt4.QtGui import QWidget, QGridLayout, QComboBox, QPushButton

import os
import time
import datetime
import json

import pyqtgraph as pg
import numpy as np

from communication.CosmosClient import CosmosClient


#from pyqtgraph.flowchart import Flowchart, Node
#import pyqtgraph.flowchart.library as fclib
#from pyqtgraph.flowchart.library.common import CtrlNode

import pyhs2


#------------------------------------------------------------------------------

class Ui_WidgetReport(QWidget):

  def __init__(self, parent = None):
    ''' '''
    super(Ui_WidgetReport, self).__init__()
    self.__parentWidget = parent
    self.helper = Ui_WidgetReportHelper(self)

    self.cosmos_cli = CosmosClient()
    
    #TODO: these should be in the app configuration tool
    self.sensor_list = [('zone', 'zone1')] #Tuple(sensor_type, sensor_name)
    webhdfs_url = 'http://130.206.80.46:14000/webhdfs/v1'
    auth_url = 'https://130.206.80.46:13000/cosmos-auth/v1'
    local_filepath = os.environ['HOME']+os.sep+'.fresh'+os.sep+'history'
    username = ''
    password = ''
    cosmos_user = ''
    serv = 'fresh'
    servpath = 'fresh'
    #--------------------------
    
    self.entity_list = dict()
    
    self.cosmos_cli.username = username
    self.cosmos_cli.password = password
    self.cosmos_cli.webhdfs_url = webhdfs_url
    self.cosmos_cli.auth_url = auth_url
    self.cosmos_cli.hdfs_username = cosmos_user
    self.cosmos_cli.hdfs_filepath = '/'+serv+'_serv/'+servpath+'_servpath/'
    self.cosmos_cli.local_filepath = local_filepath
    
    self.setupUi(self)
    
    
    
    
    #self.helper.connect_file()
    #self.helper.connect()
    #self.helper.connect_webhdfs()
    
    #self.db_zone1_cols = []
    #self.db_zone1_rows = []
    #self.db_zone2_cols = []
    #self.db_zone2_rows = []

  #----------------------------------------------------------------------------

  def setupUi(self, WidgetNetMang):
    
      layout = QGridLayout()
      self.setLayout(layout)

      #self.axis = MyStringAxis(orientation='bottom')
      self.axis = DateAxis(orientation='bottom')
      self.widget_plot = pg.PlotWidget(axisItems={'bottom': self.axis})

      self.combo_zone = QComboBox()
      for (_, sensor) in self.sensor_list:
        self.combo_zone.addItem(sensor)

      self.combo_sensor = QComboBox()

      self.button_refresh = QPushButton()
      self.button_refresh.setText('Refresh')
      
      #(QWidget, row, column, rowSpan, columnSpan)
      layout.addWidget(self.widget_plot, 0, 0, 1, 6)      
      layout.addWidget(self.combo_zone, 1, 0, 1, 2)
      layout.addWidget(self.combo_sensor, 1, 2, 1, 2)
      layout.addWidget(self.button_refresh, 1, 5, 1, 1)
      
      
      self.combo_zone.currentIndexChanged['QString'].\
        connect(self.handle_combo_zone_changed)
      self.combo_sensor.currentIndexChanged['QString'].\
        connect(self.handle_combo_sensor_changed)
      self.button_refresh.clicked.\
        connect(self.handle_button_refresh_clicked)
  
  #----------------------------------------------------------------------------
  
  @pyqtSlot('QString')
  def handle_combo_zone_changed(self, text):
    
    if str(text) == '':
      return
    
    self.combo_sensor.blockSignals(True)
    self.combo_sensor.clear()
    for e in self.entity_list[str(text)]:
      self.combo_sensor.addItem(e)
    self.combo_sensor.setCurrentIndex(0)
    self.combo_sensor.blockSignals(False)
    self.combo_sensor.currentIndexChanged['QString'].emit(self.combo_sensor.currentText())
  
  #----------------------------------------------------------------------------
  
  @pyqtSlot('QString')
  def handle_combo_sensor_changed(self, text):
    
    if str(text) == '':
      return
    
    print str(text)
    
    dates = []
    values = []
    
    found = False
    for (s_type,s_name) in self.sensor_list:
      if s_name == str(self.combo_zone.currentText()):
        self.cosmos_cli.local_filename = s_name+'_'+s_type+'.txt'
        found = True
        break;
    
    if not found:
      return
    
    self.cosmos_cli.readHistoryFromFile()
    
    for s in self.cosmos_cli.history.split('\n'):
      try:
        j = json.loads(s)
        try:
          value = j[str(text)]
          date = j['recvTime'].split('.')[0]
          values.append(float(value))
          print date
          print time.mktime(datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").timetuple())
          dates.append(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").timetuple()))
          #dates.append(date.split('T')[0]+'\n'+(date.split('T')[1]).split('.')[0])
        except:
          pass
      except:
        pass

    self.widget_plot.clear()
    #xdates = dict(zip(range(len(dates)),dates))
    #self.axis.set_dict(xdates)
    #self.widget_plot.plot(x=xdates.keys(), y=values, symbol='o')
    self.widget_plot.plot(x=dates, y=values, symbol='o')
    
    
    
    """
      
      print index
      
      values = []
      dates = []
      self.widget_plot.clear()
      
      if self.combo_zone.currentText() == 'Zone 1':
          for i in self.helper.db_zone1_rows:
              values.append(float(i[index*2+1]))
              dates.append(i[0].split('T')[0]+'\n'+(i[0].split('T')[1]).split('.')[0])
          #dates = np.arange(len(self.helper.db_zone1_rows)) #TODO Date?
          
          xdates = dict(zip(range(len(dates)),dates))
          self.axis.set_dict(xdates)
          self.widget_plot.plot(x=xdates.keys(), y=values, symbol='o')
      elif self.combo_zone.currentText() == 'Zone 2':
          for i in self.helper.db_zone2_rows:
              values.append(float(i[index*2+1]))
              dates.append(i[0].split('T')[0]+'\n'+(i[0].split('T')[1]).split('.')[0])
          #dates = np.arange(len(self.helper.db_zone2_rows)) #TODO Date?
          xdates = dict(zip(range(len(dates)),dates))
          self.axis.set_dict(xdates)
          self.widget_plot.plot(x=xdates.keys(), y=values, symbol='o')
      pass
  

  """        
  
  #----------------------------------------------------------------------------
  
  @pyqtSlot()
  def handle_button_refresh_clicked(self):
    
    """get the files from cosmos and stores them locally"""
    
    self.entity_list.clear()
    
    for (s_type, s_name) in self.sensor_list:
      self.entity_list[s_name] = dict()
      self.cosmos_cli.hdfs_filename = s_name+'_'+s_type+'/'+s_name+'_'+s_type+'.txt'
      self.cosmos_cli.local_filename = s_name+'_'+s_type+'.txt'
      try:
        self.cosmos_cli.getFileContent()
      except NameError as e:
        print e
        return
      try:
        self.cosmos_cli.writeHistoryToFile()
      except NameError as e:
        print e
        return
      
      self.entity_list[s_name].clear()
      for s in self.cosmos_cli.history.split('\n'):
        try:
          for k in json.loads(s).keys():
            if 'md' not in k and 'recv' not in k and 'RTC' not in k:
              self.entity_list[s_name][k] = ''
        except:
          pass
    
    self.combo_zone.clear()
    self.combo_sensor.clear()
    
    for e in self.entity_list:
      self.combo_zone.addItem(e)
      "print self.entity_list[e]"
      
      
    
    
    #self.combo_sensor.clear()
    #for e in self.entity_list:
    #  self.combo_sensor.addItem(e)
      
      
      
      
      
      
    
    print "refresh"
    
#==============================================================================

class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        rng = max(values)-min(values)
        #if rng < 120:
        #    return pg.AxisItem.tickStrings(self, values, scale, spacing)
        if rng < 3600*24:
            string = '%Y-%m-%d\n%H:%M:%S'
            label1 = '%b %d -'
            label2 = ' %b %d, %Y'
        elif rng >= 3600*24 and rng < 3600*24*30:
            string = '%Y-%m-%d\n%H:%M:%S'
            label1 = '%b - '
            label2 = '%b, %Y'
        elif rng >= 3600*24*30 and rng < 3600*24*30*24:
            string = '%Y-%m-%d\n%H:%M:%S'
            label1 = '%Y -'
            label2 = ' %Y'
        elif rng >=3600*24*30*24:
            string = '%Y-%m-%d\n%H:%M:%S'
            label1 = ''
            label2 = ''
        for x in values:
            try:
                strns.append(time.strftime(string, time.localtime(x)))
            except ValueError:  ## Windows can't handle dates before 1970
                strns.append('')
        try:
            label = time.strftime(label1, time.localtime(min(values)))+time.strftime(label2, time.localtime(max(values)))
        except ValueError:
            label = ''
        #self.setLabel(text=label)
        return strns

#==============================================================================

class MyStringAxis(pg.AxisItem):
  
  def __init__(self, *args, **kwargs):
    self.set_dict(dict())
    pg.AxisItem.__init__(self, *args, **kwargs)
    
  def set_dict(self, xdict):
    self.x_values = np.asarray(xdict.keys())
    self.x_strings = xdict.values()
  
  def tickStrings(self, values, scale, spacing):
    strings = []
    for v in values:
      # vs is the original tick value
      vs = v * scale
      # if we have vs in our values, show the string otherwise show nothing
      if vs in self.x_values:
        # Find the string with x_values closest to vs
        vstr = self.x_strings[np.abs(self.x_values-vs).argmin()]
      else:
        vstr = ""
        strings.append(vstr)
    return strings

#==============================================================================
  
class Ui_WidgetReportHelper(QtCore.QThread):
    
    def __init__(self, parent = None):
      #super(Ui_WidgetReportHelper, self).__init__()
      QtCore.QThread.__init__(self)
      self.parentWidget = parent      
    
    def __del__(self):
      self.wait()
    
    def run(self):
        print "something"
        self.connect()
        #self.connect_file()
        
    @pyqtSlot()
    def hive_connect(self):
        
        self.start()
      
    def connect(self):
      print "I'm running but will hang some time. Please be patient..."
      
  
      with pyhs2.connect(host='cosmos.lab.fi-ware.org',
                         port=10000,
                         authMechanism="PLAIN",
                         user='',
                         password='',
                         database='default') as conn:
          with conn.cursor() as self.cur:
              #Show databases
              #print cur.getDatabases()

              #Execute query
              self.cur.execute("select * from andre_silva_fresh_serv_fresh_servpath_zone1_zone_column")
              self.db_zone1_cols = []
              for i in self.cur.getSchema():
                  if("_md" not in i['columnName'].split('.')[1] and
                     "recv" not in i['columnName'].split('.')[1]):
                      self.db_zone1_cols.append(i['columnName'].split('.')[1])
              #print self.db_zone1_cols
              self.db_zone1_rows = self.cur.fetch()
              #print self.db_zone1_rows
              
              self.cur.execute("select * from andre_silva_fresh_serv_fresh_servpath_zone2_zone_column")
              self.db_zone2_cols = []
              for i in self.cur.getSchema():
                  if("_md" not in i['columnName'].split('.')[1] and
                     "recv" not in i['columnName'].split('.')[1]):
                      self.db_zone2_cols.append(i['columnName'].split('.')[1])
              #print self.db_zone2_cols
              self.db_zone2_rows = self.cur.fetch()
              #print self.db_zone2_rows

      print "Whoa! I have a database!"
      
    def connect_file(self):
      print "I'm running but will hang some time. Please be patient..."
      
#       f = open('/home/andre/CodeWorkspaces/eclipsemars/fresh-pcnode/src/gui/cosmos_dump.txt', 'r')
#       self.db_zone1_rows = [x.split('\t') for x in f.readlines()]
      
      with open('/home/andre/CodeWorkspaces/eclipsemars/fresh-pcnode/src/gui/cosmos_dump.txt', 'r') as f:
        self.db_zone1_rows = [x.split('\t') for x in f.readlines()]

      print "Whoa! I have a database!"
