import re
import logging

from base import BaseBot

logger = logging.getLogger(__name__)

TEACH_REGEX = re.compile(r'^!teach\s+"([^\n"]+)"\s*"([^\n"]+)"')
FORGET_REGEX = re.compile(r'^!forget')
HELP_REGEX = re.compile(r'^!teach\s+help')

class PupilBot(BaseBot):
    def __init__(self, connection, max_capacity=10):
        self.qa = []
        self.max_capacity = max_capacity
        super(PupilBot, self).__init__(connection)

    def help_message(self):
        return """I can store question/answer pairs and repeat the answer when asked a question!\n""" + \
               """`!teach \"<string>\" \"<string>\"` to teach me something new!\n""" + \
               """`!forget` and I will forget everything.\n""" + \
               """`@%s <string>` and I will answer if I can!""" % self.connection.bot_name

    def handle(self, message):
        return self.help(message) or \
               self.learn(message) or \
               self.answer(message) or \
               self.forget(message)

    def _find_answer(self, question):
        storable_question = self._get_storable_question(question)
        for pair in self.qa:
            if pair[0] == storable_question:
                return pair[1]
        return None

    def _get_storable_question(self, question):
        return question.strip().lower()

    def help(self, message):
        if re.match(HELP_REGEX, message.text):
            self.connection.send_message(self.help_message(), message.channel)
            return True
        return False

    def learn(self, message):
        match = re.match(TEACH_REGEX, message.text)
        if match:
            question, answer = match.groups()
            if self._find_answer(question):
                self.connection.send_message("I can already respond to that! :feelgood:", message.channel)
                return True
            response = ''
            if len(self.qa) >= self.max_capacity:
                del self.qa[0]
                response += "I can't remember more things, so I forgot the oldest one.\n"
            self.qa.append((self._get_storable_question(question), answer))
            response += 'Got it! I will now respond to "%s" with "%s"! :ok_hand:' % (question, answer)
            self.connection.send_message(response, message.channel)
            return True
        return False

    def forget(self, message):
        if re.match(FORGET_REGEX, message.text):
            self.qa = []
            self.connection.send_message("Forgot everything!", message.channel)
            return True
        return False

    def answer(self, message):
        if self._mentioned(message.text):
            answer = self._find_answer(message.text.replace(self._get_mention_string(), ''))
            if answer:
                self.connection.send_message(answer, message.channel)
                return True
        return False
