import sqlite3
import hashlib
import os
import binascii


class DataBase:
    def __init__(self, name):
        self.name = name

    def _hash_password(self, password):
        """Hash a password with PBKDF2_HMAC and salt"""
        salt = os.urandom(16)  # 128-bit salt
        iterations = 100000
        hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)
        return binascii.hexlify(salt + hash_bytes).decode('ascii')

    def _verify_password(self, stored_hash, provided_password):
        """Verify a stored password against one provided by user"""
        try:
            stored_bytes = binascii.unhexlify(stored_hash.encode('ascii'))
            salt = stored_bytes[:16]
            stored_hash_bytes = stored_bytes[16:]
            new_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
            return new_hash == stored_hash_bytes
        except:
            return False

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
        hashed_password = self._hash_password(new_password)
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "UPDATE manager_admin SET password = ? WHERE username = ?",
            (hashed_password, username)
        )
        self.connect.commit()
        self.connect.close()