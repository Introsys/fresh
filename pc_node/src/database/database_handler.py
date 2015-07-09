#! /usr/bin/python
'''
Created on May 27, 2015

@author: Andre Silva, Magno Guedes
@mail: andre.silva@introsys.eu, magno.guedes@introsys.eu
'''

import logging
import sqlite3
from datetime import date, datetime


class DatabaseHandler(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        

    
###############################################################################    
    
    def list_devices(self):
        ''' '''
        db = sqlite3.connect('freshdb')
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT * 
            FROM device
        ''')
        
        db.close()
        
        return 0
    
    
    def list_devices_by_zone(self, zone):
        ''' '''      
        db = sqlite3.connect('freshdb')
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT * 
            FROM device 
            WHERE id_zone = zone
        ''')
        
      
                
        db.close()


    def get_deivce(self, device_id):
        ''' '''
        db = sqlite3.connect('freshdb')
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT * 
            FROM device 
            WHERE id = id
        ''')
        
        device = cursor.fetchone()
        
        print device
        
        db.close()

        
    def update_device(self, device_id, descrition = "", id_zone = 0, rssi = 0, 
                      supply_voltage = 0, temperature = 0, added_date = "", 
                      last_update = ""):
        ''' '''
        
        db = sqlite3.connect('freshdb')
        cursor = db.cursor()    
        
        cursor.execute('''
            UPDATE device
            SET 
            WHERE id = :device_id
        ''',
        {'device_id', device_id })
        
        db.close()

        
    def add_device(self):
        ''' '''
        db = sqlite3.connect('freshdb')
        cursor = db.cursor()
        
        cursor.execute('''
            
        ''')
        
        db.close()


    def remove_device(self, device_id):
        ''' '''
        db = sqlite3.connect('freshdb')
        cursor = db.cursor()
        
        cursor.execute('''
            
        ''')
        
        db.close()


        
###############################################################################
    
    def list_zones(self):
        ''' '''
        db = sqlite3.connect('freshdb')
        cursor = db.cursor()
        
        cursor.execute('''
            
        ''')
        
        db.close()


    def add_zone(self):
        ''' '''
        db = sqlite3.connect('freshdb')
        cursor = db.cursor()
        
        cursor.execute('''
            
        ''')
        
        db.close()


    def update_zone(self):
        ''' '''
        db = sqlite3.connect('freshdb')
        cursor = db.cursor()
        
        cursor.execute('''
            
        ''')
        
        db.close()


    def remove_zone(self):
        ''' '''
        db = sqlite3.connect('freshdb')
        cursor = db.cursor()
        
        cursor.execute('''
            
        ''')
        
        db.close()


###############################################################################