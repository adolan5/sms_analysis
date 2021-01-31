import logging
import os
from xml.etree import ElementTree as ET
from smsanalysis.parsers import Parser

logger = logging.getLogger(__name__)

# TODO
class XMLParser(Parser):
    def __init__(self):
        super().__init__()

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
        # TODO: This currently does not correctly pull data from MMS messages -
        # those need to be handled differently
        messages_list = [dict(m.items()) for m in root]
        return messages_list
