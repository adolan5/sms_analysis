import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

from smsanalysis.message_analyzer import MessageAnalyzer
from smsanalysis.message_collection import MessageCollection
