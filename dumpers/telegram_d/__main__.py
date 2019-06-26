import logging

import socks
from telethon import TelegramClient, sync, client

logging.basicConfig(level=logging.INFO)

import json
from json.decoder import JSONDecodeError

configFile = open("D:/Projects/pycharm/RPiD/dumper/telegram/config.json", "r")
try:
    config = json.loads(configFile.read())
    configFile.close()
except JSONDecodeError as err:
    print(err.msg)
    exit(-1)


class Tg:
    def __init__(self, pathToSession):
        if (not "/" in pathToSession) or (not "\\" in pathToSession): pathToSession = config["app"]["defaultPathToSession"] + "/" + pathToSession
        self.client = TelegramClient(pathToSession, config["app"]["id"], config["app"]["hash"],
                                proxy=(socks.SOCKS5, config["proxy"]["host"], config["proxy"]["port"]))

