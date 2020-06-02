import workWithJSON as wJSON
import keyboard as kb
import main
from main import dataBase
import strings
import config

import time
import datetime
import telebot
from telebot.types import Message

bot = telebot.TeleBot(config.token)
jsonFormatter = wJSON.JsonFormatter(wJSON.FileProvider("dataTest.json"))


def general_func(message: Message):
    # Обработка выбора пути с ReplyKeyboardMarkup
    way = dataBase.get_way(message.chat.id)
    countParam = dataBase.get_count_parameters(message.chat.id)

    # Работа с выводом информации--------------
    if way == 10:
        stringOut = current_group_zero_parameters(message.chat.id, message.text)
        if stringOut != 'ERROR' and stringOut != '':
            bot.send_message(message.chat.id, stringOut, reply_markup=kb.determine_start_keyboard(dataBase.get_group(message.chat.id)))
        else:
            bot.send_message(message.chat.id, strings.MESSAGE_ERROR_TEXT, reply_markup=kb.determine_start_keyboard(dataBase.get_group(message.chat.id)))
        dataBase.set_way(message.chat.id, -1)
        bot.send_message(message.chat.id, strings.MESSAGE_ONE_OF_LIST_COMMANDS,
                         reply_markup=kb.determine_start_keyboard(dataBase.get_group(message.chat.id)))

    elif way == 0:
        if countParam == 0:
            stringOut = group_zero_parameters(message.chat.id, message.text)
            if stringOut == strings.MESSAGE_ERROR_GROUP or stringOut == strings.MESSAGE_ERROR_DATE:
                bot.send_message(message.chat.id, stringOut)
                if dataBase.get_group(message.chat.id) != '':
                    bot.send_message(message.chat.id, f'\nТЕКУЩАЯ ГРУППА: {dataBase.get_group(message.chat.id)}')
            elif not stringOut == '' and stringOut is not None:
                bot.send_message(message.chat.id, stringOut)
                if dataBase.get_group(message.chat.id) != '':
                    bot.send_message(message.chat.id,
                                     strings.MESSAGE_ONLY_DATE_GROUP + f'\nТЕКУЩАЯ ГРУППА: {dataBase.get_group(message.chat.id)}',
                                     reply_markup=kb.determine_start_keyboard(dataBase.get_group(message.chat.id)))
            dataBase.set_way(message.chat.id, -1)
            bot.send_message(message.chat.id, strings.MESSAGE_ONE_OF_LIST_COMMANDS,
                             reply_markup=kb.determine_start_keyboard(dataBase.get_group(message.chat.id)))

    elif way == 1:
        if countParam == 0:
            stringOut = teacher_zero_parameters(message.chat.id, message.text)
            if stringOut == strings.MESSAGE_ERROR_TEACHER or stringOut == strings.MESSAGE_ERROR_DATE:
                bot.send_message(message.chat.id, stringOut)
                if dataBase.get_teacher(message.chat.id) != '':
                    bot.send_message(message.chat.id, f'\nТЕКУЩИЙ ПРЕПОДАВАТЕЛЬ: {dataBase.get_teacher(message.chat.id)}')
            elif not stringOut == '' and stringOut is not None:
                bot.send_message(message.chat.id, stringOut)
                if dataBase.get_teacher(message.chat.id) != '':
                    bot.send_message(message.chat.id,
                                     strings.MESSAGE_ONLY_DATE_TEACHER + f'\nТЕКУЩИЙ ПРЕПОДАВАТЕЛЬ: {dataBase.get_teacher(message.chat.id)}')
            dataBase.set_way(message.chat.id, -1)
            bot.send_message(message.chat.id, strings.MESSAGE_ONE_OF_LIST_COMMANDS,
                             reply_markup=kb.determine_start_keyboard(dataBase.get_group(message.chat.id)))

    elif way == 2:
        if countParam == 0:
            bot.send_message(message.chat.id, strings.ENTER_COURSE_YEAR,
                             reply_markup=kb.choiceCourse)
            dataBase.set_count_parameters(message.chat.id, dataBase.get_count_parameters(message.chat.id) + 1)
        elif countParam == 1:
            catch = catching_stupid_in_third(message.text)
            if not catch:
                strOut = all_time_table_one_parameters(message)
                if message.text == 'выйти':
                    pass
                else:
                    ln = len(strOut)
                    if ln == 6:
                        for i, sOut in enumerate(strOut):
                            bot.send_message(message.chat.id, sOut) if not sOut == '' else print()
                    else:
                        bot.send_message(message.chat.id, strOut)
            else:
                #main.loggerDEBUG.debug('вывод всего расписания (null)')
                bot.send_message(message.chat.id, strings.MESSAGE_ERROR_ALL_TIME_TABLE)
            dataBase.set_way(message.chat.id, -1)
            bot.send_message(message.chat.id, strings.MESSAGE_ONE_OF_LIST_COMMANDS,
                             reply_markup=kb.determine_start_keyboard(dataBase.get_group(message.chat.id)))

    elif way == 3:
        #main.loggerDEBUG.debug('когда свободна Б-209? (0)')
        if message.text == 'Сегодня':
            date = datetime.datetime.today()
            bot.send_message(message.chat.id,
                             jsonFormatter.when_b209_is_free_by_date(jsonFormatter.week_to_string(date.weekday())))
        elif message.text == 'На неделе':
            bot.send_message(message.chat.id, jsonFormatter.when_b209_is_free())
        else:
            try:
                arrayData = data_to_array(message.text)
                date = datetime.datetime(int(arrayData[2]), int(arrayData[1]), int(arrayData[0]))
                strOut = jsonFormatter.when_b209_is_free_by_date(jsonFormatter.week_to_string(date.weekday()))
                bot.send_message(message.chat.id, strOut)
            except:
                bot.send_message(message.chat.id, strings.MESSAGE_ERROR_DATE)

        dataBase.set_way(message.chat.id, -1)
        bot.send_message(message.chat.id, strings.MESSAGE_ONE_OF_LIST_COMMANDS,
                         reply_markup=kb.determine_start_keyboard(dataBase.get_group(message.chat.id)))

    else:
        bot.send_message(message.chat.id, strings.MESSAGE_ERROR_TEXT)


def current_group_zero_parameters(chat_id, text):
    #main.loggerDEBUG.debug('Текущая группа (0)')
    if text == 'На сегодня':
        return group_one_parameter(chat_id, '1')
    elif text == 'На завтра':
        return group_one_parameter(chat_id, '2')
    elif text == 'На неделю':
        return group_one_parameter(chat_id, '7')
    else:
        return group_one_parameter(chat_id, text)


def group_zero_parameters(chat_id, text):
    #main.loggerDEBUG.debug('поиск по группе (0)')
    arrayGroupDate = text.split(' ')
    if text == "Поиск по группе":
        pass
    elif len(arrayGroupDate) == 1 or len(arrayGroupDate) == 3:
        gr = jsonFormatter.search_group(text)
        strOut = group_one_parameter(chat_id, arrayGroupDate[0])
        if not gr == 'ERROR':
            dataBase.set_name_group(chat_id, jsonFormatter.text_to_group(text).upper())
            return group_one_parameter(chat_id, '1')
        elif strOut != strings.MESSAGE_ERROR_GROUP and strOut != strings.MESSAGE_ERROR_TEXT \
                and strOut != strings.MESSAGE_ERROR_DATE:
            if len(arrayGroupDate) == 1:
                if strOut == strings.MESSAGE_ERROR_DATE:
                    bot.send_message(chat_id, strings.MESSAGE_ERROR_DATE)
                    return ''
                else:
                    return strOut
            strDate = '.'.join([arrayGroupDate[1], arrayGroupDate[2]])
            strOut = group_one_parameter(chat_id, strDate)
            if strOut == strings.MESSAGE_ERROR_DATE:
                bot.send_message(chat_id, strings.MESSAGE_ERROR_DATE)
                return ''
            else:
                return strOut
        strOut = group_zero_parameters(chat_id, arrayGroupDate[0])
        if strOut != strings.MESSAGE_ERROR_GROUP and strOut != '':
            strDate = '.'.join([arrayGroupDate[1], arrayGroupDate[2]])
            strOut = group_one_parameter(chat_id, strDate)
            if strOut == strings.MESSAGE_ERROR_DATE:
                bot.send_message(chat_id, strings.MESSAGE_ERROR_DATE)
                return ''
            else:
                return strOut
        elif not text == strings.SEARCH_BY_GROUP:
            return strings.MESSAGE_ERROR_GROUP
        else:
            return ''
    elif len(arrayGroupDate) == 2:
        date = group_one_parameter(chat_id, text)
        strOut = group_zero_parameters(chat_id, arrayGroupDate[0])
        if date != strings.MESSAGE_ERROR_DATE:
            return date
        elif date != strings.MESSAGE_ERROR_GROUP and strOut != '':
            return group_one_parameter(chat_id, arrayGroupDate[1])
        else:
            bot.send_message(chat_id, date)
            return ''
    elif len(arrayGroupDate) == 4:
        strOut = group_zero_parameters(chat_id, arrayGroupDate[0] + arrayGroupDate[1] + arrayGroupDate[2])
        if strOut != strings.MESSAGE_ERROR_GROUP and strOut != '':
            strGroup = arrayGroupDate[0] + arrayGroupDate[1] + arrayGroupDate[2]
            strOut = group_zero_parameters(chat_id, strGroup)
            if strOut == strings.MESSAGE_ERROR_GROUP or strOut == '':
                bot.send_message(chat_id, strings.MESSAGE_ERROR_GROUP)
                return ''
            else:
                return group_one_parameter(chat_id, arrayGroupDate[3])
        else:
            bot.send_message(chat_id, strings.MESSAGE_ERROR_TEXT)
            return ''
    elif len(arrayGroupDate) == 5:
        strGroupCheck = arrayGroupDate[0] + arrayGroupDate[1] + arrayGroupDate[2]
        strDate = '.'.join([arrayGroupDate[3], arrayGroupDate[4]])
        grZerPar = group_zero_parameters(chat_id, strGroupCheck)
        if grZerPar != strings.MESSAGE_ERROR_GROUP and grZerPar != '' \
                and group_one_parameter(chat_id, strDate) != strings.MESSAGE_ERROR_DATE:
            return group_one_parameter(chat_id, strDate)
        else:
            bot.send_message(chat_id, strings.MESSAGE_ERROR_TEXT)
            return ''
    else:
        return ''


def group_one_parameter(chat_id, text):
    #main.loggerDEBUG.debug('поиск по группе (1)')
    if text == '1':
        date = datetime.datetime.today()
        group = jsonFormatter.search_by_group_and_date(dataBase.get_group(chat_id),
                                                       jsonFormatter.week_to_string(date.weekday()))
        return group
    elif text == '2':
        date = datetime.datetime.today() + datetime.timedelta(days=1)
        group = jsonFormatter.search_by_group_and_date(dataBase.get_group(chat_id),
                                                       jsonFormatter.week_to_string(date.weekday()))
        return group
    elif text == '7':
        group = jsonFormatter.search_by_group(dataBase.get_group(chat_id))
        return group
    try:
        arrayData = data_to_array(text)
        date = datetime.datetime(int(arrayData[2]), int(arrayData[1]), int(arrayData[0]))
        group = jsonFormatter.search_by_group_and_date(dataBase.get_group(chat_id), jsonFormatter.week_to_string(date.weekday()))
        return group
    except:
        if dataBase.get_group(chat_id) == '':
            return strings.MESSAGE_ERROR_GROUP
        return strings.MESSAGE_ERROR_DATE


def teacher_zero_parameters(chat_id, text):
    #main.loggerDEBUG.debug('поиск по преподавателю (0)')
    arrayTeacherDate = text.split(' ')
    if text == "Поиск по преподавателю":
        pass
    elif len(arrayTeacherDate) == 1:
        tch = jsonFormatter.search_subject(text)
        date = teacher_one_parameter(chat_id, text)
        if not tch == 'ERROR':
            dataBase.set_name_teacher(chat_id, text.upper())
            return teacher_one_parameter(chat_id, '1')
        elif date != strings.MESSAGE_ERROR_DATE or text == strings.SEARCH_BY_TEACHER:
            return date
        else:
            return strings.MESSAGE_ERROR_TEXT
    elif len(arrayTeacherDate) == 2:
        date = teacher_one_parameter(chat_id, text)
        tch = teacher_zero_parameters(chat_id, arrayTeacherDate[0])
        if tch != strings.MESSAGE_ERROR_TEACHER and tch != '' and tch != strings.MESSAGE_ERROR_TEXT:
            return teacher_one_parameter(chat_id, arrayTeacherDate[1])
        elif date != strings.MESSAGE_ERROR_DATE:
            return date
        elif date == strings.MESSAGE_ERROR_DATE:
            return date
        elif teacher_zero_parameters(chat_id, arrayTeacherDate[0]) == strings.MESSAGE_ERROR_TEACHER:
            return strings.MESSAGE_ERROR_TEACHER
        else:
            return ''
    elif len(arrayTeacherDate) == 3:
        tch = teacher_zero_parameters(chat_id, arrayTeacherDate[0])
        if tch != strings.MESSAGE_ERROR_TEACHER and tch != '' and tch != strings.MESSAGE_ERROR_TEXT:
            strDate = '.'.join([arrayTeacherDate[1], arrayTeacherDate[2]])
            strOut = teacher_one_parameter(chat_id, strDate)
            if strOut == strings.MESSAGE_ERROR_DATE:
                bot.send_message(chat_id, strings.MESSAGE_ERROR_DATE)
                return ''
            else:
                return strOut
        else:
            bot.send_message(chat_id, strings.MESSAGE_ERROR_TEXT)
            return ''
    else:
        return ''


def teacher_one_parameter(chat_id, text):
    #main.loggerDEBUG.debug('поиск по преподавателю (1)')
    if text == '1':
        date = datetime.datetime.today()
        teacher = jsonFormatter.search_by_teacher_and_date(dataBase.get_teacher(chat_id), jsonFormatter.week_to_string(date.weekday()))
        return teacher
    elif text == '7':
        teacher = jsonFormatter.search_by_teacher(dataBase.get_teacher(chat_id))
        return teacher
    else:
        try:
            arrayData = data_to_array(text)
            date = datetime.datetime(int(arrayData[2]), int(arrayData[1]), int(arrayData[0]))
            teacher = jsonFormatter.search_by_teacher_and_date(dataBase.get_teacher(chat_id), jsonFormatter.week_to_string(date.weekday()))
            return teacher
        except:
            if dataBase.get_group(chat_id) == '':
                return strings.MESSAGE_ERROR_TEACHER
            return strings.MESSAGE_ERROR_DATE


def all_time_table_one_parameters(message: Message):
    #main.loggerDEBUG.debug('вывод всего расписания (0)')
    if message.text == 'все':
        s = jsonFormatter.print_all_time_table()
        return s
    elif message.text == 'выйти':
        dataBase.set_way(message.chat.id, -1)
        dataBase.set_count_parameters(message.chat.id, 0)
    else:
        year = f'{(int(message.text[2:4]) % 100)}'
        strGroup = ''
        if message.text[4:] == ' (магистратура)':
            strGroup += 'КММО'
        elif message.text[4:] == ' (бакалавриат)':
            strGroup += 'КМБО'
        else:
            return 'ERROR'
        return jsonFormatter.print_all_time_table_with_course(strGroup, year)


def catching_stupid_in_third(text):
    if text == kb.STRBUTTONSTHIRD_1:
        return False
    elif text == kb.STRBUTTONSTHIRD_2:
        return False
    elif text == kb.STRBUTTONSTHIRD_3:
        return False
    elif text == kb.STRBUTTONSTHIRD_4:
        return False
    elif text == kb.STRBUTTONSTHIRD_5:
        return False
    elif text == kb.STRBUTTONSTHIRD_6:
        return False
    elif text == kb.STRBUTTONSTHIRD_7:
        return False
    elif text == kb.STRBUTTONSTHIRD_8:
        return False
    return True


def data_to_array(strData):
    array = ['', '', '']
    ln = len(strData)
    if ln == 5:
        array[0] = strData[0:2]
        array[1] = strData[3:]
        if strData[2] != ' ' and strData[2] != '/' and strData[2] != '.' and strData[2] != '-':
            array = ['', '', '']
    elif ln == 4:
        array[0] = strData[0:2]
        array[1] = strData[2:]
    array[2] = str(datetime.date.today().year)
    if array[0] == '' or array[1] == '' or array[2] == '':
        return 'Некорректный ввод даты.\n' \
               'Повторите снова.'
    else:
        return array


def sendNotif(s):
    timing = time.time()
    allChatId = main.dataBase.get_all_chats()
    i = 0
    while True:
        if time.time() - timing > 0.05:
            timing = time.time()
            chat_id = allChatId[i]
            try:
                # db.close()
                if s == '':
                    bot.send_message(chat_id,
                                     strings.MESSAGE_SEND_NOTIFICATION_first + strings.MESSAGE_SEND_NOTIFICATION_second)
                    main.STRING_RETURN += f'{chat_id} уведомление отправлено\n'
                else:
                    bot.send_message(chat_id,
                                     strings.MESSAGE_SEND_NOTIFICATION_first + s + "\n" + strings.MESSAGE_SEND_NOTIFICATION_second)
            except:
                # db.close()
                main.loggerDEBUG.warning(f'----- в chat_id: {chat_id} уведомление отправлено не было')
            i += 1


def row_to_list(row):
    llist = [row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
    return llist


def text_reg_exp(user_id):
    if dataBase.get_group(user_id) == '':
        return 'ERROR'
    return f'{strings.SEARCH_BY_GROUP_FOR_TODAY_1}"{dataBase.get_group(user_id)}"'
