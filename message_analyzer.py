import nltk
import os
import xml.etree.ElementTree as ET

class message_analyzer:
    def __init__(self, sms_export):
        if not os.path.exists(sms_export):
            raise Exception('Argument must be a path to an sms export')
        tree = ET.parse(sms_export)
        root = tree.getroot()
        self.all_messages = list(root)
