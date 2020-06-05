import functions as fnc
import strings
import keyboard as kb
import inlineRealization as iRz

import threading
from telebot.types import Message
from BotSetup import app, bot, dataBase, loggerDEBUG
from BotSetup import Host, Port, NotificationMethod


STRING_SERVER = f'{Host}:{Port}{NotificationMethod}'
SERVER_GOOD_ANSWER = 'Notifications have been sent: total = {0}, passed = {1}'
SERVER_BAD_ANSWER = 'Error!'


@app.route(NotificationMethod, methods=['POST', 'GET'])
def listen_update():
    try:
        total, passed = fnc.sendNotif('')
        loggerDEBUG.debug(f'/setnew from SERVER')
        return SERVER_GOOD_ANSWER.format(total, passed)
    except:
        return SERVER_BAD_ANSWER


@bot.message_handler(commands=['start'])
def process_start_command(message: Message):
    dataBase.add_user(message.from_user.id, message.chat.id)
    dataBase.set_default_values(message.chat.id)
    bot.send_message(message.from_user.id,
                     strings.MESSAGE_START,
                     reply_markup=kb.determine_start_keyboard(dataBase.get_group(message.chat.id)))
    if message.from_user.username is None:
        loggerDEBUG.debug(f'/start None - {message.from_user.id}')
    else:
        loggerDEBUG.debug(f'/start {message.from_user.username} - {message.from_user.id}')


@bot.message_handler(commands=['setnew'])
def time_table_changed(message: Message):
    user_info = message.from_user
    if dataBase.is_admin(message.from_user.id):
        option = message.text.strip('/setnew ')
        fnc.sendNotif(option)
        loggerDEBUG.debug(
            f'/setnew {user_info.username if user_info.username else ""} - {user_info.id} - {option}'
        )
    else:
        loggerDEBUG.warning(
            '\n'.join(['/setnew ----- ВНИМАНИЕ!!! ',
                       'пользователь, НЕ ЯВЛЯЮЩИЙСЯ АДМИНОМ использовал /setnew',
                       f'chat_id: {user_info.id}',
                       f'username: {user_info.username if user_info.username else "empty username"}'])
        )


@bot.message_handler(commands=['help'])
def send_list_of_commands(message: Message):
    dataBase.add_user(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, strings.INSTROUCTIONS_HELP)
    if message.from_user.username is None:
        loggerDEBUG.debug(f'/help None - {message.from_user.id}')
    else:
        loggerDEBUG.debug(f'/help {message.from_user.username} - {message.from_user.id}')


@bot.message_handler(regexp=strings.SEARCH_BY_GROUP)
def choose_way_search_by_group(message: Message):
    loggerDEBUG.debug(f'{message.from_user.username} :: "ПОИСК ПО ГРУППЕ" :: start')
    dataBase.add_user(message.from_user.id, message.chat.id)
    dataBase.set_way(message.chat.id, 0)
    dataBase.set_count_parameters(message.chat.id, 0)
    bot.send_message(message.chat.id, 
                     strings.ENTER_GROUP, 
                     reply_markup=kb.determine_start_keyboard(dataBase.get_group(message.from_user.id)))
    loggerDEBUG.debug(f'{message.from_user.username} :: "ПОИСК ПО ГРУППЕ" :: end')


@bot.message_handler(regexp=strings.SEARCH_BY_TEACHER)
def choose_way_search_by_teacher(message: Message):
    loggerDEBUG.debug(f'{message.from_user.username} :: "ПОИСК ПО ПРЕПОДАВАТЕЛЮ" :: start')
    dataBase.add_user(message.from_user.id, message.chat.id)
    dataBase.set_way(message.chat.id, 1)
    dataBase.set_count_parameters(message.chat.id, 0)
    bot.send_message(message.chat.id, 
                     strings.ENTER_TEACHER, 
                     reply_markup=kb.determine_start_keyboard(dataBase.get_group(message.from_user.id)))
    loggerDEBUG.debug(f'{message.from_user.username} :: "ПОИСК ПО ПРЕПОДАВАТЕЛЮ" :: end')


@bot.message_handler(regexp=strings.SEARCH_ALL_TIME_TABLE)
def choose_way_all_time_table(message: Message):
    loggerDEBUG.debug(f'{message.from_user.username} :: "ВЫВОД ВСЕГО РАСПИСАНИЯ" :: start')
    dataBase.add_user(message.from_user.id, message.chat.id)
    dataBase.set_way(message.chat.id, 2)
    dataBase.set_count_parameters(message.chat.id, 0)
    fnc.general_func(message)
    loggerDEBUG.debug(f'{message.from_user.username} :: "ВЫВОД ВСЕГО РАСПИСАНИЯ" :: end')


@bot.message_handler(regexp=strings.SEARCH_BY_B209)
def choose_way_by_b209(message: Message):
    loggerDEBUG.debug(f'{message.from_user.username} :: "КОГДА СВОБОДНА Б209?" :: start')
    dataBase.add_user(message.from_user.id, message.chat.id)
    dataBase.set_way(message.chat.id, 3)
    dataBase.set_count_parameters(message.chat.id, 0)
    bot.send_message(message.chat.id, 
                     strings.ENTER_DATE_FOR_CURRENT_GROUP, 
                     reply_markup=kb.choiceDateForB209)
    loggerDEBUG.debug(f'{message.from_user.username} :: "КОГДА СВОБОДНА Б209?" :: end')


@bot.message_handler(content_types=['text'])
def repeat_message(message: Message):
    loggerDEBUG.debug(f'/text {message.from_user.username} :: start')
    dataBase.add_user(message.from_user.id, message.chat.id)

    #fnc.general_func(message)

    regExp = fnc.text_reg_exp(message.from_user.id)

    if regExp and message.text == regExp:
        bot.send_message(message.chat.id, strings.ENTER_DATE_FOR_CURRENT_GROUP,
                         reply_markup=kb.choiceDateForCurrentGroup)
        dataBase.set_way(message.chat.id, 10)
    else:
        fnc.general_func(message)

    loggerDEBUG.debug(f'/text {message.from_user.username} - {message.from_user.id} - "{message.text}" :: end')


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    loggerDEBUG.debug(f'QUERY: {query.query}')
    strOut = iRz.general_func(query)
    bot.answer_inline_query(query.id, strOut)


if __name__ == '__main__':
    threading.Thread(target=app.run, args=(Host, Port)).start()
    bot.polling(none_stop=True)
