import os
import sys
import unittest
from zk.attendance import Attendance

sys.path.append(os.path.abspath('/home/sanaz/viraweb123/odoo-iot/vw-gateway/extensions/attendence/zktec'))
import zktec_connector

attendance = Attendance(18,18,"3-07-20 13:02:53",1,1)
#[<Attendance>: 18 : 2023-07-20 13:02:53 (1, 1)]

class TestStringMethods(unittest.TestCase):
    def test_send_telemetry(self):
        self._magic_number = 0
        self.__deviceName = "test"
        self.assertEqual(zktec_connector.send_telemetry(attendance),
                            device_id)
        