import logging

logger = logging.getLogger(__name__)

class BaseBot(object):
    def __init__(self, connection=None):
        self.connection = connection

    def help_message(self):
        return ''

    def handle(self, message):
        """
            Each bot must implement this method.

            It returns False or None if the message is not intended for it,
            otherwise interacts with the connection and returns truthy.
        """
        return False
