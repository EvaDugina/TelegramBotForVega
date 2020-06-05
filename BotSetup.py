import config
import logging
import telebot
import workWithDataBase as wDB

from enum import Enum
from flask import Flask
from workWithJSON import JsonFormatter, FileProvider, ServerProvider


class States(Enum):
    MAIN = -1
    GROUP_SEARCH = 0
    TEACHER_SEARCH = 1
    FULL_TIMETABLE = 2
    BEST_ROOM = 3
    CURRENT_GROUP_SEARCH = 10


TOKEN = config.token
bot = telebot.TeleBot(TOKEN)

LOG_FORMAT = '%(asctime)s :: %(funcName)s :: %(message)s'

loggerDEBUG = logging.getLogger('logger_debug')
loggerDEBUG.setLevel('DEBUG')

logging.getLogger('urllib3').setLevel('ERROR')
logging.getLogger('TeleBot').setLevel('ERROR')
logging.getLogger('socks').setLevel('ERROR')
logging.getLogger('requests').setLevel('ERROR')

logging.basicConfig(level='DEBUG', filename='log.txt', format=LOG_FORMAT)

dataBase = wDB.DBWorker("USERS_DATA_BASE.db", "ADMINS_DATA_BASE.db")

jsonFormatter = JsonFormatter(FileProvider(config.dateFileJSON))

app = Flask(__name__)

Host = config.Host
Port = config.Port
NotificationMethod = config.NotificationMethod

