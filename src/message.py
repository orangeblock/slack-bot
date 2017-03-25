import json

class Message:
    def __init__(self, text=None, channel=None, user=None, ts=None):
        self.text = text
        self.channel = channel
        self.user = user
        self.ts = ts

    def __str__(self):
        return json.dumps({
            'text': self.text, 
            'channel': self.channel, 
            'user': self.user,
            'timestamp': self.ts}, indent=2)

    def __repr__(self):
        return self.__str__()
