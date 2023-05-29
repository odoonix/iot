import threading
import traceback
import cups  
from threading import Thread
from thingsboard_gateway.connectors.connector import Connector, log
import time
import os
import logging
from collections import Counter
import sys

sem = threading.Semaphore(1)

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
        self.__deviceName = config.get('deviceName', 'deviceName')
        
        # XXX: maso, 2023: rais error if prefix is not set
        # Set up lifecycle flags ---------------------------------------------------------------------------------------
        self.connection = False  # Service variable for check connection to device
        self.__logger = logging.getLogger("cups-"+self.__deviceName)

    def connect_device(self):
        """connects to the device throu tcp
        
        raise excpetion if connection fail
        """
        try:
            self.connection = cups.Connection()
            self.printers = self.connection.getPrinters()
        except (cups.IPPError) as e:
            os.abort(403)
           
    def open(self): 
        self.stopped = False
        self.start()

    def get_name(self):
        return self.name

    def is_connected(self):
        return self.connection 
    
    def find_jobs(self):
        # Find jobs
        dict_jobs_counter = {}
        job_completed = self.connection.getJobs(which_jobs='completed')
        job_not_completed = self.connection.getJobs(which_jobs='not-completed')
        job_all = self.connection.getJobs(which_jobs='all')

        # Completed Jobs
        result_job_completed= []
        for job in job_completed:
            string = self.connection.getJobAttributes(job)['job-printer-uri']
            printer_name_for_select_job = list(string.split("/"))[-1]
            result_job_completed.append(printer_name_for_select_job)
        dict_count_job_completed = Counter(result_job_completed)

        # Not_Completed Jobs
        result_job_not_completed= []
        for job in job_not_completed:
            string = self.connection.getJobAttributes(job)['job-printer-uri']
            printer_name_for_select_job = list(string.split("/"))[-1]
            result_job_not_completed.append(printer_name_for_select_job)
        dict_count_job_not_completed = Counter(result_job_not_completed)

        # All Jobs
        result_job_all= []
        for job in job_all:
            string = self.connection.getJobAttributes(job)['job-printer-uri']
            printer_name_for_select_job = list(string.split("/"))[-1]
            result_job_all.append(printer_name_for_select_job)
        dict_count_job_all = Counter(result_job_all)

        # Add Counter jobs
        dict_jobs_counter["Completed_jobs"] = dict_count_job_completed
        dict_jobs_counter["not_completed_jobs"] = dict_count_job_not_completed
        dict_jobs_counter["all_jobs"] = dict_count_job_all
        
        return dict_jobs_counter

    # Main method of thread, must contain an infinite loop and all calls to data receiving/processing functions.
    def run(self):
        while (True):
            try:
                if not self.is_connected():
                    self.connect_device()
                    
                # Find jobs
                dict_count_job_all = self.find_jobs() 
                for key, config in self.printers.items():
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
                        
                    # Send telemetry
                    for key_counter , value_counter in dict_count_job_all.items():
                        result['telemetry'].append({
                        key_counter: value_counter[key]
                    })

                    # Send result to thingsboard
                    self.gateway.send_to_storage(self.get_name(), result)
    
            except:
                logging.error("Printer Not Connected")
                result['attributes'].append({"Printer Error" : True})
            
            time.sleep(5)
    
    def close(self):
        #printer_names = self.connection.printers.keys()
        #for printer_name in printer_names:    
        #        self.connection.disablePrinter(printer_name)
        #signal.signal(signal.SIGINT, self.signal_handler)
        #signal.signal(signal.SIGINT, self.stop())
        pass
        
    def on_attributes_update(self, content):
        pass
    
    def print_file(self, printer_name , printer_file): 
        printid = self.connection.printFile(printer_name, printer_file ,'' , {})
        
    def server_side_rpc_handler(self, content):
        sem.acquire()
        try:
            self._server_side_rpc_handler(content, 3)
        except Exception as ex :
            self.__logger.error("Cups unsupported exception happend %s", ex)
            traceback.print_exc()
            
            self.gateway.send_rpc_reply(
                device= content["device"], 
                req_id= content["data"]["id"],
                content = {"success_sent":"False" , "message" :"Cups unsupported exception happend %s" % ex }
            )
        finally: 
            sem.release()
            time.sleep(0.25)

    
    def _server_side_rpc_handler(self, content, tries_count=3):
        params = content["data"]["params"]
        method_name = content["data"]["method"]
        try:
            if method_name == "print_file":
                # printer_file is encode string so first decode string
                str_decoded = params["printer_file"].decode('utf8', 'strict')
                self.print_file(params["printer_name"], str_decoded)
        except Exception as ex :
            self.__logger.error("Cups unsupported exception happend : %s, %s", ex, traceback.extract_stack)
            if tries_count > 0:
                self.connect_device()
                return self._server_side_rpc_handler(content, tries_count-1)
            raise ex
            

