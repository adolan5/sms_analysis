import unittest
from smsanalysis.parsers import XMLParser

class TestParser:
    def test_read_data(self):
        self.assertEqual(5, len(self.parser.messages_list))

class TestXMLParser(unittest.TestCase, TestParser):
    def setUp(self):
        self.parser = XMLParser('./data/tests/sms-backup.xml')
