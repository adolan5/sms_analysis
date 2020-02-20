import logging
import os
import re
import time
from xml.etree import ElementTree as ET
from smsanalysis.message_collection import MessageCollection

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
        self.all_messages = MessageCollection([dict(m.items()) for m in root])

    def __repr__(self):
        return '<MessageAnalyzer|{} messages>'.format(len(self.all_messages))
