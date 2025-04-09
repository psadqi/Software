import sqlite3
from passlib.hash import argon2

class DataBase:
    def __init__(self, name):
        self.name = name

    def manager_pass(self, username):
        """Get hashed password for manager"""
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "SELECT password FROM manager_admin WHERE username = ?",
            (username,)
        )
        password = self.cursor.fetchone()
        self.connect.close()
        return password

    def staff_pass(self, username):
        """Get hashed password for staff"""
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "SELECT password FROM staff WHERE username = ?",
            (username,)
        )
        password = self.cursor.fetchone()
        self.connect.close()
        return password

    def manager_recovery(self, username):
        """Get security answer for password recovery"""
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "SELECT passRecovery FROM manager_admin WHERE username = ?",
            (username,)
        )
        passRecovery = self.cursor.fetchone()
        self.connect.close()
        return passRecovery

    def update_pass(self, username, new_password):
        """Update password with hashing"""
        hashed_password = argon2.hash(new_password)
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "UPDATE manager_admin SET password = ? WHERE username = ?",
            (hashed_password, username)
        )
        self.connect.commit()
        self.connect.close()