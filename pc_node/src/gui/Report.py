'''
Created on Aug 24, 2015

@author: msg
'''
from PyQt4 import QtCore, QtGui
from pyqtgraph.flowchart import Flowchart, Node
import pyqtgraph.flowchart.library as fclib
from pyqtgraph.flowchart.library.common import CtrlNode
import pyqtgraph as pg
import numpy as np
import pyhs2
import simplejson as json
import time
from PyQt4.Qt import QObject, QStringList, pyqtSlot
from gevent.core import SIGNAL

class Ui_WidgetReport(QtGui.QWidget):

  def __init__(self, parent = None):
    ''' '''
    super(Ui_WidgetReport, self).__init__()
    self.helper = Ui_WidgetReportHelper(self)
    self.setupUi(self)
    self.__parentWidget = parent
    
    self.helper.connect_file()
    
    #self.db_zone1_cols = []
    #self.db_zone1_rows = []
    #self.db_zone2_cols = []
    #self.db_zone2_rows = []


  def setupUi(self, WidgetNetMang):
      layout = QtGui.QGridLayout()
      self.setLayout(layout)

      #Date Plot      
      #axis = DateAxis(orientation='bottom')
      self.axis = MyStringAxis(orientation='bottom')
      self.widget_plot = pg.PlotWidget(axisItems={'bottom': self.axis})
      layout.addWidget(self.widget_plot, 0, 0, 1, 2)
      
      self.combo_zone = QtGui.QComboBox()
      self.combo_sensor = QtGui.QComboBox()
      layout.addWidget(self.combo_zone, 1, 0, 1, 1)
      layout.addWidget(self.combo_sensor, 1, 1, 1, 1)
          
      self.combo_zone.addItem('Zone 1')
      self.combo_zone.addItem('Zone 2')
      
      self.combo_zone.currentIndexChanged['QString'].connect(self.handle_combo_zone_changed)
      self.combo_sensor.currentIndexChanged['int'].connect(self.handle_combo_sensor_changed)

      #w2.plot(x=dates, y=values, symbol='o')
      #x=np.array([0,1,2,3,4,5,6,7])
      #y=np.array([0,1,2,3,4,5,6,7])
      #w1.plot(x,y)

      """
      v1 = pg.ImageView()
      layout.addWidget(v1, 0, 1)
      v2 = pg.ImageView()
      layout.addWidget(v2, 1, 1)
      
      ## generate random input data
      data = np.random.normal(size=(100,100))
      data = 25 * pg.gaussianFilter(data, (5,5))
      data += np.random.normal(size=(100,100))
      data[40:60, 40:60] += 15.0
      data[30:50, 30:50] += 15.0
      #data += np.sin(np.linspace(0, 100, 1000))
      #data = metaarray.MetaArray(data, info=[{'name': 'Time', 'values': np.linspace(0, 1.0, len(data))}, {}])

      ## Set the raw data as the input value to the flowchart
      fc.setInput(dataIn=data)
      """

  def handle_combo_zone_changed(self, text):
      self.combo_sensor.clear()
      if text == 'Zone 1':
          print 'Zone 1'
          for i in self.helper.db_zone1_cols:
              self.combo_sensor.addItem(i)
      elif text == 'Zone 2':
          print 'Zone 2'
          for i in self.helper.db_zone2_cols:
              self.combo_sensor.addItem(i)


  def handle_combo_sensor_changed(self, index):
      
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
  

           


class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        rng = max(values)-min(values)
        #if rng < 120:
        #    return pg.AxisItem.tickStrings(self, values, scale, spacing)
        if rng < 3600*24:
            string = '%H:%M:%S'
            label1 = '%b %d -'
            label2 = ' %b %d, %Y'
        elif rng >= 3600*24 and rng < 3600*24*30:
            string = '%d'
            label1 = '%b - '
            label2 = '%b, %Y'
        elif rng >= 3600*24*30 and rng < 3600*24*30*24:
            string = '%b'
            label1 = '%Y -'
            label2 = ' %Y'
        elif rng >=3600*24*30*24:
            string = '%Y'
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
      
class MyStringAxis(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)
        
    def set_dict(self, xdict):
        self.x_values = np.asarray(xdict.keys())
        self.x_strings = xdict.values()
        

    def tickStrings(self, values, scale, spacing):
        strings = []
        for v in values:
            # vs is the original tick value
            vs = v * scale
            # if we have vs in our values, show the string
            # otherwise show nothing
            if vs in self.x_values:
                # Find the string with x_values closest to vs
                vstr = self.x_strings[np.abs(self.x_values-vs).argmin()]
            else:
                vstr = ""
            strings.append(vstr)
        return strings
      
#class Ui_WidgetReportHelper(QtCore.QObject):
#    def __init__(self, parent = None):
#      super(Ui_WidgetReportHelper, self).__init__()
#      self.parentWidget = parent
      
class Ui_WidgetReportHelper(QtCore.QThread):
    
    db_zone1_cols = ['temp_1', 'temp_2', 'humidity']
    db_zone2_cols = ['temp_1', 'temp_2', 'humidity']
    db_zone1_rows = []
    db_zone2_rows = []
    
    
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
                         user='andre.silva',
                         password='Andr=#fi0',
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
