import logging
import os
from smsanalysis.parsers import Parser

logger = logging.getLogger(__name__)

# TODO
class XMLParser(Parser):
    def __init__(self, sms_source):
        super().__init__(sms_source)

    def _import_messages(self, sms_source):
        logger.debug('Importing SMS data from SMS Backup XML')
        return []
