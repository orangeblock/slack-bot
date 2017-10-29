import re
import requests
import logging

from base import BaseBot

logger = logging.getLogger(__name__)

COMMAND_REGEX = r'^!yt (.+)|^!youtube (.+)'
BASE_URL = 'https://www.youtube.com'
SEARCH_URL = '%s/results' % BASE_URL

def search_youtube(term, max_results=1):
    resp = requests.get(SEARCH_URL, params={'search_query': term})
    partials = re.findall(r'/watch\?v=[a-zA-Z0-9_-]+', resp.text)
    full = [BASE_URL + part for part in partials]
    return full[:min(max_results, len(full))]

class YoutubeBot(BaseBot):
    def __init__(self, connection=None):
        super(YoutubeBot, self).__init__(connection)

    def handle(self, message):
        m = re.match(COMMAND_REGEX, message.text)
        if m:
            term = m.group(1) or m.group(2)
            results = search_youtube(term, 1)
            if not results:
                response = 'No results :('
            else:
                response = results[0]
            self.connection.send_message(response, message.channel)
            return True
        return False
