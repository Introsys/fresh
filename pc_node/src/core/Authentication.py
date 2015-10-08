'''
Created on Sep 2, 2015

@author: msg
'''

import json
import logging
from datetime import datetime
from keystoneclient.v2_0 import client
from PyQt4 import QtCore
from PyQt4.QtCore import QDir, pyqtSignal, pyqtSlot, QMutex, QMutexLocker

class Authentication(QtCore.QThread):
  
  __slots__ = ('username', 'password', 'tenant_name', 'keystone_url', 'domain',
               'token', 'token_path', 'token_expires', 'token_auth_ref')

  tokenReceived = pyqtSignal("QString", name="tokenReceived")
  mutex = QMutex()
  
  def __init__(self, username="", password="", 
               tenant_name="Introsys", 
               keystone_url="http://cloud.lab.fiware.org:4730/v2.0", 
               domain = 'default',
               token_path = QDir.toNativeSeparators('{home}/.fresh/token'.format(home=QDir.homePath()))):
    super(Authentication, self).__init__()
    self.f_log = logging.getLogger('App') # this can be called in any place
    
    with QMutexLocker(self.mutex):
      self.username = username
      self.password = password
      self.tenant_name = tenant_name
      self.keystone_url = keystone_url
      self.domain = domain
      self.token_path = token_path.__str__()
      self.token_expires = datetime.now()
      self.token = None
      self.token_auth_ref = None
      

      
  #----------------------------------------------------------------------------  

  
  
  def run(self):
    ''' 
    method that executes the thread for getting a new token
    Emit the tokenReceived() signal when finished
    '''
    try:
      token = self.__getToken()
      self.tokenReceived.emit(token)
    except NameError as e:
      self.f_log.error("ERROR {0}".format(str(e)))
    finally:
      self.finished.emit()
  #----------------------------------------------------------------------------
    
  
  def __del__(self):
    ''' 
    TODO - Description
    '''
    self.f_log.debug('Object Authentication Destroyed')
    self.destroyed.emit(self)
  #----------------------------------------------------------------------------
    
 
  @pyqtSlot(name="getToken")   
  def getToken(self):
    ''' 
    Executes the start() method for initiate the thread
    Non blocking method, will emit a tokenReceived() signal from the run() method
    '''
    self.start()
  #----------------------------------------------------------------------------
    
  
  def getStaticToken(self):
    ''' 
    Static getToken method. this will block until the server response
    '''
    return self.__getToken()
  #----------------------------------------------------------------------------
  
  def __getToken(self):
    ''' 
      TODO - Description
    '''
    with QMutexLocker(self.mutex):
      if not self.token:
        try:
          self.__readTokenFromFile()
        except NameError as e:
          self.f_log.error("ERROR {0}".format(str(e)))
  
      if not self.token or self.token_expires < datetime.now():
        try:
          self.__getTokenFromServer()
        except NameError as e:
          self.f_log.error("ERROR {0}".format(str(e)))
          #raise
          pass
        try:
          self.__writeTokenToFile()
        except NameError as e:
          self.f_log.error("ERROR {0}".format(str(e)))
          pass
      if not self.token:
        raise NameError("Can't get token from file or server, please check the configurations")
      return self.token
  #----------------------------------------------------------------------------
  
  
  def __getTokenFromServer(self):
    ''' 
      TODO - Desciption
    '''
    try:
      keystone = client.Client(username=self.username,
                               password=self.password,
                               tenant_name=self.tenant_name,
                               auth_url=self.keystone_url,
                               domain_name=self.domain,
                               timeout=5)
      self.token = keystone.get_token(keystone.session)
      self.token_auth_ref = keystone.auth_ref
      self.token = self.token_auth_ref['token']['id']
      self.token_expires = datetime.strptime(self.token_auth_ref
                                             ['token']['expires'],
                                             '%Y-%m-%dT%H:%M:%SZ')
      self.f_log.info("Token: {token} [expires: {expires}]".format(token=self.token, expires=self.token_expires))
      return self.token
    except Exception as e:
      raise NameError("Error getting token from server ({erro})".format(erro=str(e)))
  
  #----------------------------------------------------------------------------
  
  def __readTokenFromFile(self):
    ''' 
      TODO - Desciption
    '''
    try:
      with open(QDir.toNativeSeparators('{0}/auth_ref'.format(self.token_path)).__str__(), 'r') as token_content:
        content = token_content.read()
        if not content:
          raise NameError("Token file is empty")
        else:
          self.token_auth_ref = json.loads(content)
          self.token = self.token_auth_ref['token']['id']
          self.token_expires = datetime.strptime(self.token_auth_ref
                                                 ['token']['expires'],
                                                 '%Y-%m-%dT%H:%M:%SZ')
          return self.token
    except Exception as e:
      raise NameError("Error getting token from file ({erro})".format(erro=str(e)))
  
  #----------------------------------------------------------------------------
  
  def __writeTokenToFile(self):
    ''' 
      TODO - Desciption
    '''
    try:
      # Create the directory if not exists
      if not QDir(self.token_path).exists():
        QDir().mkdir(self.token_path)
        self.f_log.debug("Created the Dir {dir}".format(dir=self.token_path))
        
    except Exception as e:
      self.f_log.error("ERRO {0}".format(str(e)))
    if not self.token_auth_ref:
      raise NameError('No token')
    try:
      with open(QDir.toNativeSeparators('{0}/auth_ref'.format(self.token_path)).__str__(), 'w+') as auth_ref:
        json.dump(self.token_auth_ref, auth_ref)
      with open(QDir.toNativeSeparators('{0}/token'.format(self.token_path)).__str__(), 'w+') as token:
        json.dump(self.token, token)
    except Exception as e:
      raise NameError('Error writing token to file {0}'.format(str(e)))
  #----------------------------------------------------------------------------



if __name__ == '__main__':
  
  import getpass
  
  auth = Authentication()
  auth.username = raw_input("username: ")
  auth.password = getpass.getpass()
  auth.tenant_name = raw_input("tenant: ")
#----------------------------------------------------------------------------

# EOF