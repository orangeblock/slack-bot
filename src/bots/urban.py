import re
import requests
import logging

from base import BaseBot
from lxml import html

logger = logging.getLogger(__name__)

COMMAND_REGEX = r'^!urban (.+)'
SEARCH_URL = 'https://www.urbandictionary.com/define.php'

def search_urban(term, max_results=1):
    resp = requests.get(SEARCH_URL, params={'term': term})
    tree = html.fromstring(resp.content)
    results = tree.xpath('//div[@data-defid]')
    if len(results) < max_results:
        max_results = len(results)
    responses = []
    for i in range(max_results):
        meaning = results[i].xpath('div[@class="meaning"]')
        if meaning:
            responses.append(meaning[0].text_content().strip('\n'))
    return responses

class UrbanBot(BaseBot):
    def __init__(self, connection=None):
        super(UrbanBot, self).__init__(connection)

    def handle(self, message):
        m = re.match(COMMAND_REGEX, message.text)
        if m:
            results = search_urban(m.group(1), 1)
            if not results:
                response = 'No results :('
            else:
                response = results[0]
            self.connection.send_message(response, message.channel)
            return True
        return False
