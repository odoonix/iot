import cups  
from threading import Thread
from thingsboard_gateway.connectors.connector import Connector, log
from pathlib import Path
from zk import ZK
from zk.exception import ZKErrorResponse,ZKNetworkError
from datetime import datetime
import time
import pytz
import os
import logging



class CUPSPro(Connector, Thread): 

    def __init__(self, gateway, config, connector_type):
        super().__init__()
        self.statistics = {'MessagesReceived': 0,
                           'MessagesSent': 0}
        self.gateway = gateway  # Reference to TB Gateway
        self.connector_type = connector_type  # Use For Convertor
        self.config = config  # sii.json Contents

        # Extract main sections from configuration ---------------------------------------------------------------------
        self.__prefix = config.get('prefix', 'prefix')
        # XXX: maso, 2023: rais error if prefix is not set
        
        
        # Set up lifecycle flags ---------------------------------------------------------------------------------------
        #self.connection = False  # Service variable for check connection to device
        #self.__logger = logging.getLogger("zkteck-"+self._ip)


    def connect_device(self):
        """connects to the device throu tcp
        
        raise excpetion if connection fail
        """
        self.connection = cups.Connection()

            
    def open(self): 
        self.stopped = False
        self.start()

    def get_name(self):
        return self.name

    def is_connected(self):
        return False #self.connection and self.connection.is_connect

    
    # Main method of thread, must contain an infinite loop and all calls to data receiving/processing functions.
    def run(self):
        while (True):
            try:
                
                if not self.is_connected():
                    self.connect_device()
                    
                printers = self.connection.getPrinters()
                for key, config in printers.items():
                    result = {
                        'deviceName': self.__prefix + key,
                        'deviceType': self.config.get('deviceType', 'default'),
                        'attributes': [],
                        'telemetry': [],
                    }
                    
                    # Send attribute 
                    for attribute_key in ['printer-is-shared', 'printer-state', 'printer-state-message', 'printer-state-reasons', 'printer-type',
                                          'printer-uri-supported', 'printer-location', 'printer-info', 'device-uri', 'printer-make-and-model']:
                        result['attributes'].append({
                            attribute_key: config[attribute_key]
                        })
                        
                    # TODO: maso, 2023: check if there is a telemetry
                    # Send telemetry
                    job_not_completed = len(self.connection.getJobs(which_jobs='not-completed'))
                    job_completed = len(self.connection.getJobs(which_jobs='completed'))
                    job_all = len(self.connection.getJobs(which_jobs='all'))
                    
                    result['telemetry'].append({"job_not_completed" : job_not_completed})
                    result['telemetry'].append({"job_completed" : job_completed})
                    result['telemetry'].append({"job_all": job_all})
                    
                    # Send result to thingsboard
                    self.gateway.send_to_storage(self.get_name(), result)
    
            except :
                logging.error("Printer Not Connected")
                result['attributes'].append({"Printer Error" : True})
                
            time.sleep(5)

    def close(self):
        if self.connection:
            self.connection.disconnect()

    def on_attributes_update(self, content):
        pass

    def server_side_rpc_handler(self, content):
        pass


 #close//is_connected//telemetry job//exept 
 