import logging

logger = logging.getLogger(__name__)

class MessageCollection:
    def __init__(self, messages_list):

        for m in messages_list:
            if m.get('contact_name') == '(Unknown)':
                m['contact_name'] = m.get('address')
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

    def __iter__(self):
        return iter(self.messages)

    def __len__(self):
        return len(self.messages)

    def __repr__(self):
        return '<MessageCollection|{} messages>'.format(len(self.messages))
