import logging
import time

logger = logging.getLogger(__name__)

class Parser:
    """The Parser class template.

    A Parser is meant to read raw SMS data out of its original form (however it
    is encoded) and produce a consistent, formatted version.
    """

    def __init__(self, sms_source):
        read_time_start = time.time()
        messages_list = self._import_messages(sms_source)
        read_time_end = time.time()
        read_time = read_time_end - read_time_start
        logger.debug('Read {} messages in {} seconds'.format(len(messages_list), read_time))

    def _import_messages(self, sms_source):
        """Read messages from the SMS export data source.

        This is the main functionality of a parser. Parser implementations must
        implement this function.
        """
        pass
