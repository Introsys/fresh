'''
Created on Aug 24, 2015

@author: msg
'''
from PyQt4 import QtCore
from PyQt4.Qt import pyqtSlot
from PyQt4.QtGui import QWidget, QStackedWidget, QGridLayout, QScrollArea
from PyQt4.QtGui import QFrame, QGroupBox, QLabel, QPixmap, QFileDialog, QInputDialog
from PyQt4.QtGui import QLineEdit, QTextEdit, QComboBox, QPushButton

import os
import time
from z3c.rml import rml2pdf
import datetime
import preppy
import json



import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np

from communication.CosmosClient import CosmosClient
from communication.EmailClient import EmailClient


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
    webhdfs_url = 'http://130.206.80.46:14000/webhdfs/v1'
    auth_url = 'https://130.206.80.46:13000/cosmos-auth/v1'
    local_filepath = os.environ['HOME']+os.sep+'.fresh'+os.sep+'history'
    username = 'user@cosmos'
    password = ''
    cosmos_user = 'user'
    serv = 'fresh'
    servpath = 'fresh'
    #--------------------------

    self.sensor_list = [('zone', 'zone1')] #Tuple(sensor_type, sensor_name)
    self.entity_list = dict()
    
    self.cosmos_cli.username = username
    self.cosmos_cli.password = password
    self.cosmos_cli.webhdfs_url = webhdfs_url
    self.cosmos_cli.auth_url = auth_url
    self.cosmos_cli.hdfs_username = cosmos_user
    self.cosmos_cli.hdfs_filepath = '/'+serv+'_serv/'+servpath+'_servpath/'
    self.cosmos_cli.local_filepath = local_filepath
    
    self.rep_template = preppy.getModule('reportTemplate.prep')
    
    self.setupUi(self)

  #----------------------------------------------------------------------------

  def setupUi(self, WidgetNetMang):
    
    #This view contains a stacked widget with two pages
    
    #1st page plots the graphic:
    
    layout_plot = QGridLayout()
    self.widget_page_plot = QWidget()
    self.widget_page_plot.setLayout(layout_plot)    
    self.axis = DateAxis(orientation='bottom')
    self.widget_plot = pg.PlotWidget(axisItems={'bottom': self.axis})
    self.combo_zone = QComboBox()
    for (_, sensor) in self.sensor_list: self.combo_zone.addItem(sensor)
    self.combo_sensor = QComboBox()
    self.button_refresh = QPushButton()
    self.button_refresh.setText('Refresh')
    self.button_report = QPushButton()
    self.button_report.setText('Report')
    
    #(QWidget, row, column, rowSpan, columnSpan)
    layout_plot.addWidget(self.widget_plot, 0, 0, 1, 5)      
    layout_plot.addWidget(self.combo_zone, 1, 0, 1, 1)
    layout_plot.addWidget(self.combo_sensor, 1, 1, 1, 1)
    layout_plot.addWidget(self.button_report, 1, 3, 1, 1)
    layout_plot.addWidget(self.button_refresh, 1, 4, 1, 1) 
    
    #2nd page shows the report form:
    
    label_requester_name = QLabel('Name:')
    label_requester_addr = QLabel('Address:')
    label_requester_mail = QLabel('Email:')
    self.edit_requester_name = QLineEdit()
    self.edit_requester_addr = QTextEdit()
    self.edit_requester_addr.setMaximumHeight(80)
    self.edit_requester_mail = QLineEdit()
    layout_requester = QGridLayout()
    layout_requester.addWidget(label_requester_name, 0, 0, 1, 1)
    layout_requester.addWidget(self.edit_requester_name, 0, 1, 4, 1)
    layout_requester.addWidget(label_requester_addr, 4, 0, 1, 1)
    layout_requester.addWidget(self.edit_requester_addr, 4, 1, 4, 1)
    layout_requester.addWidget(label_requester_mail, 8, 0, 1, 1)
    layout_requester.addWidget(self.edit_requester_mail, 8, 1, 4, 1)
    group_requester = QGroupBox('Requester')
    group_requester.setLayout(layout_requester)
    
    label_expert_name = QLabel('Name:')
    label_expert_addr = QLabel('Address:')
    label_expert_mail = QLabel('Email:')
    self.edit_expert_name = QLineEdit()
    self.edit_expert_addr = QTextEdit()
    self.edit_expert_addr.setMaximumHeight(80)
    self.edit_expert_mail = QLineEdit()
    layout_expert = QGridLayout()
    layout_expert.addWidget(label_expert_name, 0, 0, 1, 1)
    layout_expert.addWidget(self.edit_expert_name, 0, 1, 4, 1)
    layout_expert.addWidget(label_expert_addr, 4, 0, 1, 1)
    layout_expert.addWidget(self.edit_expert_addr, 4, 1, 4, 1)
    layout_expert.addWidget(label_expert_mail, 8, 0, 1, 1)
    layout_expert.addWidget(self.edit_expert_mail, 8, 1, 4, 1)
    group_expert = QGroupBox('Expert')
    group_expert.setLayout(layout_expert)
    
    self.edit_observations = QTextEdit()
    self.edit_observations.setMaximumHeight(80)
    layout_observations = QGridLayout()
    layout_observations.addWidget(self.edit_observations, 0, 0, 1, 1)
    group_observations = QGroupBox('Observations')
    group_observations.setLayout(layout_observations)
    
    self.label_plot = QLabel()
    self.label_plot.setFixedSize(700, 300)
    self.label_plot.setScaledContents(True)
    layout_group_plot = QGridLayout()
    layout_group_plot.addWidget(self.label_plot, 0, 0, 1, 1)
    group_plot = QGroupBox('Plot Preview')
    group_plot.setLayout(layout_group_plot)
    
    vertical_line = QFrame()
    vertical_line.setFrameShape(QFrame().VLine)
    vertical_line.setFrameShadow(QFrame().Sunken)
    
    layout_frame_form = QGridLayout()
    layout_frame_form.addWidget(group_requester, 0, 0, 1, 1)
    layout_frame_form.addWidget(vertical_line, 0, 1, 1, 1)
    layout_frame_form.addWidget(group_expert, 0, 2, 1, 1)
    layout_frame_form.addWidget(group_observations, 1, 0, 1, 3)
    layout_frame_form.addWidget(group_plot, 2, 0, 1, 3)
    
    frame_form = QFrame()
    frame_form.setLayout(layout_frame_form)
    
    scroll_area = QScrollArea()
    scroll_area.setWidget(frame_form)
    
    
    self.button_form_back = QPushButton()
    self.button_form_save = QPushButton()
    self.button_form_send = QPushButton()
    self.button_form_back.setText('Back')
    self.button_form_save.setText('Save')
    self.button_form_send.setText('Send')
    
    layout_form = QGridLayout()
    layout_form.addWidget(scroll_area, 0, 0, 1, 5)
    layout_form.addWidget(self.button_form_back, 1, 0, 1, 1)
    layout_form.addWidget(self.button_form_save, 1, 3, 1, 1)
    layout_form.addWidget(self.button_form_send, 1, 4, 1, 1)
    
    self.widget_page_form = QWidget()
    self.widget_page_form.setLayout(layout_form)
    
    self.widget_stacked = QStackedWidget(self)
    self.widget_stacked.addWidget(self.widget_page_plot)
    self.widget_stacked.addWidget(self.widget_page_form)
    
    layout_main = QGridLayout()
    layout_main.addWidget(self.widget_stacked)
    self.setLayout(layout_main)
    
    #---
    
    self.combo_zone.currentIndexChanged['QString'].\
      connect(self.handle_combo_zone_changed)
    self.combo_sensor.currentIndexChanged['QString'].\
      connect(self.handle_combo_sensor_changed)
    self.button_refresh.clicked.\
      connect(self.handle_button_refresh_clicked)
    self.button_report.clicked.\
      connect(self.handle_button_report_clicked)
    self.button_form_back.clicked.\
      connect(self.handle_button_form_back_clicked)
    self.button_form_save.clicked.\
      connect(self.handle_button_form_save_clicked)
    self.button_form_send.clicked.\
      connect(self.handle_button_form_send_clicked)
  
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
        except Exception as e:
          print e
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
    
  #============================================================================

  @pyqtSlot()
  def handle_button_report_clicked(self):
    
    try:
      exporter = pyqtgraph.exporters.ImageExporter(self.widget_plot.plotItem)
      exporter.export(self.cosmos_cli.local_filepath + '/plot.png')
      self.label_plot.setPixmap(QPixmap(self.cosmos_cli.local_filepath + '/plot.png'))
    except Exception as e:
      print e
      return
    
    self.widget_stacked.setCurrentIndex(1)

  #============================================================================

  @pyqtSlot()
  def handle_button_form_back_clicked(self):
    
    self.widget_stacked.setCurrentIndex(0)
  
  #============================================================================

  @pyqtSlot()
  def handle_button_form_save_clicked(self):
 
    rmlText = self.rep_template.get(str(self.combo_zone.currentText())+' - '+
                                    str(self.combo_sensor.currentText()),
                                    datetime.datetime.now().strftime("%Y-%m-%d"),
                                    str(self.edit_requester_name.text()),
                                    str(self.edit_requester_addr.toPlainText()),
                                    '',
                                    str(self.edit_expert_name.text()),
                                    str(self.edit_expert_addr.toPlainText()),
                                    '',
                                    str(self.edit_observations.toPlainText()),
                                    self.cosmos_cli.local_filepath+'/plot.png')
    pdf = rml2pdf.parseString(rmlText)
    
    filename = QFileDialog().getSaveFileName()
    
    if str(filename == ''): return
    
    with open(str(filename), 'w+') as pdfFile:
      pdfFile.write(pdf.read())
 
  #============================================================================

  @pyqtSlot()
  def handle_button_form_send_clicked(self):
    
    rmlText = self.rep_template.get(str(self.combo_zone.currentText())+' - '+
                                    str(self.combo_sensor.currentText()),
                                    datetime.datetime.now().strftime("%Y-%m-%d"),
                                    str(self.edit_requester_name.text()),
                                    str(self.edit_requester_addr.toPlainText()),
                                    str(self.edit_requester_mail.text()),
                                    str(self.edit_expert_name.text()),
                                    str(self.edit_expert_addr.toPlainText()),
                                    str(self.edit_expert_mail.text()),
                                    str(self.edit_observations.toPlainText()),
                                    self.cosmos_cli.local_filepath+'/plot.png')
    pdf = rml2pdf.parseString(rmlText)
    
    with open(self.cosmos_cli.local_filepath+'/rmlReport.pdf', 'w+') as pdfFile:
      pdfFile.write(pdf.read())
    
    time.sleep(1)
    
    (password, ok) = QInputDialog().getText(self, 'password', 'password', mode=QLineEdit.Password)
    
    print str(self.edit_requester_mail.text())
    print str(password)
    
    email_cli = EmailClient(username = str(self.edit_requester_mail.text()),
                            password = str(password))
    
    email_cli.sendEmail(from_addr=str(self.edit_requester_mail.text()),
                        to_addr=str(self.edit_expert_mail.text()),
                        mail_subject='[FRESH Expert Service] Request for Advice',
                        mail_body=str(self.edit_observations.toPlainText()),
                        attachment_path=self.cosmos_cli.local_filepath+'/rmlReport.pdf')

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
