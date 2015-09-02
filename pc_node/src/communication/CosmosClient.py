'''
Created on Sep 1, 2015

@author: msg
'''

import os
import requests

from time import time

class CosmosClient(object):
  
  __slots__ = ('username', 'password', 'webhdfs_url', 'auth_url',
               'hdfs_username', 'hdfs_filepath', 'hdfs_filename',
               'token', 'token_expires', 'history')

  def __init__(self):
    
    self.username = ''
    self.password = ''
    self.webhdfs_url = 'http://130.206.80.46:14000/webhdfs/v1'
    self.auth_url = 'https://130.206.80.46:13000/cosmos-auth/v1'
    self.hdfs_username = ''
    self.hdfs_filepath = ''
    self.hdfs_filename = ''
    self.token = None
    self.token_expires = int(time())
    self.history = None
  
  #----------------------------------------------------------------------------
  
  def getToken(self):
    
    if self.token and int(time()) < self.token_expires:
      return self.token
    
    try:
      url = self.auth_url+'/token'
      headers = {'Accept': 'application/json',
                 'Content-Type': 'application/json'}
      payload = {'grant_type': 'password',
                 'username': self.username,
                 'password': self.password}
      r = requests.post(url=url, headers=headers, data=payload, verify=False)
      self.token = r.json()['access_token']
      print 'New token from cosmos: %s' % self.token
      self.token_expires = int(time()) + int(r.json()['expires_in'])
    except:
      raise
  
  #----------------------------------------------------------------------------
  
  def getFileStatus(self):
    
    try:
      url = self.webhdfs_url+'/user/'+self.hdfs_username+self.hdfs_filepath+self.hdfs_filename
      headers = {'Accept': 'application/json',
                 'Content-Type': 'application/json',
                 'X-Auth-Token': self.getToken()}
      payload = {'op': 'GETFILESTATUS',
                 'user.name': self.hdfs_username}
      r = requests.get(url=url, headers=headers, params=payload)
      print r.text

    except:
      pass
  
  #----------------------------------------------------------------------------
  
  def getFileContent(self):
    
    try:
      url = self.webhdfs_url+'/user/'+self.hdfs_username+self.hdfs_filepath+self.hdfs_filename
      headers = {'Accept': 'application/json',
                 'Content-Type': 'application/json',
                 'X-Auth-Token': self.getToken()}
      payload = {'op': 'OPEN',
                 'user.name': self.hdfs_username}
      r = requests.get(url=url, headers=headers, params=payload)
      self.history = r.text
      
    except:
      pass
  
  #----------------------------------------------------------------------------
  
  def writeHistoryToFile(self):
    
    if not self.history:
      raise NameError("No historic data to write")
    
    file_path = os.environ['HOME'] + '/.fresh/history'
    if not os.path.exists(file_path):
      os.makedirs(file_path)
    
    try:
      with open(file_path+'/history.txt', 'w+') as hist_file:
        hist_file.write(self.history)
    except:
      raise NameError('Error writing token to file')
   
  #---------------------------------------------------------------------------- 
  
  def readHistoryFromFile(self):
    
    file_path = os.environ['HOME'] + '/.fresh/history'
    
    try:
      with open(file_path+'/history.txt', 'r') as hist_file:
        self.history = hist_file.read()
    except:
      raise NameError('Error reading token from file')    

#==============================================================================

if __name__ == '__main__':
  
  import getpass
  
  cosmos_cli = CosmosClient()
  cosmos_cli.username = raw_input("username: ")
  cosmos_cli.password = getpass.getpass()
  cosmos_cli.hdfs_username = raw_input("cosmos user: ")
  cosmos_cli.hdfs_filepath = raw_input("hdfs filepath: ")
  cosmos_cli.hdfs_filename = raw_input("hdfs filename: ")

  cosmos_cli.getToken()
  cosmos_cli.getFileStatus()
  cosmos_cli.getFileContent()
  cosmos_cli.writeHistoryToFile()
  cosmos_cli.readHistoryFromFile()