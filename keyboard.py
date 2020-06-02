import strings

import telebot
import datetime


def determine_the_year():
    month = datetime.datetime.today().month
    if month == 9 or month == 10 or month == 11 or month == 12:
        number = datetime.datetime.today().year % 100
    else:
        number = datetime.datetime.today().year % 100 - 1
    return number


def determine_start_keyboard(strGroup):
    choiceMarkup = telebot.types.ReplyKeyboardMarkup(1)
    if strGroup != '':
        choiceMarkup.row(f'{strings.SEARCH_BY_GROUP_FOR_TODAY_1}"{strGroup}"')
    choiceMarkup.row(strings.SEARCH_BY_GROUP)
    choiceMarkup.row(strings.SEARCH_BY_TEACHER)
    choiceMarkup.row(strings.SEARCH_ALL_TIME_TABLE)
    choiceMarkup.row(strings.SEARCH_BY_B209)
    return choiceMarkup


choiceDateForB209 = telebot.types.ReplyKeyboardMarkup(1)
choiceDateForB209.row("Сегодня")
choiceDateForB209.row("На неделе")


choiceDateForCurrentGroup = telebot.types.ReplyKeyboardMarkup(1)
choiceDateForCurrentGroup.row("На сегодня")
choiceDateForCurrentGroup.row("На неделю")


choiceCourse = telebot.types.ReplyKeyboardMarkup(1)
number = determine_the_year()

STRBUTTONSTHIRD_1 = f'20{number} (бакалавриат)'
STRBUTTONSTHIRD_2 = f'20{(number - 1)} (бакалавриат)'
STRBUTTONSTHIRD_3 = f'20{(number - 2)} (бакалавриат)'
STRBUTTONSTHIRD_4 = f'20{(number - 3)} (бакалавриат)'
STRBUTTONSTHIRD_5 = f'20{number} (магистратура)'
STRBUTTONSTHIRD_6 = f'20{(number - 1)} (магистратура)'
STRBUTTONSTHIRD_7 = "все"
STRBUTTONSTHIRD_8 = "выйти"

choiceCourse.row(STRBUTTONSTHIRD_1, STRBUTTONSTHIRD_2)
choiceCourse.row(STRBUTTONSTHIRD_3, STRBUTTONSTHIRD_4)
choiceCourse.row(STRBUTTONSTHIRD_5, STRBUTTONSTHIRD_6)
choiceCourse.row(STRBUTTONSTHIRD_7)
choiceCourse.row(STRBUTTONSTHIRD_8)
