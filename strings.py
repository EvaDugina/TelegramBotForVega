SEARCH_BY_GROUP_FOR_TODAY_1 = 'Расписание группы: '
SEARCH_BY_GROUP = 'Поиск по группе'
SEARCH_BY_TEACHER = 'Поиск по преподавателю'
SEARCH_ALL_TIME_TABLE = 'Вывод полного расписания'
SEARCH_BY_B209 = 'Когда свободна Б-209?'

ENTER_DATE_FOR_CURRENT_GROUP = '\n'.join(["Выберите дату из списка",
                                          "или введите её в формате примера.",
                                          "ПРИМЕРЫ:",
                                          "21.08", "21/08", "21 08", "2108"])
ENTER_GROUP = '\n'.join(["Введите номер группы и дату или только дату, если хотите искать расписание текущей группы.",
                         "ПРИМЕР:",
                         "'кмбо0219' - вывод расписания КМБО-02-19 на текущую дату",
                         "'кмбо 02 19 21.08' - вывод расписания КМБО-02-19 на 21.08 (текущего года)",
                         "'кмбо0219 21 08' - вывод расписания КМБО-02-19 на 21.08 (текущего года)",
                         "'кмбо 02 19 21 08' - вывод расписания КМБО-02-19 на 21.08 (текущего года)"])
ENTER_TEACHER = '\n'.join(["Введите фамилию преподавателя и дату.",
                         "ПРИМЕР:",
                         "'громова' - вывод расписания преподавателя: Громова на текущую дату",
                         "'громова 21.08' - вывод расписания преподавателя: Громова на 21.08 (текущего года)",
                         "'громова 21 08' - вывод расписания преподавателя: Громова на 21.08 (текущего года)"])
ENTER_DATE = '\n'.join(["Введите дату в формате примера или воспользуйтесь ключами:",
             "'1' (значение текущей даты)",
             "'7' (вывод расписания на целую неделю)",
             "ПРИМЕРЫ:",
             "1", "21.08.2001", "21/08/2001", "21 08 2001", "21082001"])
ENTER_COURSE_YEAR = "Выберите год курса: "

MESSAGE_ONLY_DATE_GROUP = "Теперь вы можете писать только дату."
MESSAGE_ONLY_DATE_TEACHER = "Теперь вы можете писать только дату."
MESSAGE_START = '\n'.join([f'Здравствуйте!', "Выберите один из пунктов меню:"])
MESSAGE_ERROR_GROUP = "Такой группы не существует."
MESSAGE_ERROR_TEACHER = "Такой преподаватель у нас не работает("
MESSAGE_ERROR_ALL_TIME_TABLE = "Выберите снова."
MESSAGE_ERROR_DATE = "Некорректный ввод даты.\nПовторите снова."
MESSAGE_ERROR_TEXT = "Некорректный ввод."
MESSAGE_SEND_NOTIFICATION_first = "Расписание на БК-536 изменилось!\n"
MESSAGE_SEND_NOTIFICATION_second = '\n'.join(['Проверьте его здесь или на официальном сайте:',
                                  'http://www.vega.fcyb.mirea.ru/'])
MESSAGE_ONE_OF_LIST_COMMANDS = "Выберите один из пунктов меню:"

INSTROUCTIONS_HELP = '\n'.join(["Дорогие друзья, надо помнить, "
                                "как завещал Владимир Владимирович, "
                                "о правилах, которые присутствуют в каждом боте "
                                "и не нарушать их."])


NO_PARS = "Занятия отсутствуют."
