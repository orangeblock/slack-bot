import os
import sys
import time
import json
import random
import logging
import requests
import websocket

from ssl import SSLError

BASE_URL = 'https://slack.com/api/'
rtm_url = lambda method: '%s%s' % (BASE_URL, method)
COUNTER = 0

def get_counter():
    global COUNTER
    COUNTER += 1
    return COUNTER

def _rtm_start(token):
    return requests.get(rtm_url('rtm.start'), params={"token": token}).json()

def _ws_start(ws_url):
    ws = websocket.create_connection(ws_url)
    ws.sock.setblocking(0)
    return ws

def start(token):
    conn_resource = _rtm_start(token)
    ws = _ws_start(conn_resource['url'])
    memes = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
    while True:
        try:
            obj = json.loads(ws.recv())
            if obj.get('type') == 'message':
                if 'text' in obj and '@%s' % conn_resource['self']['id'] in obj['text']:
                    logging.info('Received mention. Sending meme...')
                    ws.send(json.dumps({'id': get_counter(),'type': 'message', 'text': random.choice(memes)['url'], 'channel': obj['channel']}))
        except SSLError as ssle:
            pass
        except Exception as e:
            logging.info('Error: %s' % e)
        time.sleep(.2)


if __name__ == '__main__':
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=log_level)

    slack_token = os.getenv("SLACK_TOKEN")
    if slack_token:
        start(slack_token)
    else:
        logging.info("SLACK_TOKEN env var not set. Exiting...")
