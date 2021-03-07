import logging
import pkg_resources
import json
import jsonschema

logger = logging.getLogger(__name__)

class MessageCollection:
    def __init__(self, messages_list=None):
        self._contacts = None
        try:
            schema_stream = pkg_resources.resource_stream(__name__, 'data/schema/message_collection.json')
            self._schema = json.load(schema_stream)
            schema_stream.close()
        except:
            logger.error('Failed to get message collection schema resource')
        if messages_list is None:
            self.messages = list()
        else:
            jsonschema.validate(messages_list, self._schema)
            self.messages = message_list

    def set_contacts(self, contacts):
        self._contacts = contacts

    def get_contacts(self):
        return self._contacts

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
