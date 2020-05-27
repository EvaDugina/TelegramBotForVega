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
    row = dataBase.get_row_by_id(message.from_user.id)
    listRow = row_to_list(row)
    way = row[3]
    countParam = row[4]

    # Работа с выводом информации--------------
    if way == 0:
        if countParam == 0:
            stringOut = group_zero_parameters(message.chat.id, message.text)
            if stringOut == strings.MESSAGE_ERROR_GROUP or stringOut == strings.MESSAGE_ERROR_DATE:
                row = dataBase.get_row_by_id(message.from_user.id)
                listRow = row_to_list(row)
                bot.send_message(message.chat.id, stringOut)
                if listRow[5] != '':
                    bot.send_message(message.chat.id, f'\nТЕКУЩАЯ ГРУППА: {listRow[5]}')
            elif not stringOut == '' and stringOut is not None:
                row = dataBase.get_row_by_id(message.from_user.id)
                listRow = row_to_list(row)
                bot.send_message(message.chat.id, stringOut)
                if listRow[5] != '':
                    bot.send_message(message.chat.id,
                                     strings.MESSAGE_ONLY_DATE_GROUP + f'\nТЕКУЩАЯ ГРУППА: {listRow[5]}',
                                     reply_markup=kb.determine_start_keyboard(listRow[5]))

    elif way == 1:
        if countParam == 0:
            stringOut = teacher_zero_parameters(message.chat.id, message.text)
            if stringOut == strings.MESSAGE_ERROR_TEACHER or stringOut == strings.MESSAGE_ERROR_DATE:
                row = dataBase.get_row_by_id(message.from_user.id)
                listRow = row_to_list(row)
                bot.send_message(message.chat.id, stringOut)
                if listRow[6] != '':
                    bot.send_message(message.chat.id, f'\nТЕКУЩИЙ ПРЕПОДАВАТЕЛЬ: {listRow[6]}')
            elif not stringOut == '' and stringOut is not None:
                row = dataBase.get_row_by_id(message.from_user.id)
                listRow = row_to_list(row)
                bot.send_message(message.chat.id, stringOut)
                if listRow[6] != '':
                    bot.send_message(message.chat.id,
                                     strings.MESSAGE_ONLY_DATE_TEACHER + f'\nТЕКУЩИЙ ПРЕПОДАВАТЕЛЬ: {listRow[6]}')

    elif way == 2:
        if countParam == 0:
            listRow[4] += 1
            bot.send_message(message.chat.id, strings.ENTER_COURSE_YEAR,
                             reply_markup=kb.determine_start_keyboard(listRow[5]))
            dataBase.edit_row(listRow[0], listRow)
        elif countParam == 1:
            catch = catching_stupid_in_third(message.text)
            if not catch:
                strOut = all_time_table_one_parameters(message)
                if message.text == 'выйти':
                    bot.send_message(message.chat.id, 'Выберите:',
                                     reply_markup=kb.determine_start_keyboard(listRow[5]))
                else:
                    ln = len(strOut)
                    if ln == 6:
                        for i, sOut in enumerate(strOut):
                            bot.send_message(message.chat.id, sOut) if not sOut == '' else print()
                    else:
                        bot.send_message(message.chat.id, strOut)
            else:
                main.loggerDEBUG.debug('вывод всего расписания (null)')
                bot.send_message(message.chat.id, strings.MESSAGE_ERROR_ALL_TIME_TABLE)

    elif way == 3:
        main.loggerDEBUG.debug('когда свободна Б-209? (0)')
        bot.send_message(message.chat.id, jsonFormatter.when_b209_is_free())
        listRow[3] = -1
        dataBase.edit_row(listRow[0], listRow)


def group_zero_parameters(chat_id, text):
    main.loggerDEBUG.debug('поиск по группе (0)')
    row = dataBase.get_row_by_id(chat_id)
    listRow = row_to_list(row)
    arrayGroupDate = text.split(' ')
    if text == "Поиск по группе":
        pass
    elif len(arrayGroupDate) == 1 or len(arrayGroupDate) == 3:
        gr = jsonFormatter.search_group(text)
        strOut = group_one_parameter(chat_id, arrayGroupDate[0])
        if not gr == 'ERROR':
            listRow[5] = jsonFormatter.text_to_group(text).upper()
            dataBase.edit_row(listRow[0], listRow)
            return group_one_parameter(chat_id, '1')
        elif strOut != strings.MESSAGE_ERROR_GROUP and strOut != "Некорректный ввод.\nПовторите снова." \
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
    elif len(arrayGroupDate) == 3:
        strOut = group_zero_parameters(chat_id, arrayGroupDate[0])
        if strOut != strings.MESSAGE_ERROR_GROUP and strOut != '':
            strDate = '.'.join([arrayGroupDate[1], arrayGroupDate[2]])
            strOut = group_one_parameter(chat_id, strDate)
            if strOut == strings.MESSAGE_ERROR_DATE:
                bot.send_message(chat_id, strings.MESSAGE_ERROR_DATE)
                return ''
            else:
                return strOut
        else:
            bot.send_message(chat_id, 'Некорректный ввод.\nПовторите снова.')
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
            bot.send_message(chat_id, 'Некорректный ввод.\nПовторите снова.')
            return ''
    elif len(arrayGroupDate) == 5:
        strGroupCheck = arrayGroupDate[0] + arrayGroupDate[1] + arrayGroupDate[2]
        strDate = '.'.join([arrayGroupDate[3], arrayGroupDate[4]])
        grZerPar = group_zero_parameters(chat_id, strGroupCheck)
        if grZerPar != strings.MESSAGE_ERROR_GROUP and grZerPar != '' \
                and group_one_parameter(chat_id, strDate) != strings.MESSAGE_ERROR_DATE:
            return group_one_parameter(chat_id, strDate)
        else:
            bot.send_message(chat_id, 'Некорректный ввод.\nПовторите снова.')
            return ''
    else:
        return ''


def group_one_parameter(chat_id, text):
    main.loggerDEBUG.debug('поиск по группе (1)')
    row = dataBase.get_row_by_id(chat_id)
    listRow = row_to_list(row)
    if text == '1':
        date = datetime.datetime.today()
        group = jsonFormatter.search_by_group_and_date(listRow[5], jsonFormatter.week_to_string(date.weekday()))
        return group
    elif text == '7':
        group = jsonFormatter.search_by_group(listRow[5])
        return group
    try:
        arrayData = data_to_array(text)
        date = datetime.datetime(int(arrayData[2]), int(arrayData[1]), int(arrayData[0]))
        group = jsonFormatter.search_by_group_and_date(listRow[5], jsonFormatter.week_to_string(date.weekday()))
        dataBase.edit_row(listRow[0], listRow)
        return group
    except:
        dataBase.edit_row(listRow[0], listRow)
        if listRow[5] == '':
            return strings.MESSAGE_ERROR_GROUP
        return strings.MESSAGE_ERROR_DATE


def teacher_zero_parameters(chat_id, text):
    main.loggerDEBUG.debug('поиск по преподавателю (0)')
    row = dataBase.get_row_by_id(chat_id)
    listRow = row_to_list(row)
    arrayTeacherDate = text.split(' ')
    if text == "Поиск по преподавателю":
        pass
    elif len(arrayTeacherDate) == 1:
        tch = jsonFormatter.search_subject(text)
        date = teacher_one_parameter(chat_id, text)
        if not tch == 'ERROR':
            listRow[6] = text.upper()
            dataBase.edit_row(listRow[0], listRow)
            return teacher_one_parameter(chat_id, '1')
        elif date != strings.MESSAGE_ERROR_DATE:
            return date
        elif date == strings.MESSAGE_ERROR_DATE or text == strings.SEARCH_BY_TEACHER:
            return date
        else:
            return ''
    elif len(arrayTeacherDate) == 2:
        date = teacher_one_parameter(chat_id, text)
        tch = teacher_zero_parameters(chat_id, arrayTeacherDate[0])
        if tch != strings.MESSAGE_ERROR_TEACHER and tch != '' and tch != "Некорректный ввод даты.\nПовторите снова.":
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
        if tch != strings.MESSAGE_ERROR_TEACHER and tch != '' and tch != "Некорректный ввод даты.\nПовторите снова.":
            strDate = '.'.join([arrayTeacherDate[1], arrayTeacherDate[2]])
            strOut = teacher_one_parameter(chat_id, strDate)
            if strOut == strings.MESSAGE_ERROR_DATE:
                bot.send_message(chat_id, strings.MESSAGE_ERROR_DATE)
                return ''
            else:
                return strOut
        else:
            bot.send_message(chat_id, 'Некорректный ввод.\nПовторите снова.')
            return ''
    else:
        return ''


def teacher_one_parameter(chat_id, text):
    main.loggerDEBUG.debug('поиск по преподавателю (1)')
    row = dataBase.get_row_by_id(chat_id)
    listRow = row_to_list(row)
    if text == '1':
        date = datetime.datetime.today()
        teacher = jsonFormatter.search_by_teacher_and_date(listRow[6], jsonFormatter.week_to_string(date.weekday()))
        return teacher
    elif text == '7':
        teacher = jsonFormatter.search_by_teacher(listRow[6])
        return teacher
    else:
        try:
            arrayData = data_to_array(text)
            date = datetime.datetime(int(arrayData[2]), int(arrayData[1]), int(arrayData[0]))
            teacher = jsonFormatter.search_by_teacher_and_date(listRow[6], jsonFormatter.week_to_string(date.weekday()))
            return teacher
        except:
            if listRow[5] == '':
                return strings.MESSAGE_ERROR_TEACHER
            return strings.MESSAGE_ERROR_DATE


def all_time_table_one_parameters(message: Message):
    main.loggerDEBUG.debug('вывод всего расписания (0)')
    row = dataBase.get_row_by_id(message.from_user.id)
    listRow = row_to_list(row)
    if message.text == 'все':
        s = jsonFormatter.print_all_time_table()
        return s
    elif message.text == 'выйти':
        listRow[4] = 0
        listRow[3] = -1
        dataBase.edit_row(listRow[0], listRow)
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
    connection = dataBase.get_user_connection()
    db = connection.cursor()
    db.execute("SELECT * FROM all_users")
    timing = time.time()
    while True:
        if time.time() - timing > 0.05:
            timing = time.time()
            row = db.fetchone()
            if row == None:
                break

            chat_id = row[2]
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


def isAdmin(id):
    connection = dataBase.get_admin_connection()
    db = connection.cursor()
    db.execute("SELECT * FROM admins")
    while True:
        row = db.fetchone()
        if row == None:
            break

        user_id = row[1]
        if int(user_id) == int(id):
            # db.close()
            return True
    # db.close()
    return False


def row_to_list(row):
    llist = [row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
    return llist


def text_reg_exp(user_id):
    row = dataBase.get_row_by_id(user_id)
    listRow = row_to_list(row)
    if listRow[5] == '':
        return 'ERROR'
    return f'{strings.SEARCH_BY_GROUP_FOR_TODAY_1}"{listRow[5]}"{strings.SEARCH_BY_GROUP_FOR_TODAY_2}'
