import sqlite3
import functions as fnc
from BotStates import States

''' Тут нужно обернуть все в класс BDWorker '''


class AbstractDBWork:

    def add_user(self, user_id: int, chat_id: int):
        pass

    def set_default_values(self, chat_id):
        pass

    def set_default_way(self, chat_id):
        pass

    def set_user_id(self, chat_id, user_id):
        pass

    def set_way(self, chat_id, way):
        pass

    def set_count_parameters(self, chat_id, count_parameters):
        pass

    def set_name_group(self, chat_id, name_group):
        pass

    def set_name_teacher(self, chat_id, name_teacher):
        pass

    def get_all_chats(self):
        pass

    def get_user_id(self, user_id):
        pass

    def get_chat_id(self, user_id):
        pass

    def get_way(self, user_id):
        pass

    def get_count_parameters(self, user_id):
        pass

    def get_group(self, user_id):
        pass

    def get_teacher(self, user_id):
        pass

    def is_admin(self, id):
        pass


class DBWorker(AbstractDBWork):
    CONNECTION_USERS_DB = None
    CONNECTION_ADMINS_DB = None

    def __init__(self, usersDataBaseName, adminsDataBaseName, force: bool = False):
        if self.CONNECTION_USERS_DB is None:
            self.CONNECTION_USERS_DB = sqlite3.connect(usersDataBaseName, check_same_thread=False)
        if self.CONNECTION_ADMINS_DB is None:
            self.CONNECTION_ADMINS_DB = sqlite3.connect(adminsDataBaseName, check_same_thread=False)

        users_connection = self.CONNECTION_USERS_DB
        c = users_connection.cursor()
        if force:
            c.execute('DROP TABLE IF EXISTS all_users')
        c.execute("""CREATE TABLE IF NOT EXISTS all_users
                        (id         INTEGER PRIMARY KEY, 
                            user_id     INTEGER NOT NULL UNIQUE,
                            chat_id     INTEGER NOT NULL UNIQUE,
                            way         INTEGER DEFAULT -1,
                            count_par   INTEGER DEFAULT 0,
                            name_group  TEXT NOT NULL DEFAULT '',
                            name_teacher  TEXT NOT NULL DEFAULT '')
                        """)
        users_connection.commit()
        # c.close()

        admins_connection = self.CONNECTION_ADMINS_DB
        c = admins_connection.cursor()
        if force:
            c.execute('DROP TABLE IF EXISTS admins')
        c.execute("""CREATE TABLE IF NOT EXISTS admins
                            (id         INTEGER PRIMARY KEY, 
                            user_id     INTEGER NOT NULL UNIQUE,
                            chat_id     INTEGER NOT NULL UNIQUE)
                            """)
        admins_connection.commit()
        # c.close()

    def __edit_row(self, index, row):
        row[3] = fnc.way_state_to_int(row[3])
        connection = self.CONNECTION_USERS_DB
        db = connection.cursor()
        db.execute("""UPDATE all_users 
                      SET way = ?, count_par = ?, name_group = ?, name_teacher = ?
                      WHERE chat_id=?""", (row[3], row[4], row[5], row[6], index))
        connection.commit()
        # db.close()

    def __get_row_by_id(self, user_id):
        connection = self.CONNECTION_USERS_DB
        db = connection.cursor()
        db.execute("SELECT * FROM all_users")
        while True:
            row = db.fetchone()
            if row == None:
                break
            u_id = row[1]
            if user_id == u_id:
                # db.close()
                connection.commit()
                return row
        connection.commit()
        # db.close()
        return None

    def add_admin(self, user_id):
        connection = self.CONNECTION_ADMINS_DB
        db = connection.cursor()
        try:
            db.execute('INSERT INTO admins (user_id, chat_id) VALUES (?, ?)', (user_id, user_id,))
            connection.commit()
            # c.close()
        except:
            connection.commit()

    def add_user(self, user_id: int, chat_id: int):
        connection = self.CONNECTION_USERS_DB
        c = connection.cursor()
        try:
            c.execute('INSERT INTO all_users (user_id, chat_id) VALUES (?, ?)', (user_id, chat_id,))
            connection.commit()
            # c.close()
        except:
            connection.commit()
            # c.close()

    def set_default_values(self, chat_id):
        row = self.__get_row_by_id(chat_id)
        listRow = fnc.row_to_list(row)
        listRow[3] = States[0]
        listRow[4] = 0
        listRow[5] = ''
        listRow[6] = ''
        self.__edit_row(chat_id, listRow)

    def set_default_way(self, chat_id):
        self.set_way(chat_id, States[0])

    def set_user_id(self, chat_id, user_id):
        connection = self.CONNECTION_USERS_DB
        db = connection.cursor()
        db.execute("""UPDATE all_users 
                              SET user_id = ?
                              WHERE chat_id=?""", (user_id, chat_id))
        connection.commit()

    def set_way(self, chat_id, way):
        way = fnc.way_state_to_int(way)
        if way != -2:
            connection = self.CONNECTION_USERS_DB
            db = connection.cursor()
            db.execute("""UPDATE all_users 
                                          SET way = ?
                                          WHERE chat_id=?""", (way, chat_id))
            connection.commit()

    def set_count_parameters(self, chat_id, count_parameters):
        connection = self.CONNECTION_USERS_DB
        db = connection.cursor()
        db.execute("""UPDATE all_users 
                                      SET count_par = ?
                                      WHERE chat_id=?""", (count_parameters, chat_id))
        connection.commit()

    def set_name_group(self, chat_id, name_group):
        connection = self.CONNECTION_USERS_DB
        db = connection.cursor()
        db.execute("""UPDATE all_users 
                                              SET name_group = ?
                                              WHERE chat_id=?""", (name_group, chat_id))
        connection.commit()

    def set_name_teacher(self, chat_id, name_teacher):
        connection = self.CONNECTION_USERS_DB
        db = connection.cursor()
        db.execute("""UPDATE all_users 
                                                      SET name_teacher = ?
                                                      WHERE chat_id=?""", (name_teacher, chat_id))
        connection.commit()

    def get_all_chats(self):
        connection = self.CONNECTION_USERS_DB
        db = connection.cursor()
        db.execute("SELECT * FROM all_users")
        allRows = []
        while True:
            newRow = db.fetchone()
            if newRow is None:
                break
            allRows.append(newRow[2])
        return allRows

    def get_user_id(self, user_id):
        return self.__get_row_by_id(user_id)[1]

    def get_chat_id(self, user_id):
        return self.__get_row_by_id(user_id)[2]

    def get_way(self, user_id):
        return States(self.__get_row_by_id(user_id)[3])

    def get_count_parameters(self, user_id):
        return self.__get_row_by_id(user_id)[4]

    def get_group(self, user_id):
        return self.__get_row_by_id(user_id)[5]

    def get_teacher(self, user_id):
        return self.__get_row_by_id(user_id)[6]

    def is_admin(self, id):
        connection = self.CONNECTION_ADMINS_DB
        db = connection.cursor()
        db.execute("SELECT * FROM admins")
        while True:
            row = db.fetchone()
            if row is None:
                break

            user_id = row[1]
            if int(user_id) == int(id):
                # db.close()
                return True
        # db.close()
        return False
