import unittest
import sys
import os

sys.path.append(os.path.abspath('/home/sanaz/viraweb123/odoo-iot/vw-gateway/extensions/attendence/zktec'))
import zktec_connector

class TestStringMethods(unittest.TestCase):

    def test_convert_to_device_id(self):
        data = [
            (1, 31745, 62),
            (1, 0x3C01, 30),
            (1, 0x201,  1),
            (1, 513,  1),
            # Magic number is default
            (513, 513, 0),
            (4095, 4095, 0x0),
        ]
        for user_id, device_id, magic_number in data:
            self.assertEqual(zktec_connector.convert_to_device_id(magic_number, user_id),
                            device_id)
            self.assertEqual(zktec_connector.convert_to_company_id(magic_number, device_id),
                            user_id)
    def test_convert_to_device_id_invalid(self):
        ids = [
            2500,
            6000,
            2049,
        ]
        magic_number= 0x7c00
        for id in ids:
            self.assertRaises(Exception, zktec_connector.convert_to_device_id, magic_number, id)
        
    def test_convert_to_device_id_invalid_magic_number(self):
        id = 0x01
        magic_number= 0x8c00
        self.assertRaises(Exception, zktec_connector.convert_to_device_id, magic_number, id)


if __name__ == '__main__':
    unittest.main()