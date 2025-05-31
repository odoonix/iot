import sys
import signal
import logging

import rich
from zk import ZK, const


def zk_devices_check_connection(ip=None, password=None):
    """Connects to the ZK device and get more information from device.
    """
    logging.debug("create ZK instance")
    conn = None
    zk = ZK(str(ip), port=4370, timeout=5, password=int(
        password), force_udp=False, ommit_ping=True)

    try:
        logging.debug("Connect to device")
        conn = zk.connect()
        attendances = conn.get_attendance()
        users = conn.get_users()
        rich.print(users)
        rich.print(attendances)
    except Exception as e:
        logging.error("Fail to get attendences", exc_info=True)
    finally:
        if conn:
            conn.disconnect()
