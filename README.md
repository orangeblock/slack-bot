An easily extensible framework for building Slack bots. Built from scratch using WebSockets.

## Requirements
Python 2.7+. Packages are in `requirements.txt`. Install them by running `pip install -r requirements.txt` from the root of this repo. You might not have the required distro libraries needed for lxml so make sure you get them first. I have a Dockerfile that will work for Ubuntu 14+, so just copy and run the apt command. lxml is not strictly needed but one of the bots requires it. You can remove dependency on the bot and not have to deal with that headache ;)  

As long as you can satisfy all the Python reqs you can use any OS you want but the following instructions are for Ubuntu 14+.

## Setup
Replace all instances of `<bot-token-here>` with the token obtained after creating a slack bot account.  

Clone the repository and then:  
```bash
cd slack-bot
export SLACK_TOKEN=<bot-token-here>
python ./src/app.py
```

Of course, you probably want to run this in the background, so you can create a systemd service very easily:
```
[Unit]
Description=Slack Bot
After=network.target

[Service]
Type=simple
User=root
Environment=SLACK_TOKEN=<bot-token-here>
WorkingDirectory=/path/to/slack-bot
ExecStart=/usr/bin/python src/app.py
Restart=on-abort

[Install]
WantedBy=multi-user.target
```
Save this in `/etc/systemd/system/slack-bot.service`, reload the daemon with `systemctl daemon-reload` and you're good to run the service using `systemctl start slack-bot.service`.  
  
You can view logs using `journalctl -fu slack-bot.service`.  

If you have Docker installed you can also use the Dockerfile in this directory to build the environment. You will need to inject the token in the container. I haven't deployed this using Docker myself but I've used a third party service in the past that required a Dockerfile to setup a container and it worked fine.

## Usage
Look into `src/bots/` for existing bot implementations. You can easily build your own and hook it up in `src/app.py` to make your bot respond to a different command.

Invite the bot in a channel or a group discussion, or send messages directly to it in a PM. It will pick up all sent messages and pass them through all bot handlers. Only one bot can respond to a message, so keep that in mind when you order the bots in app.py.

This project was made just for fun and you can use and extend it freely.
