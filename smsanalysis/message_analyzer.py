import logging
import os
import re
import time
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)

class MessageAnalyzer:
    def __init__(self, sms_export):
        if not os.path.exists(sms_export):
            logger.error('Export {} does not exist'.format(sms_export))
            raise Exception('Argument must be a path to an sms export')
        read_time_start = time.time()
        tree = ET.parse(sms_export)
        read_time_end = time.time()
        self.read_time = read_time_end - read_time_start
        root = tree.getroot()
        self.all_messages = [dict(m.items()) for m in root]

    def __repr__(self):
        return 'SMS message analyzer containing total of {} messages; took {:.02f} seconds to read data'.format(len(self.all_messages), self.read_time)

    def get_messages_by_contact(self):
        organized_messages = {}
        for m in self.all_messages:
            cname = m.get('contact_name')
            contact_key = m.get('address') if cname == '(Unknown)' else cname
            organized_messages.setdefault(contact_key, []).append(m)
        return organized_messages

    def get_messages_by_direction(self, message_list):
        return {'sent': [m for m in message_list if m.get('type') == '2'], 'recv': [m for m in message_list if m.get('type') == '1']}

    def get_message_tokens(self, message_list):
        sym = re.compile('[^A-Za-z ]')
        full_body = re.sub(sym, '', ' '.join([m.get('body') for m in message_list if m.get('body') is not None]).lower())
        full_body = re.sub(sym, '', full_body)
        return nltk.word_tokenize(full_body)
