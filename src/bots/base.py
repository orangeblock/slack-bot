import logging

logger = logging.getLogger(__name__)

class BaseBot(object):
    def __init__(self, connection):
        self.connection = connection

    def _get_mention_string(self):
        return '<@%s>' % self.connection.bot_id

    def _mentioned(self, text):
        return self._get_mention_string() in text

    def help_message(self):
        return ''

    def handle(self, message):
        """
            Each bot must implement this method. 
            
            It returns False or None if the message is not intended for it,
            otherwise interacts with the connection and returns truthy.
        """
        return False
