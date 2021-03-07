import unittest
from smsanalysis.parsers import XMLParser

class TestParser:
    def test_message_number_format(self):
        expected_numbers = set(['+14115555555', '+14115555554'])
        numbers = set([m.get('number') for m in self.messages])
        self.assertEqual(expected_numbers, numbers)

    def test_read_num_messages(self):
        self.assertEqual(5, len(self.messages))

    def test_message_ordering(self):
        self.assertEqual("This is a test text message.", self.messages[0].get('body'))
        self.assertEqual("How's everything going with the SMS project?", self.messages[3].get('body'))

    def test_message_direction(self):
        self.assertTrue(self.messages[0].get('sent'))
        self.assertFalse(self.messages[1].get('sent'))
        self.assertTrue(self.messages[2].get('sent'))
        self.assertFalse(self.messages[3].get('sent'))
        self.assertTrue(self.messages[4].get('sent'))

    def test_contact_dict(self):
        expected_contacts = {'+14115555555': 'Alice', '+14115555554': 'Jeff'}
        self.assertDictEqual(expected_contacts, self.parser.contacts)

class TestXMLParser(unittest.TestCase, TestParser):
    @classmethod
    def setUpClass(cls):
        cls.parser = XMLParser()
        cls.messages = cls.parser.read_messages('./data/tests/sms-backup.xml')
