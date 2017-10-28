class BaseConnection(object):
    def connect(self):
        """Connect to the server"""
        raise NotImplementedError

    def close(self):
        """Gracefully close the connection"""
        raise NotImplementedError

    def new_messages(self):
        """Streams messages from the server"""
        raise NotImplementedError

    def send_message(self, message, channel):
        """Send a message through the connection"""
        raise NotImplementedError
