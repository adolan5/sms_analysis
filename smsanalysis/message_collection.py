import logging
import phonenumbers

logger = logging.getLogger(__name__)

# TODO
class MessageCollection:
    def __init__(self, messages_list=None):

        messages_list = list() if messages_list is None else messages_list
        self.messages = messages_list

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

    def append(self, message):
        if type(message) is not dict:
            raise TypeError('message must be a formatted message.')
        original_number = phonenumbers.parse(message.get('number'), 'US')
        formatted_number = phonenumbers.format_number(original_number, phonenumbers.PhoneNumberFormat.E164)
        message['number'] = formatted_number
        self.messages.append(message)

    def extend(self, other_message_collection):
        if type(other_message_collection) is not MessageCollection:
            raise TypeError('other_message_collection must be a MessageCollection.')
        self.messages.extend(other_message_collection.messages)

    def __iter__(self):
        return iter(self.messages)

    def __getitem__(self, key):
        return self.messages[key]

    def __len__(self):
        return len(self.messages)

    def __repr__(self):
        return '<MessageCollection|{} messages>'.format(len(self.messages))
