import re
import time
import random
import logging
import requests

from base import BaseBot

logger = logging.getLogger(__name__)

MEME_URL = 'http://www.memes.com'
MEME_REGEX = re.compile(r'^!meme')
SCRAPE_REGEX = re.compile(r'<img id="image_\d+" src="([^"]+)"')

def random_meme():
    try:
        html = requests.get('%s/random' % MEME_URL).text
        urls = re.findall(SCRAPE_REGEX, html)
        if urls:
            return random.choice(urls).replace('/tile', '')
        else:
            logger.info("Meme scrape regex not working")
            return None
    except Exception as e:
        logger.info("Error retrieving meme: %s" % e)
        return None

class MemeBot(BaseBot):
    def __init__(self, connection, delay=60):
        self.delay = delay
        self.allowed_chans = ['G', 'D']
        self.ts_last_sent = 0
        super(MemeBot, self).__init__(connection)

    def _is_too_soon(self):
        ts = time.time()
        if int(ts - self.ts_last_sent) < self.delay:
            return True
        return False

    def handle(self, message):
        if message.channel[0] not in self.allowed_chans:
            return False
        if re.match(MEME_REGEX, message.text):
            if self._is_too_soon():
                self.connection.send_message('You have to wait %d seconds :simple_smile:' % self.delay, message.channel)
                return True
            meme_url = random_meme()
            if not meme_url:
                response = 'Something went wrong :disappointed:'
            else:
                response = meme_url
            self.connection.send_message(response, message.channel)
            self.ts_last_sent = time.time()
            return True
        return False
