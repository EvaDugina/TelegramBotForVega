from enum import Enum


class States(Enum):
    MAIN = -1
    GROUP_SEARCH = 0
    TEACHER_SEARCH = 1
    FULL_TIMETABLE = 2
    BEST_ROOM = 3
    CURRENT_GROUP_SEARCH = 10