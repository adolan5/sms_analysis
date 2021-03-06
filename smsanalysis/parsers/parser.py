import logging
import time
import phonenumbers
from smsanalysis import MessageCollection

logger = logging.getLogger(__name__)

class Parser:
    """The Parser class template.

    A Parser is meant to read raw SMS data out of its original form (however it
    is encoded) and produce a consistent, formatted version.
    """

    def __init__(self):
        self.read_time = 0
        self.contacts = None

    def read_messages(self, sms_source):
        """Read messages from one or more SMS export data sources and return them
        as a formatted list.

        First determine whether or not more than a single data source has been specified.
        """
        sms_source_list = [sms_source] if type(sms_source) is str else sms_source
        read_time_start = time.time()
        messages = MessageCollection()
        for source in sms_source_list:
            messages.extend(self._import_messages(source))
        read_time_end = time.time()
        self.read_time = read_time_end - read_time_start
        logger.debug('Read {} messages in {} seconds'.format(len(messages), self.read_time))
        if self.contacts is not None:
            messages.set_contacts(self.contacts)
        return messages


    def _import_messages(self, sms_source_list):
        """Read SMS message data from file(s) with specific format.

        This is the main functionality of a parser. Parser implementations must
        implement this function.
        """
        pass

    # TODO: Issue here with non-numbers like '#CMAS#CMASALL' - displayed as SMS (even though it isn't)
    def _format_number(self, number, region='US'):
        try:
            original_number = phonenumbers.parse(number, region)
            formatted_number = phonenumbers.format_number(original_number, phonenumbers.PhoneNumberFormat.E164)
        except:
            logger.warning('Failed to convert number: {}'.format(number))
            formatted_number = number
        return formatted_number
