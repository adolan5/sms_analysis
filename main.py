import logging
import spacy
from smsanalysis import MessageAnalyzer

logging.basicConfig()
logging.getLogger('smsanalysis').setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.debug('Loading spacy model')
# spacy_model = spacy.load('en_core_web_lg', disable=['parse', 'ner'])
spacy_model = spacy.load('en_core_web_sm', disable=['parse', 'ner'])

logger.debug('Creating MessageAnalyzer')
ma = MessageAnalyzer('./data/sms-export.xml')
# ma = message_analyzer('./sms-text-only.xml')
logger.info(ma)
