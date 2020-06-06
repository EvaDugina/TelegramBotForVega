import config
import logging
import telebot
import workWithDataBase as wDB

from workWithJSON import JsonFormatter, FileProvider, ServerProvider

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

Host = config.Host
Port = config.Port
NotificationMethod = config.NotificationMethod

for admin_id in config.admins:
    dataBase.add_admin(admin_id)

