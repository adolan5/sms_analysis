import logging
import os
from xml.etree import ElementTree as ET
from smsanalysis.parsers import Parser
from smsanalysis import MessageCollection

logger = logging.getLogger(__name__)

class XMLParser(Parser):
    def __init__(self):
        super().__init__()
        self.contacts = dict()

    def _import_messages(self, sms_source):
        logger.debug('Importing SMS data from SMS Backup XML')
        if type(sms_source) is not str:
            logger.error('sms_source is expected to be a path to an sms export')
        logger.debug('Attempting to import SMS messages from {}'.format(sms_source))
        if not os.path.exists(sms_source):
            logger.error('Export {} does not exist'.format(sms_source))
            raise Exception('Argument must be a path to an sms export')
        tree = ET.parse(sms_source)
        root = tree.getroot()
        messages = MessageCollection()
        for m in root:
            messages.append(self._process_message_parts(dict(m.items())))
        return messages

    """
    TODO: This currently does not correctly pull data from MMS messages -
    those need to be handled differently
    """
    def _process_message_parts(self, message_parts):
        formatted_number = self._format_number(message_parts.get('address'))
        new_message = dict()
        new_message['body'] = message_parts.get('body')
        new_message['number'] = formatted_number
        direction = message_parts.get('type')
        new_message['sent'] = True if direction == '2' else False
        self.contacts[formatted_number] = message_parts.get('contact_name')
        return new_message
