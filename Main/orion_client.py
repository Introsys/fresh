#! /usr/bin/python

import requests
import json

orionURL = "http://172.18.1.15:10026"

def createContext(type, id, attributes=[]):
  
  body =  {
        "contextElements" : [
                 {
                        "type": type,
                        "isPattern": "false",
                        "id": id,
      "attributes": attributes
                }
        ],
  "updateAction": "APPEND"
  }
  headers = {
        "Accept": "application/json",
        "Content-type": "application/json"
  }
  print json.dumps(body)
  r = requests.post("http://172.18.1.15:10026/v1/updateContext", data=json.dumps(body), headers=headers)
  print "The response code is " + str(r.status_code)
  
  if r.status_code == 200:
    print "Message sent succesfully"

  elif r.status_code == 405:
    print "There was an error"

  else:
    print "Unknown result"
    
    
    
def updateContext(type, id, attributes=[]):
  
  body =  {
        "contextElements" : [
                 {
                        "type": type,
                        "isPattern": "false",
                        "id": id,
      "attributes": attributes
                }
        ],
  "updateAction": "UPDATE"
  }
  headers = {
        "Accept": "application/json",
        "Content-type": "application/json"
  }
  print json.dumps(body)
  r = requests.post("http://172.18.1.15:10026/v1/updateContext", data=json.dumps(body), headers=headers)
  print "The response code is " + str(r.status_code)
  
  if r.status_code == 200:
    print "Message sent succesfully"

  elif r.status_code == 405:
    print "There was an error"

  else:
    print "Unknown result"