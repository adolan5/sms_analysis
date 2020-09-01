import logging
import os
import re
import time
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)

class MessageCollection:
    def __init__(self, sms_source):
        if type(sms_source) is str:
            messages_list = self._import_messages(sms_source)
        elif type(sms_source) is list:
            messages_list = sms_source
        else:
            logger.error('sms_source is expected to be a path to an sms export (str) or a list of messages')

        for m in messages_list:
            if m.get('contact_name') == '(Unknown)':
                m['contact_name'] = m.get('address')
        self.messages = messages_list

    def _import_messages(self, sms_source):
        logger.debug('Attempting to import SMS messages from {}'.format(sms_source))
        if not os.path.exists(sms_source):
            logger.error('Export {} does not exist'.format(sms_source))
            raise Exception('Argument must be a path to an sms export')
        read_time_start = time.time()
        tree = ET.parse(sms_source)
        root = tree.getroot()
        # TODO: This currently does not correctly pull data from MMS messages -
        # those need to be handled differently
        messages_list = [dict(m.items()) for m in root]
        read_time_end = time.time()
        read_time = read_time_end - read_time_start
        logger.debug('Read {} messages in {} seconds'.format(len(messages_list), read_time))
        return messages_list

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
