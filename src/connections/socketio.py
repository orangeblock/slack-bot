import Queue
import logging

from message import Message
from socketIO_client import SocketIO
from connections.base import BaseConnection

logger = logging.getLogger(__name__)

DEFAULT_NAME = 'awesomebot'

# This was used for a custom raw socket io connection and should be tweaked to work with different auth and message models.
class SocketIOConnection(BaseConnection):
    def __init__(self, bot_id=None, url=None, username=None, block_delay=.2):
        self.socket = None
        self.message_q = Queue.Queue()
        self.bot_id = bot_id
        self.url = url
        self.bot_name = username or DEFAULT_NAME
        self.block_delay = block_delay

    def connect(self):
        self.socket = SocketIO(self.url)
        logger.info('Socket IO connection successful')
        self._setup_callbacks()

    def _setup_callbacks(self):
        self.socket.on('chat message', self._handle_message)

    def _handle_message(self, data):
        try:
            if data['id'] != self.bot_id:
                self.message_q.put(data)
        except KeyError as ke:
            logger.debug('Message does not contain some fields: %s' % ke)

    def _message_stream(self):
        while True:
            self.socket.wait(self.block_delay)
            try:
                yield self.message_q.get(block=False)
            except Queue.Empty:
                pass

    def new_messages(self):
        for message in self._message_stream():
            try:
                yield Message(text=message['text'], user=message['id'])
            except KeyError as ke:
                logger.debug('Message missing some parameters: %s' % ke)

    def send_message(self, message, channel):
        data = {
            'text': message,
            'username': self.bot_name,
            'id': self.bot_id
        }
        logger.debug('Sending message to socket.io')
        self.socket.emit('chat message', data)

    def close(self):
        try:
            self.socket.disconnect()
        except Exception as e:
            logger.info("Socket.io connection close failed: %s" % e)
