import unittest
from smsanalysis.parsers import XMLParser

class TestMessageCollection(unittest.TestCase):
    def setUp(self):
        self.parser = XMLParser()
        self.messages = self.parser.read_messages('./data/tests/sms-backup.xml')

    def test_message_number_format(self):
        expected_numbers = set(['+14115555555', '+14115555554'])
        numbers = set([m.get('number') for m in self.messages])
        self.assertEqual(expected_numbers, numbers)
