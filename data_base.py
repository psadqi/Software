import sqlite3

class DataBase:
    def __init__(self, name):
        self.name = name

    def manager_pass(self, username):
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute("SELECT password FROM manager_admin WHERE username = ?", (username,))
        password = self.cursor.fetchone()
        self.connect.close()
        return password

    def staff_pass(self, username):
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute("SELECT password FROM staff WHERE username = ?", (username,))
        password = self.cursor.fetchone()
        self.connect.close()
        return password

    def manager_recovery(self,username):
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute("SELECT passRecovery FROM manager_admin WHERE username = ?", (username,))
        passRecovery = self.cursor.fetchone()
        self.connect.close()
        return passRecovery

    def update_pass(self, username, password):
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute("UPDATE manager_admin SET password = (?) WHERE username = (?);", (password, username))
        self.connect.commit()
        self.connect.close()
