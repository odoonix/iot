import sys
import signal
import logging

import rich
from zk import ZK, const


def zk_devices_check_connection(ip=None, password=None, port=4370):
    """Connects to the ZK device and get more information from device.
    """
    logging.debug("create ZK instance")
    zk = ZK(str(ip), port=port, timeout=5, password=int(
        password), force_udp=False, ommit_ping=True)

    try:
        logging.debug("Connect to device")
        conn = zk.connect()
        attendances = conn.get_attendance()
        users = conn.get_users()
        rich.print(users)
        rich.print(attendances)
    finally:
        if conn:
            conn.disconnect()


def zk_devices_check_utf8(ip=None, password=None, port=4370):
    """Check devices language
    """
    conn = None
    logging.debug("create ZK instance")
    zk = ZK(str(ip), port=port, timeout=5, password=int(
        password), force_udp=False, ommit_ping=True)

    try:
        logging.debug("Connect to device")
        conn = zk.connect()
        # disable device, this method ensures no activity on the device while the
        # process is run
        conn.disable_device()
        # another commands will be here!
        conn.set_user(uid=1000, name='فارسی', privilege=const.USER_DEFAULT,
                      password='', group_id='', user_id='1000', card=0)

    except Exception:
        logging.error("Fail to get attendences", exc_info=True)
    finally:
        if conn:
            conn.disconnect()


def zk_devices_get_attendance(ip=None, password=None, port=4370):
    """Check devices language
    """
    logging.debug("create ZK instance")
    zk = ZK(str(ip), port=port, timeout=5, password=int(
        password), force_udp=False, ommit_ping=True)

    try:
        logging.debug("Connect to device")
        conn = zk.connect()
        # disable device, this method ensures no activity on the device while the process is run
        conn.disable_device()
        # another commands will be here!
        # Example: Get All Users
        attendances = conn.get_attendance()
        rich.print(attendances)
    finally:
        if conn:
            conn.disconnect()


def zk_devices_get_user_info(ip=None, password=None, port=4370):
    """Check devices language
    """
    logging.debug("create ZK instance")
    zk = ZK(str(ip), port=port, timeout=5, password=int(
        password), force_udp=False, ommit_ping=True)

    try:
        logging.debug("Connect to device")
        conn = zk.connect()
        # disable device, this method ensures no activity on the device while the process is run
        conn.disable_device()
        # another commands will be here!
        # Example: Get All Users
        users = conn.get_users()
        for user in users:
            privilege = 'User'
            if user.privilege == const.USER_ADMIN:
                privilege = 'Admin'
            rich.print('+ UID #{}'.format(user.uid))
            rich.print('  Name       : {}'.format(user.name))
            rich.print('  Privilege  : {}'.format(privilege))
            rich.print('  Password   : {}'.format(user.password))
            rich.print('  Group ID   : {}'.format(user.group_id))
            rich.print('  User  ID   : {}'.format(user.user_id))

        # Test Voice: Say Thank You
        conn.test_voice()
        # re-enable device after all commands already executed
        conn.enable_device()
    finally:
        if conn:
            conn.disconnect()
