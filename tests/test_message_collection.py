import unittest
import copy
from smsanalysis import MessageCollection
from smsanalysis.parsers import XMLParser
from jsonschema.exceptions import ValidationError

class TestMessageCollection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = XMLParser()
        cls.original_messages = parser.read_messages('./data/tests/sms-backup.xml')
        cls.single_message = {'body': 'a message', 'number': '+14115555553', 'sent': True}
        cls.bad_message = {'body': 'a bad message', 'number': '+14115555553', 'sent': True, 'extra field': 'bad'}
        cls.jeff_messages = [
                {'body': 'How\'s everything going with the SMS project?', 'number': '+14115555554', 'sent': False},
                {'body': 'Not too bad. Slow, but coming along!', 'number': '+14115555554', 'sent': True} ]

    def setUp(self):
        self.messages = copy.deepcopy(self.original_messages)

    def test_append(self):
        other_mc = MessageCollection()
        self.assertEqual(0, len(other_mc))
        try:
            other_mc.append(self.single_message)
        except:
            self.fail('Should not have thrown')
        self.assertEqual(1, len(other_mc))

    def test_append_exception(self):
        with self.assertRaises(TypeError):
            self.messages.append('fail')

    def test_extend(self):
        other_mc = MessageCollection()
        other_mc.append(self.single_message)
        try:
            self.messages.extend(other_mc)
        except:
            self.fail('Should not have thrown')
        self.assertEqual(6, len(self.messages))

    def test_extend_exception(self):
        other_list = ['not', 'a', 'MessageCollection']
        with self.assertRaises(TypeError):
            self.messages.extend(other_list)

    def test_validate(self):
        try:
            self.messages.validate()
        except:
            self.fail('Should not have thrown')
        # Circumvent formatting done by append
        self.messages.messages.append(self.bad_message)
        with self.assertRaises(ValidationError):
            self.messages.validate()

    def test_validate_on_create(self):
        bad_message_number_format = {'body': 'a message', 'number': 'a'}
        another_bad_message_number_format = {'body': 'a message', 'number': '23'}
        with self.assertRaises(ValidationError):
            badmessages = MessageCollection([self.bad_message])
        with self.assertRaises(ValidationError):
            badmessages = MessageCollection([bad_message_number_format])
        with self.assertRaises(ValidationError):
            badmessages = MessageCollection([another_bad_message_number_format])

    def test_get_messages_by_number(self):
        jeff_message_collection = self.messages.get_messages_for_number('+14115555554')
        self.assertEqual(self.jeff_messages, jeff_message_collection.messages)

    def test_get_messages_by_contact(self):
        jeff_message_collection = self.messages.get_messages_for_contact('Jeff')
        self.assertEqual(self.jeff_messages, jeff_message_collection.messages)