import json
import os
from threading import Thread
import traceback
from thingsboard_gateway.connectors.connector import Connector, log
from pathlib import Path
from zk import ZK,const
from zk.exception import ZKErrorResponse,ZKNetworkError
from datetime import datetime
import time
import pytz
import logging
from simplejson import dumps
import threading
import signal


sem = threading.Semaphore(1)

class ZktecPro(Connector, Thread):
 
    def __init__(self, gateway, config, connector_type):
        super().__init__()
        self.statistics = {'MessagesReceived': 0,
                           'MessagesSent': 0}
        self.gateway = gateway  # Reference to TB Gateway
        self.connector_type = connector_type  # Use For Convertor
        self.config = config  # zktec.json Contents

        # Extract main sections from configuration ---------------------------------------------------------------------
        self.__device = config.get('device')
        self.__storage_path = config.get('storage')
        self._name = self.__device.get('name', 'zktec')
        self._ip = self.__device.get('ip', '127.0.0.1')
        self._port = self.__device.get('port', "1883")
        self._password = self.__device.get('password', "1")
        self._timezone = self.__device.get('timezone', "210")
        
        # Set up lifecycle flags ---------------------------------------------------------------------------------------
        self.connection = False  # Service variable for check connection to device
        self.__logger = logging.getLogger("zkteck-"+self._ip)
        self.__deviceName = config.get('deviceName', 'deviceName')
        self.__deviceType = config.get('deviceType', 'default')
        
        # Create device
        self.gateway.add_device(self.__deviceName, {"connector": self},
                                    device_type=self.__deviceType)
 
    def connect_device(self):
        """connects to the device throu tcp
        
        raise excpetion if connection fail
        """
        # if self.connection and not self.connection.disconnect():
        #     raise Exception("Fail to disconnect from device. Something bad happend.")
            
        self.connection = ZK(
            self._ip, 
            port=int(self._port), 
            timeout=5, 
            password=int(self._password), 
            force_udp=False, 
            ommit_ping=False, 
            verbose=False,
            encoding='UTF-8',
        )
        if not self.connection.connect():
            raise Exception("Fail to connect to the device")

    def open(self): 
        self.stopped = False
        self.start()

    def get_name(self):
        return self.name

    def is_connected(self):
        return self.connection and self.connection.is_connect

    def timezone(self, attendence):
        tz = pytz.FixedOffset(int(self._timezone))
        
        datetimeOrg = attendence.timestamp
        dateTimeUts = datetime(
            datetimeOrg.year,
            datetimeOrg.month,
            datetimeOrg.day,
            datetimeOrg.hour,
            datetimeOrg.minute,
            datetimeOrg.second,
            tzinfo=tz
        )
        attendence.timestamp = datetime.fromtimestamp(
            datetime.timestamp(dateTimeUts))
        return attendence.timestamp
 
    def get_storage_path(self):
        
        path_storage = Path(self.__storage_path + '/%s.txt' % self.config.get('deviceName')) 
        #path_storage = os.path.join(self.__storage_path,'/%s.txt' % self.config.get('deviceName'))
        return path_storage

    def lastdatetime_text_file(self):
        # Fetch last date time
        
        path = self.get_storage_path()
        
        if path.is_file():
            with open(path, 'r') as f:
                lines = f.readlines()
                lastdatetime = datetime.strptime(lines[0], '%Y-%m-%d %H:%M:%S')
        else:
            lastdatetime = datetime.strptime('1990-10-5 00:00:00', '%Y-%m-%d %H:%M:%S')
        return lastdatetime

    def send_attribute(self):
        try:
            self.connection.read_sizes()
        except:
            logging.info("Usage Space device Not available")
        try:
            firmware_version = self.connection.get_firmware_version()
        except:
            logging.info("Firmware Version device Not available")
        try:
            serialnumber = self.connection.get_serialnumber()
        except:
            logging.info("Serial Number device Not available")
        try:
            platform = self.connection.get_platform()
        except:
            logging.info("Platform device Not available")
        try:
            device_name = self.connection.get_device_name()
        except:
            logging.info("Device Name Not available")
        try:
            face_version = self.connection.get_face_version()
        except:
            logging.info("Face Version device Not available")
        try:
            fp_version = self.connection.get_fp_version()
        except:
            logging.info("Finter Print Version device Not available")
        try:
            extend_fmt = self.connection.get_extend_fmt()
        except:
            logging.info("Extend FMT device Not available")
        try:
            user_extend_fmt = self.connection.get_user_extend_fmt()
        except:
            logging.info("User Extend FMT device Not available")
        try:
            face_fun_on = self.connection.get_face_fun_on()
        except:
            logging.info("Face Fun On device Not available")
        try:
            compat_old_firmware = self.connection.get_compat_old_firmware(),
        except:
            logging.info("Compat Old Firmware device Not available")
        try:
            network_params = self.connection.get_network_params()
        except:
            logging.info("Network Params device Not available")
        try:
            mac = self.connection.get_mac()
        except:
            logging.info("Mac device Not available")
        try:
            pin_width = self.connection.get_pin_width()
        except:
            logging.info("pin_width device Not available")

        device_attribute = {
            "ZKTec Error": False,
            "Records" : self.connection.records,
            "Max Records": self.connection.rec_cap,
            "Users": self.connection.users,
            "Max Users": self.connection.users_cap,
            "Fingers": self.connection.fingers,
            "Max Fingers": self.connection.fingers_cap,
            "Faces": self.connection.faces,
            "Max Faces": self.connection.faces_cap,
            "Firmware Version": firmware_version,
            "Serialnumber": serialnumber,
            "Platform": platform,
            "Device_name": device_name,
            "Face Version": face_version,
            "Finter Print Version": fp_version,
            "Extend Fmt": extend_fmt,
            "User Extend Fmt": user_extend_fmt,
            "Face Fun On": face_fun_on,
            "Compat Old Firmware": compat_old_firmware,
            "Network Params": network_params,
            "Mac": mac,
            "Pin Width": pin_width
        }

        return (device_attribute)

    def send_telemetry(self, attendence):
        attendence_telemetry = {
            "ts": attendence.timestamp.timestamp()*1000,
            "values":
                {
                "user_id": attendence.user_id,
                "timestamp": str(attendence.timestamp),
                "punch": attendence.punch
            }
        }
        return attendence_telemetry

    # Main method of thread, must contain an infinite loop and all calls to data receiving/processing functions.
    def run(self):
        path = self.get_storage_path()
        
        while (True):
            sem.acquire()
            
            self.result_dict = {
                            'deviceName': self.__deviceName,
                            'deviceType': self.__deviceType,
                            'attributes': [],
                            'telemetry': [],
                        }

            
            #result = {
            #    'deviceName': self.config.get('deviceName', 'ZktecDevice'),
            #    'deviceType': self.config.get('deviceType', 'default'),
            #    
            #    'attributes': [],
            #    'telemetry': [],
            #}
            
            try:   
                if not self.is_connected():
                    self.connect_device()
                    
                lastdatetime = self.lastdatetime_text_file()
                attendances = self.connection.get_attendance()

                # Send Attribute
                device_attribute = self.send_attribute()
                self.result_dict['attributes'].append(device_attribute)
                
                # Send Telemetry
                for attendence in attendances:
                    # Change key telemetry 
                    attendence.timestamp = self.timezone(attendence)
                    if attendence.punch == 1:
                            attendence.punch = 'in'
                    elif attendence.punch == 2:
                        attendence.punch = 'out'
                
                    
                    if attendence.timestamp > lastdatetime:
                        
                        attendence_telemetry = self.send_telemetry(attendence)
                        
                        self.result_dict['telemetry'].append(attendence_telemetry)
                        lastdatetime = attendence.timestamp
                        with open(path, 'w') as f:
                            f.write(str(lastdatetime))
                
            # except ZKErrorResponse as e:
            #     self.__logger.error("ZKTec failt to get response from device : %s", e)
            #     if self.connection:
            #         self.connection = False
            #     result['attributes'].append({"ZKTec Response Error" : True})
                
            # except ZKNetworkError as netex:
            #     self.__logger.error("ZKTec network error : %s", netex)
            #     if self.connection:
            #         self.connection = False
            #     result['attributes'].append({"ZKTec Network Error" : True})
                    
            except Exception as ex:
                logging.error('ZKTec unsupported exception happend: %s', ex)
                self.result_dict['attributes'].append({"ZKTec Error" : True})
                
                
                traceback.print_exc()
                # Note: for network connection
                try: 
                    self.connect_device()
                except:
                    pass
                
  
            finally:
                # Send result to thingsboard
                self.gateway.send_to_storage(self.get_name(), self.result_dict)
                sem.release()
                time.sleep(1)    
        
    def close(self):
        if self.connection:
            self.connection.disconnect()

    def on_attributes_update(self, content):
        pass
    
    def update_user(self, params , content):
        
        if not self.connection:
            raise Exception("Device is not connected")
        users = self.connection.get_users()
        
        for key, value in params.items():
            # Check user is exist        
            exist_user = 0
            for item in users:
                if item.user_id == value["user_id"]:
                    exist_user = item
                
                
            # user not exist Create user 
            if exist_user == 0:
                self.connection.set_user(int(value["uid"]),
                            value["name"],
                            value["privilege"],
                            value["password"],
                            value["group_id"],
                            value["user_id"],
                            int(value["card"])
                            )
            else:
                # user is exist delete and create
                # save finger print
                
                fingers = self.connection.get_templates()
                
                save_fingers = []
                for finger in fingers:
                    if finger.uid == value["uid"]:
                        save_fingers.append(finger)
                
                
                self.connection.delete_user(user_id=value["user_id"])
                  
                self.connection.set_user(int(value["uid"]),
                            value["name"],
                            value["privilege"],
                            value["password"],
                            value["group_id"],
                            value["user_id"],
                            int(value["card"])
                            )
                # add finger print
                self.connection.save_user_template(value["uid"], save_fingers) 
                  
            self.gateway.send_rpc_reply(
                            device= content["device"], 
                            req_id= content["data"]["id"],
                            content = {"success_sent": 'True'}
                        )
           
    def del_user(self , params , content):
        if not self.connection:
            raise Exception("Device is not connected")
        
        for key, value in params.items():              
            
            self.connection.delete_user(user_id=value['user_id_delete'])
            
            self.gateway.send_rpc_reply(
            device= content["device"], 
            req_id= content["data"]["id"],
            content = {"success_sent": 'True'}
            )
     
    def update_fingerprint(self, params):
        # TODO : add toway rpc for get template in rpc reply
        if not self.connection:
            raise Exception("Device is not connected")
        
        #fingers = self.connection.get_templates()
        #for finger in fingers:
        #    if finger.uid == int(params["user_id_change"]):
        #        finger = self.connection.enroll_user(int(params["user_id_change"]))
        #    else:
        self.connection.enroll_user(int(params["user_id_change"]))
        
        #template = self.connection.get_user_template(uid=int(params["user_id_change"]), temp_id=0)
        
    def server_side_rpc_handler(self, content):
        sem.acquire()
        try:
            self._server_side_rpc_handler(content, 3)
        except Exception as ex :
            self.__logger.error("ZKTec unsupported exception happend %s", ex)
            traceback.print_exc()
            
            self.gateway.send_rpc_reply(
                device= content["device"], 
                req_id= content["data"]["id"],
                content = {"success_sent":"False" , "message" :"ZKTec unsupported exception happend %s" % ex }
            )
        finally: 
            sem.release()
            time.sleep(0.25)
               
    def _server_side_rpc_handler(self, content, tries_count=3):
        params = content["data"]["params"]
        method_name = content["data"]["method"]
        try:
                # update_user
            if method_name == "update_user":
                return self.update_user(params, content)
            
            # delete user
            if method_name == "del_user":
                return self.del_user(params, content)
                
            # update fingerprint 
            if method_name == "update_fingerprint":
                return self.update_fingerprint(params)
        except ZKNetworkError as netex:
            self.__logger.error("ZKTec network error detected : %s, %s", netex, traceback.extract_stack)
            if tries_count > 0:
                self.connect_device()
                return self._server_side_rpc_handler(content, tries_count-1)
            raise netex
        
        
        
