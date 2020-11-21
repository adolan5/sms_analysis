import unittest
from smsanalysis.parsers import XMLParser

class TestParser:
    def test_read_data(self):
        pass

class TestXMLParser(unittest.TestCase, TestParser):
    def setUp(self):
        self.parser = XMLParser('foo')
