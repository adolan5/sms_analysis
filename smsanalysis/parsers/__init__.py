import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

from smsanalysis.parsers.parser import Parser
from smsanalysis.parsers.xml_sms_backup import XMLParser
