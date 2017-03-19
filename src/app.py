import os
import bots
import logging
import connection


if __name__ == '__main__':
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=log_level)

    slack_token = os.getenv("SLACK_TOKEN")
    if slack_token:
        connection = connection.SlackConnection(slack_token)
        bots = [bots.PupilBot(connection), bots.ChuckBot(connection), bots.MemeBot(connection)]
        for message in connection.new_messages():    
            for bot in bots:
                responded = bot.handle(message)
                if responded:
                    break
    else:
        logging.info("SLACK_TOKEN env var not set. Exiting...")
