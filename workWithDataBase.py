import sqlite3

''' Тут нужно обернуть все в класс BDWorker '''


class AbstractDBWork:

    def add_user(self, user_id: int, chat_id: int):
        pass

    def edit_row(self, index, row):
        pass

    def get_all_rows(self):
        pass

    def get_row_by_id(self, user_id):
        pass

    def get_user_id(self, user_id):
        pass

    def get_chat_id(self):
        pass

    def get_way(self):
        pass

    def get_count_parameters(self):
        pass

    def get_group(self):
        pass

    def get_teacher(self):
        pass

    def is_admin(self, id):
        pass


class FileDBWork(AbstractDBWork):
    CONNECTION_USERS_DB = None
    CONNECTION_ADMINS_DB = None

    def __init__(self, usersDataBaseName, adminsDataBaseName, force: bool=False):
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
        #c.close()

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
        #c.close()

    def add_user(self, user_id: int, chat_id: int):
        connection = self.CONNECTION_USERS_DB
        c = connection.cursor()
        try:
            c.execute('INSERT INTO all_users (user_id, chat_id) VALUES (?, ?)', (user_id, chat_id,))
            connection.commit()
            #c.close()
        except:
            connection.commit()
            #c.close()

    def edit_row(self, index, row):
        connection = self.CONNECTION_USERS_DB
        db = connection.cursor()
        db.execute("""UPDATE all_users 
                      SET way = ?, count_par = ?, name_group = ?, name_teacher = ?
                      WHERE id=?""", (row[3], row[4], row[5], row[6], index))
        connection.commit()
        #db.close()

    def get_all_rows(self):
        connection = self.CONNECTION_USERS_DB
        db = connection.cursor()
        db.execute("SELECT * FROM all_users")
        allRows = []
        while True:
            newRow = db.fetchone()
            if newRow == None:
                break
            allRows.append(newRow)
        return allRows

    def get_row_by_id(self, user_id):
        connection = self.CONNECTION_USERS_DB
        db = connection.cursor()
        db.execute("SELECT * FROM all_users")
        while True:
            row = db.fetchone()
            if row == None:
                break
            u_id = row[1]
            if user_id == u_id:
                #db.close()
                connection.commit()
                return row
        connection.commit()
        #db.close()
        return 'ERROR'

    def get_user_id(self, user_id):
        return self.get_row_by_id(self, user_id)[1]

    def get_chat_id(self, user_id):
        return self.get_row_by_id(self, user_id)[2]

    def get_way(self, user_id):
        return self.get_row_by_id(self, user_id)[3]

    def get_count_parameters(self, user_id):
        return self.get_row_by_id(self, user_id)[4]

    def get_group(self, user_id):
        return self.get_row_by_id(self, user_id)[5]

    def get_teacher(self, user_id):
        return self.get_row_by_id(self, user_id)[6]


    def is_admin(self, id):
        connection = self.CONNECTION_ADMINS_DB
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


class DBWorker:
    def __init__(self, provider):
        self.db_provider = provider

    def add_user(self, user_id: int, chat_id: int):
        return self.db_provider.add_user(user_id, chat_id)

    def get_row_by_id(self, user_id):
        return self.db_provider.get_row_by_id(user_id)

    def edit_row(self, index, row):
        return self.db_provider.edit_row(index, row)

    def get_all_rows(self):
        return self.db_provider.get_all_rows()

    def is_admin(self, id):
        return self.db_provider.is_admin(id)