import unittest
from smsanalysis.parsers import XMLParser

class TestParser:
    def test_read_num_messages(self):
        self.assertEqual(5, len(self.messages))

    def test_message_ordering(self):
        pass
        # self.assertEqual("This is a text message.", self.messages)

class TestXMLParser(unittest.TestCase, TestParser):
    def setUp(self):
        self.parser = XMLParser()
        self.messages = self.parser.read_messages('./data/tests/sms-backup.xml')
