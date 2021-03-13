import unittest
import copy
import json
from smsanalysis import MessageCollection
from smsanalysis.parsers import XMLParser
from jsonschema.exceptions import ValidationError

class TestMessageCollection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = XMLParser()
        cls.original_messages = parser.read_messages('./data/tests/sms-backup.xml')
        cls.single_message = {'body': 'a message', 'number': '+14115555553', 'sent': True}
        cls.bad_message = copy.deepcopy(cls.single_message)
        cls.bad_message['extra field'] = 'Bad'
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
        with self.assertRaises(ValidationError):
            badmessages = MessageCollection()
            badmessages.set_messages([self.bad_message])

    def test_get_messages_by_number(self):
        jeff_message_collection = self.messages.get_messages_for_number('+14115555554')
        self.assertEqual(self.jeff_messages, jeff_message_collection.messages)

    def test_get_messages_by_contact(self):
        jeff_message_collection = self.messages.get_messages_for_contact('Jeff')
        self.assertEqual(self.jeff_messages, jeff_message_collection.messages)

    def test_get_messages_by_direction(self):
        sent_messages = self.messages.get_messages_by_direction(sent=True)
        received_messages = self.messages.get_messages_by_direction(sent=False)
        for m in sent_messages:
            self.assertTrue(m.get('sent'))
        for m in received_messages:
            self.assertFalse(m.get('sent'))
        self.assertIsNotNone(sent_messages.get_contacts())
        self.assertIsNotNone(received_messages.get_contacts())

    def test_dump_messages(self):
        with open('./data/tests/MessageCollection.json') as f:
            expected_output = json.load(f)
        mc_output = json.loads(self.messages.dump())
        self.assertEqual(expected_output, mc_output)

    def test_create_from_dump(self):
        with self.assertRaises(FileNotFoundError):
            MessageCollection(filename='./data/notfound')
        with self.assertRaises(ValidationError):
            MessageCollection(filename='./data/tests/IncorrectMessageCollection.json')
        try:
            new_mc = MessageCollection(filename='./data/tests/MessageCollection.json')
        except:
            self.fail('Should not have failed creation from file')
        self.assertIsNotNone(new_mc.get_contacts())
        self.assertGreater(len(new_mc.messages), 0)

    def test_get_message_bodies(self):
        expected_messages = [
                'This is a test text message.',
                'This is also a test text message.',
                'Excellent!',
                'How\'s everything going with the SMS project?',
                'Not too bad. Slow, but coming along!']
        self.assertEqual(expected_messages, self.messages.get_message_bodies())
