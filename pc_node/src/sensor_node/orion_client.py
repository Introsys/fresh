#! /usr/bin/python
'''
Created on May 15, 2015

@author: Magno Guedes, Andre Silva
@mail: magno.guedes@introsys.eu, andre.silva@introsys.eu
'''

import requests
import logging
import os
import yaml
import simplejson as json
from keystoneclient import exceptions
from keystoneclient.v2_0 import client


''' Configuration files
Authentication Token is store in the .fresh.token file
Configuration are store in the .fresh.cfg
'''

###############################################################################
###############################################################################


class OrionClient(object):
  ''' TODO - Description '''

  def __init__(self, token_file='.fresh.token',cfg_file='.fresh.cfg'):
    '''Load the Configuration Files'''
    self.o_log = logging.getLogger('orion')
    self.cfg_loded = False
    self.token_loded = False
    self.token_file = token_file
    self.cfg_file = cfg_file
    
    
    try:
      # Load config file
      mode = 'r' if os.path.exists(self.cfg_file) else'w'
      with open(self.cfg_file, mode) as cfg_content:
        cfg = yaml.load(cfg_content)
        if not cfg:        
          self.o_log.error('Configuration file is empty!')
        else:
          print 'Reading File...'
          self.orion_ip = cfg['orion_ip']
          self.orion_port = cfg['orion_port']
          self.username = cfg['username']
          self.password = cfg['password']
          self.keystone_ip = cfg['keystone_ip']
          self.keystone_port = cfg['keystone_port']
          self.keystone_url = cfg['keystone_url']
          self.tenant_name = cfg['tenant_name']
          self.tenant_id = cfg['tenant_id']
          self.domain = cfg['domain']
          self.cfg_loded = True

      # -------------------------------------------------------
      
      # Load token if exists already
      mode = 'r' if os.path.exists(self.token_file) else 'w'
      with open(self.token_file, mode) as token_content:
          content = token_content.read()
          if not content:
            self.o_log.error('Token file is empty!')
          else:
            self.auth_ref = json.loads(content)
            self.o_log.info('Token was loded with success')
            self.token_loded = True   
      
      # -------------------------------------------------------

    except IOError as e:
      print 'I/O error({0}): {1}'.format(e.errno, e.strerror)

      # TODO

# -----------------------------------------------------------------------------

  
  def createContext(self, _type, _id, attributes=[]):
    ''' TODO - Description '''
    
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
      print json.dumps(body)
      r = requests.post('http://{0}:{1}/v1/updateContext'.format(self.orion_ip,
                                                                 self.orion_port), 
                        data=json.dumps(body), headers=headers)
      
      print 'The response code is ' + str(r.status_code)
      
      if r.status_code == 200:
        print 'Message sent succesfully'
    
      elif r.status_code == 405:
        print 'There was an error'
    
      else:
        print 'Unknown result'
        
        
    else:
      print 'No configuration was provided'
  
# -----------------------------------------------------------------------------

  def updateContext(self, _type, _id, attributes=[]):
    ''' TODO - Description '''
    
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
    print json.dumps(body)
    r = requests.post('http://{0}:{1}/v1/updateContext'.format(self.orion_ip,
                                                               self.orion_port), 
                      data=json.dumps(body), headers=headers)
    print 'The response code is ' + str(r.status_code)
    
    if r.status_code == 200:
      print 'Message sent succesfully'
  
    elif r.status_code == 405:
      print 'There was an error'
  
    else:
      print 'Unknown result'


# -----------------------------------------------------------------------------

  def getAuthToken(self):
    ''' TODO - Description '''
    
    try: 
      if self.token_loded:
        keystone = client.Client(username=self.username,
                                 password=self.password,
                                 tenant_name=self.tenant_name,
                                 auth_url=self.keystone_url,
                                 domain_name=self.domain,
                                 auth_ref=self.auth_ref)
      else:
        keystone = client.Client(username=self.username,
                                 password=self.password,
                                 tenant_name=self.tenant_name,
                                 auth_url=self.keystone_url,
                                 domain_name=self.domain)

        self.auth_ref = keystone.auth_ref
        with open(self.token_file, 'w') as outfile:
            json.dump(self.auth_ref, outfile) # Save the token into a file
   
      token = keystone.get_token(keystone.session)
    
      return token
        
    except IOError as e:
      print 'Erro {0}: {1}'.format(e.errno, e.strerror)  
      
    except yaml.YAMLError as e:
      print 'Erro in configuration file: {0}'.format(e)
      
    except exceptions.Unauthorized as e:
      print 'Erro in configuration file: {0}'.format(e) 
      
    
      
      
      
      
#EOF