from zk import ZK, const
import sys
import logging

_ip = sys.argv[1]
_password = sys.argv[2]

logging.basicConfig(level=logging.DEBUG)

logging.debug("IP Address is %s from input", _ip)
logging.debug("Password %s from input", _password)
    
conn = None
logging.debug("create ZK instance")
zk = ZK(str(_ip), port=4370, timeout=5, password=int(_password), force_udp=False, ommit_ping=False)

try:
    logging.debug("Connect to device")
    conn = zk.connect()
    # disable device, this method ensures no activity on the device while the process is run
    conn.disable_device()
    # another commands will be here!
    # Example: Get All Users
    users = conn.get_users()
    print(users)
    
except Exception as e:
    logging.error("Fail to get attendences", exc_info=True)
finally:
    if conn:
        conn.disconnect()
