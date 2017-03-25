import os
import bots
import logging
import threading
import connections

logger = logging.getLogger(__name__)

def _run_handle_loop(connection, bots):
    for message in connection.new_messages():
        for bot in bots:
            responded = bot.handle(message)
            if responded:
                break

def run_slack_connection():
    slack_token = os.getenv("SLACK_TOKEN")
    if slack_token:
        connection = connections.SlackConnection(slack_token)
        bot_list = [bots.PupilBot(connection), bots.ChuckBot(connection), bots.MemeBot(connection)]
        _run_handle_loop(connection, bot_list)
    else:
        logger.info("SLACK_TOKEN env var not set. Exiting...")

def run_socketio_conenction():
    connection = connections.CustomChatConnection()
    bot_list = [bots.ChuckBot(connection), bots.MemeBot(connection)]
    _run_handle_loop(connection, bot_list)


if __name__ == '__main__':
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=log_level)

    threads = [
        threading.Thread(target=run_slack_connection, args=()),
        threading.Thread(target=run_socketio_conenction, args=())
    ]
    [t.start() for t in threads]
    [t.join() for t in threads]
