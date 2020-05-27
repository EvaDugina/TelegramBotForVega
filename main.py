import config
import functions as fnc
import strings
import keyboard as kb
import inlineRealization as iRz
import workWithDataBase as wDB

from flask import Flask
import threading
import telebot
from telebot.types import Message
import logging


# TOKEN = os.environ.get('TELEGRAM_BOT_FOR_VEGA_TOKEN')
TOKEN = config.token
LOG_FORMAT = '%(asctime)s :: %(funcName)s :: %(message)s'
STRING_SERVER = f'{config.Host}:{config.Port}/{config.NotificationMethod}'
STRING_RETURN = ''

bot = telebot.TeleBot(TOKEN)
loggerDEBUG = logging.getLogger('logger_debug')
loggerDEBUG.setLevel('DEBUG')

logging.getLogger('urllib3').setLevel('ERROR')
logging.getLogger('TeleBot').setLevel('ERROR')
logging.getLogger('socks').setLevel('ERROR')
logging.getLogger('requests').setLevel('ERROR')

dataBase = wDB.FileDBWork("USERS_DATA_BASE.db", "ADMINS_DATA_BASE.db")
logging.basicConfig(level='DEBUG', filename='log.txt', format=LOG_FORMAT)


app = Flask(__name__)


@app.route(config.NotificationMethod, methods=['POST', 'GET'])
def listen_update():
    fnc.sendNotif('')
    loggerDEBUG.debug(f'/setnew from SERVER')
    return STRING_RETURN


@bot.message_handler(commands=['start'])
def process_start_command(message: Message):
    dataBase.add_user(user_id=message.from_user.id, chat_id=message.chat.id)
    row = dataBase.get_row_by_id(message.from_user.id)
    listRow = fnc.row_to_list(row)
    listRow[3] = -1
    listRow[4] = 0
    listRow[5] = ''
    listRow[6] = ''
    dataBase.edit_row(listRow[0], listRow)
    bot.send_message(message.from_user.id, strings.MESSAGE_START, reply_markup=kb.determine_start_keyboard(listRow[5]))
    if message.from_user.username is None:
        loggerDEBUG.debug(f'/start None - {message.from_user.id}')
    else:
        loggerDEBUG.debug(f'/start {message.from_user.username} - {message.from_user.id}')


@bot.message_handler(commands=['setnew'])
def time_table_changed(message: Message):
    if fnc.isAdmin(message.from_user.id):
        s = message.text.split(' ')
        option = ''
        if len(s) > 1:
            for i in range(1, len(s)):
                option += s[i] + ' '
        fnc.sendNotif(option)
        if message.from_user.username is None:
            loggerDEBUG.debug(f'/setnew None - {message.from_user.id} - {option}')
        else:
            loggerDEBUG.debug(f'/setnew {message.from_user.username} - {message.from_user.id} - {option}')
    else:
        if message.from_user.username is None:
            loggerDEBUG.warning('\n'.join([f'/setnew ----- ВНИМАНИЕ!!! ',
                                           f'пользователь, НЕ ЯВЛЯЮЩИЙСЯ АДМИНОМ использовал /setnew',
                                           f'chat_id: {message.from_user.id}',
                                           f'username: None']))
        else:
            loggerDEBUG.warning('\n'.join([f'/setnew ----- ВНИМАНИЕ!!! ',
                                       f'пользователь, НЕ ЯВЛЯЮЩИЙСЯ АДМИНОМ использовал /setnew',
                                       f'chat_id: {message.from_user.id}',
                                       f'username: {message.from_user.username}']))


@bot.message_handler(commands=['help'])
def send_list_of_commands(message: Message):
    dataBase.add_user(user_id=message.from_user.id, chat_id=message.chat.id)
    bot.send_message(message.chat.id, strings.INSTROUCTIONS_HELP)
    if message.from_user.username is None:
        loggerDEBUG.debug(f'/help None - {message.from_user.id}')
    else:
        loggerDEBUG.debug(f'/help {message.from_user.username} - {message.from_user.id}')


@bot.message_handler(regexp=strings.SEARCH_BY_GROUP)
def choose_way_search_by_group(message: Message):
    loggerDEBUG.debug(f'поиск по группе {message.from_user.username} :: start')
    dataBase.add_user(user_id=message.from_user.id, chat_id=message.chat.id)
    row = dataBase.get_row_by_id(message.from_user.id)
    listRow = fnc.row_to_list(row)
    listRow[3] = 0
    listRow[4] = 0
    dataBase.edit_row(listRow[0], listRow)
    bot.send_message(message.chat.id, strings.ENTER_GROUP)
    loggerDEBUG.debug(f'поиск по группе {message.from_user.username} :: end')


@bot.message_handler(regexp=strings.SEARCH_BY_TEACHER)
def choose_way_search_by_teacher(message: Message):
    loggerDEBUG.debug(f'поиск по преподавателю {message.from_user.username} :: start')
    dataBase.add_user(user_id=message.from_user.id, chat_id=message.chat.id)
    row = dataBase.get_row_by_id(message.from_user.id)
    listRow = fnc.row_to_list(row)
    listRow[3] = 1
    listRow[4] = 0
    dataBase.edit_row(listRow[0], listRow)
    bot.send_message(message.chat.id, strings.ENTER_TEACHER)
    loggerDEBUG.debug(f'поиск по группе {message.from_user.username} :: end')


@bot.message_handler(regexp=strings.SEARCH_ALL_TIME_TABLE)
def choose_way_all_time_table(message: Message):
    loggerDEBUG.debug(f'вывод всего расписания {message.from_user.username}')
    dataBase.add_user(user_id=message.from_user.id, chat_id=message.chat.id)
    row = dataBase.get_row_by_id(message.from_user.id)
    listRow = fnc.row_to_list(row)
    listRow[3] = 2
    listRow[4] = 0
    dataBase.edit_row(listRow[0], listRow)
    fnc.general_func(message)


@bot.message_handler(regexp=strings.SEARCH_BY_B209)
def choose_way_by_b209(message: Message):
    loggerDEBUG.debug(f'когда свободна Б209? {message.from_user.username} :: start')
    dataBase.add_user(user_id=message.from_user.id, chat_id=message.chat.id)
    row = dataBase.get_row_by_id(message.from_user.id)
    listRow = fnc.row_to_list(row)
    listRow[3] = 3
    listRow[4] = 0
    dataBase.edit_row(listRow[0], listRow)
    fnc.general_func(message)
    loggerDEBUG.debug(f'когда свободна Б209? {message.from_user.username} :: end')


@bot.message_handler(content_types=['text'])
def repeat_message(message: Message):
    loggerDEBUG.debug(f'/text {message.from_user.username} :: start')
    dataBase.add_user(user_id=message.from_user.id, chat_id=message.chat.id)
    regExp = fnc.text_reg_exp(message.from_user.id)

    if regExp != 'ERROR' and message.text == regExp:
        bot.send_message(message.chat.id, fnc.group_one_parameter(message.chat.id, '1'))
        row = dataBase.get_row_by_id(message.from_user.id)
        listRow = fnc.row_to_list(row)
        listRow[3] = -1
        dataBase.edit_row(listRow[0], listRow)
    else:
        fnc.general_func(message)

    if message.from_user.username is None:
        loggerDEBUG.debug(f'/text None - {message.from_user.id} - "{message.text}" :: end')
    else:
        loggerDEBUG.debug(f'/text {message.from_user.username} - {message.from_user.id} - "{message.text}" :: end')


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    loggerDEBUG.debug(f'QUERY: {query.query}')
    strOut = iRz.general_func(query)
    bot.answer_inline_query(query.id, strOut)


if __name__ == '__main__':
    threading.Thread(target=app.run, args=(config.Host, config.Port)).start()
    bot.polling(none_stop=True)
