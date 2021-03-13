import logging
import pkg_resources
import json
import jsonschema

logger = logging.getLogger(__name__)

class MessageCollection:
    def __init__(self, filename=None):
        self._contacts = None
        self.messages = list()
        try:
            schema_stream = pkg_resources.resource_stream(__name__, 'data/schema/message_collection.json')
            self._schema = json.load(schema_stream)
            schema_stream.close()
        except:
            logger.error('Failed to get message collection schema resource')

    def set_contacts(self, contacts):
        self._contacts = contacts

    def set_messages(self, new_messages):
        self.messages = new_messages
        self.validate()

    def get_contacts(self):
        return self._contacts

    def get_messages_for_number(self, number):
        matching_messages = [m for m in self.messages if m['number'] == number]
        new_collection = MessageCollection()
        new_collection.set_messages(matching_messages)
        return new_collection

    def get_messages_for_contact(self, contact_name):
        matching_numbers = [k for (k,v) in self._contacts.items() if v == contact_name]
        matching_collections = [self.get_messages_for_number(n) for n in matching_numbers]
        full_collection = MessageCollection()
        for m in matching_collections:
            full_collection.extend(m)
        return full_collection

    """
    TODO: Requires Update
    def get_contact_names(self):
        return set([m.get('contact_name') for m in self.messages])

    def get_message_bodies(self):
        return [m.get('body') for m in self.messages]

    def get_messages_by_contact(self):
        organized_messages = {}
        for m in self.messages:
            organized_messages.setdefault(m.get('contact_name'), []).append(m)
        return {k: MessageCollection(v) for k, v in organized_messages.items()}

    def get_messages_by_direction(self):
        return {'sent': MessageCollection([m for m in self.messages if m.get('type') == '2']),
                'recv': MessageCollection([m for m in self.messages if m.get('type') == '1'])}
    """

    def append(self, message):
        if type(message) is not dict:
            raise TypeError('message must be a formatted message.')
        self.messages.append(message)

    def extend(self, other_message_collection):
        if type(other_message_collection) is not MessageCollection:
            raise TypeError('other_message_collection must be a MessageCollection.')
        self.messages.extend(other_message_collection.messages)

    def validate(self):
        jsonschema.validate(self.messages, self._schema)

    def dumps(self, filename=None):
        output = { 'contacts': self._contacts, 'messages': self.messages }
        if filename is None:
            return json.dumps(output)
        with open(filename, 'w') as f:
            json.dump(output, f)

    def __iter__(self):
        return iter(self.messages)

    def __getitem__(self, key):
        return self.messages[key]

    def __len__(self):
        return len(self.messages)

    def __repr__(self):
        message_len = len(self.messages)
        contact_len = 'None' if self._contacts is None else len(self._contacts)
        return '<MessageCollection|{} messages| {} contacts>'.format(message_len, contact_len)
