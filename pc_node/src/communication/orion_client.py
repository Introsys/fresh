#! /usr/bin/python
'''
Created on May 15, 2015

@author: Magno Guedes, Andre Silva
@mail: magno.guedes@introsys.eu, andre.silva@introsys.eu
'''

import requests
import logging
import os
import sys
import yaml
import simplejson as json
from requests import ConnectionError
from keystoneclient import exceptions
from keystoneclient.v2_0 import client
from PyQt4 import QtCore


''' Configuration files
Authentication Token is store in the .fresh.token file
Configuration are store in the .fresh.cfg
'''

###############################################################################
###############################################################################


class OrionClient(QtCore.QObject):
  ''' TODO - Description '''

  # -----------------------------------------------------------------------------
  # 
  def __init__(self, orion_ip, orion_port, username, password, 
              keystone_ip, keystone_port, keystone_url, tenant_name,
              tenant_id, domain, token_path, parent = None):
    
    super(OrionClient, self).__init__()
        
    self.o_log = logging.getLogger('orion')
    self.cfg_loded = False
    self.token_loded = False
    self.__parent = parent
    
    self.orion_ip = str (orion_ip)
    self.orion_port = str (orion_port)
    self.username = str (username)
    self.password = str (password)
    self.keystone_ip = str (keystone_ip)
    self.keystone_port = str (keystone_port)
    self.keystone_url = str (keystone_url)
    self.tenant_name = str (tenant_name)
    self.tenant_id  = str (tenant_id)
    self.domain = str (domain)
    self.token_path = str (token_path)
    
    self.cfg_loded = True
    
    # Load token_path if exists already
    mode = 'r' if os.path.exists(self.token_path) else 'w'
    with open(self.token_path, mode) as token_content:
        content = token_content.read()
        if not content:
          self.o_log.error('Token file is empty!')
        else:
          self.auth_ref = json.loads(content)
          self.o_log.info('Token was loded with success')
          self.token_loded = True    
  
    
  # -----------------------------------------------------------------------------
  #
  def getAuthToken(self):
    '''  '''
    
    try: 
      if self.token_loded:
        keystone = client.Client(username=self.username,
                                 password=self.password,
                                 tenant_name=self.tenant_name,
                                 auth_url=self.keystone_url,
                                 domain_name=self.domain,
                                 auth_ref=self.auth_ref,
                                 timeout=5)
      else:
        keystone = client.Client(username=self.username,
                                 password=self.password,
                                 tenant_name=self.tenant_name,
                                 auth_url=self.keystone_url,
                                 domain_name=self.domain,
                                 timeout=5)

        self.auth_ref = keystone.auth_ref
        
        with open(self.token_path, 'w') as outfile:
          json.dump(self.auth_ref, outfile) # Save the token into a file

      token = keystone.get_token(keystone.session)
          
      return token
        
    except IOError as e:
      print 'Erro {0}: {1}'.format(e.errno, e.strerror)
      
    except yaml.YAMLError as e:
      print 'Erro in configuration file: {0}'.format(e)
      
    except exceptions.Unauthorized as e:
      print 'Erro in configuration file: {0}'.format(e)
    except exceptions.AuthorizationFailure as e:  
      print 'Erro in configuration file: {0}'.format(e)
    except:
      e = sys.exc_info()[0]
      print str(e)
      #raise    
    

  # -----------------------------------------------------------------------------
  # -----------------------------------------------------------------------------
  # -----------------------------------------------------------------------------
    

  # -----------------------------------------------------------------------------
  # 
  def createContext(self, _type, _id, attributes=[]):
    ''' TODO - Description '''
    
    try:     
      if self.cfg_loded:
        body =  {
              'contextElements' : [
                       {
                              'type': _type,
                              'isPattern': 'false',
                              'id': _id,
            'attributes': attributes
                      }
              ],
        'updateAction': 'APPEND'
        }
        headers = {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'X-Auth-Token': self.getAuthToken()
        }
      
        r = requests.post('http://{0}:{1}/v1/updateContext'.format(self.orion_ip,
                                                                 self.orion_port), 
                        data=json.dumps(body), headers=headers)
          
        #print 'The response code is ' + str(r.status_code) # DBEUG
        
        if r.status_code == 200:
          print 'Message sent succesfully'
        elif r.status_code == 405:
          print 'There was an error'
        else:
          print 'Unknown result'
      else:
        print 'No configuration was provided'
        
    except ConnectionError as e:
      print "Error sending CreateContext to Orion {0} ".format(str(e))
    except:
      e = sys.exc_info()[0] 
      print str(e)
      #raise

  # -----------------------------------------------------------------------------
  #
  def updateContext(self, _type, _id, attributes=[]):
    ''' TODO - Description '''
    try:     
      if self.cfg_loded:
        body =  {
              'contextElements' : [
                       {
                              'type': _type,
                              'isPattern': 'false',
                              'id': _id,
            'attributes': attributes
                      }
              ],
        'updateAction': 'UPDATE'
        }
        headers = {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'X-Auth-Token': self.getAuthToken()
        }
        r = requests.post('http://{0}:{1}/v1/updateContext'.format(self.orion_ip,
                                                                   self.orion_port), 
                                                                   data=json.dumps(body), headers=headers)
        #print 'The response code is ' + str(r.status_code)
        if r.status_code == 200:
          print 'Message sent succesfully'
      
        elif r.status_code == 405:
          print 'There was an error'
      
        else:
          print 'Unknown result'
    except ConnectionError as e:
      print "Error sending UpdateContext to Orion {0} ".format(str(e))
    except:
      e = sys.exc_info()[0] 
      print str(e)
      #raise
      
  # -----------------------------------------------------------------------------
  #
  def persistDataToHDFS(self, _type, _id, attributes=[]):
    ''' '''
    print "send Subscription request"
    json_list =  json.loads(json.dumps(attributes))
    _list = []
    for att in json_list:
      _list.append(att['name']) 
    try:
      body =  { 
        'entities' : [
          {
            'type': _type,
            'isPattern': 'false',
            'id': _id,
          }
        ],
        'attributes': _list,
        'reference': 'http://localhost:5050/notify',
        'duration': 'P1M',
        'notifyConditions':[
          {
            'type': 'ONCHANGE',
            'condValues': _list
          }
        ]
      }
      
      headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Auth-Token': self.getAuthToken()
      }
      
      r = requests.post('http://{0}:{1}/v1/subscribeContext'.format(self.orion_ip,
                                                                 self.orion_port), 
                                                                 data=json.dumps(body), headers=headers)     
      print 'The response code is ' + str(r.status_code)
      if r.status_code == 200:
        print 'Message sent Subscription succesfully'
        return str(r.content)
      elif r.status_code == 400:
        print 'There was an error'
      else:
        print 'Unknown result'
    except ConnectionError as e:
      print "Error sending SubscribeContext to Orion {0}".format(str(e))
    except:
      e = sys.exc_info()[0] 
      print str(e)
      #raise
    
    # -----------------------------------------------------------------------------
  #
  def removeHDFSSubscription(self, _subscriptionId):
    ''' '''
    #print "send unSubscription request"
    try:
      body =  { 'subscriptionId':_subscriptionId}
      
      headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Auth-Token': self.getAuthToken()
      }
      
      r = requests.post('http://{0}:{1}/v1/unsubscribeContext'.format(self.orion_ip,
                                                                 self.orion_port), 
                                                                 data=json.dumps(body), headers=headers)     
      print 'The response code is ' + str(r.status_code)
      if r.status_code == 200:
        print 'Message sent Unsubscribe Context succesfully'
        return str(r.content)
      elif r.status_code == 400:
        print 'There was an error'
      else:
        print 'Unknown result'
    
    except ConnectionError as e:
      print "Error sending SubscribeContext to Orion {0}".format(str(e))
    
    except:
      e = sys.exc_info()[0] 
      print str(e)
      #raise
    
    
    
    
    
    
#EOF