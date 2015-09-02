'''
Created on Sep 2, 2015

@author: msg
'''

import os
import json
from datetime import datetime
from keystoneclient.v2_0 import client

class Authentication(object):
  
  __slots__ = ('username', 'password', 'tenant_name', 'keystone_url', 'domain',
               'token', 'token_path', 'token_expires', 'token_auth_ref')

  def __init__(self):
    
    #default values:
    self.username = ''
    self.password = ''
    self.tenant_name = 'Introsys'
    self.keystone_url = 'http://cloud.lab.fiware.org:4730/v2.0'
    self.domain = 'default'
    self.token = None
    self.token_path = os.environ['HOME'] + '/.fresh/token'
    self.token_expires = datetime.now()
    self.token_auth_ref = None
    
  def getToken(self):
    
    if not self.token:
      try:
        self.readTokenFromFile()
      except NameError as e:
        print e
    
    if not self.token or self.token_expires < datetime.now():
      try:
        self.getTokenFromServer()
      except NameError as e:
        print e
        raise
      try:
        self.writeTokenToFile()
      except NameError as e:
        print e
        pass
    
    if not self.token:
      raise
    
    return self.token

  #----------------------------------------------------------------------------
  
  def getTokenFromServer(self):
    try:
      keystone = client.Client(username=self.username,
                               password=self.password,
                               tenant_name=self.tenant_name,
                               auth_url=self.keystone_url,
                               domain_name=self.domain,
                               timeout=5)
      #self.token = keystone.get_token(keystone.session)
      self.token_auth_ref = keystone.auth_ref
      self.token = self.token_auth_ref['token']['id']
      self.token_expires = datetime.strptime(self.token_auth_ref
                                             ['token']['expires'],
                                             '%Y-%m-%dT%H:%M:%SZ')
      print 'New token: %s' % self.token
      print 'expires: %s' % self.token_expires
      return self.token
    
    except:
      raise NameError("Error getting token from server")
  
  #----------------------------------------------------------------------------
  
  def readTokenFromFile(self):
    try:
      with open(self.token_path+'/auth_ref', 'r') as token_content:
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
      print e
      raise NameError("Error reading token from file")
  
  #----------------------------------------------------------------------------
  
  def writeTokenToFile(self):
    
    if not os.path.exists(self.token_path):
      os.makedirs(self.token_path)
    
    if not self.token_auth_ref:
      raise NameError('No token')
    try:
      with open(self.token_path+'/auth_ref', 'w+') as token_file:
        json.dump(self.token_auth_ref, token_file)
      with open(self.token_path+'/token', 'w+') as token_file:
        json.dump(self.token, token_file)
    except:
      raise NameError('Error writing token to file')
  
  #----------------------------------------------------------------------------
  
if __name__ == '__main__':
  
  import getpass
  
  auth = Authentication()
  auth.username = raw_input("username: ")
  auth.password = getpass.getpass()
  auth.tenant_name = raw_input("tenant: ")
  print auth.getToken()