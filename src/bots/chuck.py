import re
import requests
import logging

from base import BaseBot
from HTMLParser import HTMLParser

logger = logging.getLogger(__name__)
html_parser = HTMLParser()

CHUCK_API_URL = 'http://api.icndb.com'
CHUCK_REGEX = re.compile(r'^!chuck')

def random_chuck_fact():
    try:
        fact = requests.get('%s/jokes/random' % CHUCK_API_URL.rstrip('/')).json()
        return html_parser.unescape(fact['value']['joke'])
    except Exception as e:
        logger.info('Error while retrieving Chuck Norris facts: %s' % e)
        return None

class ChuckBot(BaseBot):
    def __init__(self, connection=None):
        super(ChuckBot, self).__init__(connection)

    def handle(self, message):
        if re.match(CHUCK_REGEX, message.text):
            fact = random_chuck_fact()
            if not fact:
                response = "Can't find any facts :("
            else:
                response = fact
            self.connection.send_message(response, message.channel)
            return True
        return False
