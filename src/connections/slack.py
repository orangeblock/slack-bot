import time
import json
import logging
import requests
import websocket

from ssl import SSLWantReadError, SSLError
from message import Message
from util import generate_counter
from connections.base import BaseConnection

logger = logging.getLogger(__name__)
SLACK_API_BASE = 'https://slack.com/api'
RTM_START_URL = '%s/rtm.start' % SLACK_API_BASE

class SlackConnection(BaseConnection):
    def __init__(self, oauth_token, read_delay=.2):
        self.token = oauth_token
        self.websocket = None
        self.conn_data = None
        self.bot_id = None
        self.bot_name = None
        self.read_delay = read_delay
        self.counter = generate_counter()

    def connect(self):
        rtm_response = requests.get(
            RTM_START_URL,
            params={'token': self.token, 'simple_latest': 'true', 'no_unreads': 'true'})
        if rtm_response.ok:
            logger.info('rtm.start response successful')
            self.conn_data = rtm_response.json()
            self.bot_id = self.conn_data['self']['id']
            self.bot_name = self.conn_data['self']['name']
            self._bind_ws(self.conn_data['url'])
        else:
            logger.debug('rtm.start failed with status %d' % rtm_response.status_code)
            raise SlackConnectError

    def _bind_ws(self, url):
        self.websocket = websocket.create_connection(self.conn_data['url'])
        self.websocket.sock.setblocking(0)
        self.conn_data['_ts_connected'] = time.time()
        logger.info('WS connection successful')

    def _ws_read(self):
        while True:
            try:
                yield self.websocket.recv()
            except SSLWantReadError as ssle:
                yield None

    def _stream_data(self):
        for data in self._ws_read():
            if data:
                yield json.loads(data)
            time.sleep(self.read_delay)

    def _ws_send(self, data):
        try:
            self.websocket.send(data)
        except SSLError as ssle:
            logger.debug('SSL error when trying to send data. Trying to reconnect...')
            self._connect()

    def new_messages(self):
        """Generator that streams messages received from Slack"""
        for obj in self._stream_data():
            try:
                if 'ts' in obj:
                    timestamp = float(obj['ts'])
                else:
                    timestamp = None
                if obj.get('type') == 'message' and timestamp > self.conn_data['_ts_connected']:
                    logger.debug('Received new message: %s' % obj)
                    yield Message(text=obj['text'], channel=obj['channel'], user=obj['user'], ts=timestamp)
            except KeyError as ke:
                logger.debug('Message missing some parameters: %s' % ke)
            except TypeError as te:
                logger.debug('Timestamp not in correct format')

    def send_message(self, message, channel):
        data = {
            'id': self.counter(),
            'type': 'message',
            'text': message,
            'channel': channel
        }
        logger.debug('Sending message in channel %s' % channel)
        self._ws_send(json.dumps(data))

    def close(self):
        try:
            self.websocket.close()
        except Exception as e:
            logger.info("Slack connection close failed: %s" % e)


class SlackConnectError(Exception):
    pass
