import logging
import spacy
from smsanalysis import MessageAnalyzer, MessageCollection
from smsanalysis.parsers import XMLParser

logging.basicConfig()
logging.getLogger('smsanalysis').setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.debug('Loading spacy model')
spacy_model = spacy.load('en_core_web_md', disable=['parse', 'ner'])
# spacy_model = spacy.load('en_core_web_sm', disable=['parse', 'ner'])

logger.debug('Creating XML Parser')
xml_parser = XMLParser('./data/sms-export.xml')

logger.debug('Creating MessageCollection')
mc = MessageCollection(xml_parser.messages_list)
logger.info(mc)
