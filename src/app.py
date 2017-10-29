import os
import bots
import time
import logging
import threading

from connections import SlackConnection, SocketIOConnection

logger = logging.getLogger(__name__)

WAIT_DURATION = 60
SLACK_TOKEN_ENV = 'SLACK_TOKEN'

def run_connection(connection, bots):
    bots = [bot(connection) for bot in bots]
    while True:
        try:
            connection.connect()
            for message in connection.new_messages():
                for bot in bots:
                    responded = bot.handle(message)
                    if responded:
                        break
        except Exception as e:
            logger.info("Unhandled error: %s" % e)
            connection.close()
        logger.info('Waiting %d seconds and retrying...' % WAIT_DURATION)
        time.sleep(WAIT_DURATION)

if __name__ == '__main__':
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=log_level)

    slack_token = os.getenv(SLACK_TOKEN_ENV)
    if slack_token is None:
        raise Exception('Slack token is missing. Set %s env variable.' % SLACK_TOKEN_ENV)

    threads = [
        threading.Thread(
            target=run_connection,
            args=(
                SlackConnection(slack_token),
                [bots.PupilBot, bots.ChuckBot, bots.MemeBot, bots.UrbanBot, bots.YoutubeBot])),
    ]
    [t.start() for t in threads]
    [t.join() for t in threads]
