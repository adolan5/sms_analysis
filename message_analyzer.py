import nltk
import os
import xml.etree.ElementTree as ET
import time
import re

class message_analyzer:
    def __init__(self, sms_export):
        if not os.path.exists(sms_export):
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
        uniq_contacts = set(m.get('contact_name') for m in self.all_messages)
        return {name: [m for m in self.all_messages if m.get('contact_name') ==
            name] for name in uniq_contacts}

    def get_message_tokens(self, message_list):
        sym = re.compile('[^A-Za-z ]')
        full_body = re.sub(sym, '', ' '.join([m.get('body') for m in message_list if m.get('body') is not None]).lower())
        full_body = re.sub(sym, '', full_body)
        return nltk.word_tokenize(full_body)
