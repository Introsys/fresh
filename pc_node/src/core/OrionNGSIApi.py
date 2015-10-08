#! /usr/bin/python
'''
Created on May 15, 2015

@author: Magno Guedes, Andre Silva
@mail: magno.guedes@introsys.eu, andre.silva@introsys.eu
'''

import requests
import logging
import sys
import simplejson as json
from requests import ConnectionError

class OrionNGSIApi(object):
  ''' 
    Small API for Orion NGSI API core
    This is a low level API and therefore the return data from all the methods includes:
    http response code
    ngsi response code
    response content (raw) 
  '''
  
  def __init__(self, orion_ip, orion_port, token):    
    ''' 
      TODO - Description
    '''
    super(OrionNGSIApi, self).__init__()
    self.f_log = logging.getLogger('App') # this can be called in any place
    self.f_log.debug("Create object OrionNGSIApi")
    
    self.orion_ip = str (orion_ip)
    self.orion_port = str (orion_port)
    self.auth_token = str (token)
  # -----------------------------------------------------------------------------
  
  
  def __del__(self):
    self.f_log.debug("Object OrionNGSIAPI destroyed")
  
  
  def createContext(self, _type, _id, attributes=[]):
    ''' 
    Orion Create Context API  
    '''
    self.f_log.debug("Sending createContext to Orion")
    try:       
      headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Auth-Token': self.auth_token
      }
      body = {
        'contextElements' : 
        [{
          'type': _type,
          'isPattern': 'false',
          'id': _id,
          'attributes': attributes
        }],
        'updateAction': 'APPEND'
      }
      # Send HTTP post to server, this will wait for the server response
      address = 'http://{ip}:{port}/v1/updateContext'.format(ip=self.orion_ip, port=self.orion_port)
      r = requests.post(address, data=json.dumps(body), headers=headers)
      # Evaluate the HTTP response and returns a tuple with the http and ngsi response code, msg description and raw response code
      if r.status_code == 200:  
        json_response = json.loads(r.content)
        self.f_log.info('HTTP Code: {0}  |  NGSI Code: {1}  |  Create context sent successfully'.format(r.status_code, json_response['contextResponses'][0]['statusCode']['code']))
        return {'http_code': r.status_code, 
                'ngsi_code': json_response['contextResponses'][0]['statusCode']['code'],
                'msg': 'CreateContext sent successfully',
                'content':r.content}
      elif r.status_code == 405:
        self.f_log.warning('HTTP Code: {0}  |  Method not allowed'.format(r.status_code))
        return {'http_code': r.status_code, 'msg': 'Method not allowed'}
      else:
        self.f_log.warning('HTTP Code: {0}  |  Method not allowed'.format(r.status_code))
        return {'http_code': r.status_code, 'msg': 'Unknown error'}
    except ConnectionError as e:
      self.f_log.error('ERROR {0}'.format(str(e)))
    except:
      e = sys.exc_info()[0] 
      self.f_log.error('ERROR {0}'.format(str(e)))
      raise
  # -----------------------------------------------------------------------------
  
  
  def updateContext(self, _type, _id, attributes=[]):
    ''' Orion Update Context API 
    '''
    self.f_log.debug("Sending updateContext to Orion")
    try:
      headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Auth-Token': self.auth_token
      }
      body =  {
        'contextElements' : [{
          'type': _type,
          'isPattern': 'false',
          'id': _id,
          'attributes': attributes
        }],
        'updateAction': 'UPDATE'
      }
      # Send HTTP post to server, this will wait for the server response
      address = 'http://{ip}:{port}/v1/updateContext'.format(ip=self.orion_ip, port=self.orion_port)
      r = requests.post(address, data=json.dumps(body), headers=headers)
      # Evaluate the HTTP response and returns a tuple with the http and ngsi response code, msg description and raw response code
      if r.status_code == 200:  
        json_response = json.loads(r.content)
        self.f_log.info('HTTP Code: {0}  |  NGSI Code: {1}  |  Update context sent successfully'.format(r.status_code, json_response['contextResponses'][0]['statusCode']['code']))
        return {'http_code': r.status_code, 
                'ngsi_code': json_response['contextResponses'][0]['statusCode']['code'],
                'msg': 'UpdateContext sent successfully',
                'content':r.content}
      elif r.status_code == 405:
        self.f_log.warning('HTTP Code: {0}  |  Method not allowed'.format(r.status_code))
        return {'http_code': r.status_code, 'msg': 'Method not allowed'}
      else:
        self.f_log.warning('HTTP Code: {0}  |  Method not allowed'.format(r.status_code))
        return {'http_code': r.status_code, 'msg': 'Unknown error'}
    except ConnectionError as e:
      self.f_log.error('ERROR {0}'.format(str(e)))
    except:
      e = sys.exc_info()[0] 
      self.f_log.error('ERROR {0}'.format(str(e)))
      raise
  # -----------------------------------------------------------------------------
  
  
  def persistDataToHDFS(self, _type, _id, attributes=[]):
    ''' 
      Cygnus Subscription to Orion Context Update Attributes ONCHANGE 
      returns 
        if successful: http_code | subscription_id | subscription_duration
        if error:      http_code | error message
    '''
    
    self.f_log.debug("Sending subscription request to Orion")
    json_list =  json.loads(json.dumps(attributes))
    _list = []
    for att in json_list:
      _list.append(att['name']) 
    try:  
      headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Auth-Token': self.auth_token
      }
      body =  { 
        'entities' : [{
          'type': _type,
          'isPattern': 'false',
          'id': _id,
        }],
        'attributes': _list,
        'reference': 'http://localhost:5050/notify',
        'duration': 'P1M',
        'notifyConditions':[{
          'type': 'ONCHANGE',
          'condValues': _list
        }]
      }
      # Send HTTP post to server, this will wait for the server response
      address = 'http://{ip}:{port}/v1/subscribeContext'.format(ip=self.orion_ip, port=self.orion_port)
      r = requests.post(address, data=json.dumps(body), headers=headers) 
      self.f_log.debug('Subscription - the response code is {0}'.format(str(r.status_code)))
      if r.status_code == 200:  
        json_response = json.loads(r.content)
        return {'http_code': r.status_code, 
                'subscription_id': json_response['subscribeResponse']['subscriptionId'],
                'subscription_duration': json_response['subscribeResponse']['duration']
                }
      elif r.status_code == 405:
        self.f_log.warning('HTTP Code: {0}  |  Method not allowed'.format(r.status_code))
        return {'http_code': r.status_code, 'msg': 'Method not allowed'}
      else:
        self.f_log.warning('HTTP Code: {0}  |  Method not allowed'.format(r.status_code))
        return {'http_code': r.status_code, 'msg': 'Unknown error'}
    except ConnectionError as e:
      self.f_log.error('ERROR {0}'.format(str(e)))
      return None
    except:
      e = sys.exc_info()[0] 
      self.f_log.error('ERROR {0}'.format(str(e)))
      return None
      raise
  # -----------------------------------------------------------------------------


  def removeHDFSSubscription(self, _subscriptionId):
    ''' 
    Cygnus Cancel Subscription to Orion Context Update Attributes 
    '''
    self.f_log.debug("Sending unsubscribe context request to Orion")
    try:
      headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Auth-Token': self.auth_token
      }
      body =  { 
        'subscriptionId':_subscriptionId
      }
      
      # Send HTTP post to server, this will wait for the server response
      address = 'http://{ip}:{port}/v1/unsubscribeContext'.format(ip=self.orion_ip, port=self.orion_port)
      r = requests.post(address, data=json.dumps(body), headers=headers)     
      
      if r.status_code == 200:  
        json_response = json.loads(r.content)
        self.f_log.info('Unsubscribe - the HTTP Code: {0}  and  NGSI Code: {1} response codes'.format(r.status_code, json_response['statusCode']['code']))
        return {'http_code': r.status_code, 
                'ngsi_code': json_response['statusCode']['code'],
                'msg': 'Unsubscribe sent successfully',
                'content':r.content}
      elif r.status_code == 405:
        self.f_log.warning('HTTP Code: {0}  |  Method not allowed'.format(r.status_code))
        return {'http_code': r.status_code, 'msg': 'Method not allowed'}
      else:
        self.f_log.warning('HTTP Code: {0}  |  Method not allowed'.format(r.status_code))
        return {'http_code': r.status_code, 'msg': 'Unknown error'}
    
    except ConnectionError as e:
      self.f_log.error('ERROR {0}'.format(str(e)))
    except:
      e = sys.exc_info()[0] 
      self.f_log.error('ERROR {0}'.format(str(e)))
      raise
  # -----------------------------------------------------------------------------
    



# EOF