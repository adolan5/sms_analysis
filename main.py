import logging
from smsanalysis import MessageAnalyzer

logging.basicConfig()
logging.getLogger('smsanalysis').setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ma = MessageAnalyzer('./data/sms-export.xml')
# ma = message_analyzer('./sms-text-only.xml')
logger.info(ma)
