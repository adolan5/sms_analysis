import logging
import re
from smsanalysis.message_collection import MessageCollection

logger = logging.getLogger(__name__)

class MessageAnalyzer:
    def __init__(self, messages, spacy_model=None):
        self.all_messages = messages
        self.spacy_model = spacy_model

    def get_message_tokens(self, lemmatize=False):
        sym = re.compile('[^A-Za-z -]')
        dashes = re.compile('[-/]')
        spaces = re.compile('[ ]{2,}')
        full_body = re.sub(sym, '', ' '.join([m.get('body') for m in self.all_messages if m.get('body') is not None]).lower())
        full_body = re.sub(dashes, ' ', full_body)
        full_body = re.sub(spaces, ' ', full_body)

        if lemmatize and self.spacy_model is not None:
            return [t.lemma_ for t in self.spacy_model(full_body)]
        else:
            return full_body.split(' ')

    def __repr__(self):
        return '<MessageAnalyzer|{} messages>'.format(len(self.all_messages))
