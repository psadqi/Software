import sqlite3
import hashlib
import os
import binascii

# کلاس پایگاه داده برای مدیریت رمزهای عبور و تعامل با دیتابیس SQLite
class DataBase:
    def __init__(self, name):
        self.name = name  # نام فایل پایگاه داده

    def _hash_password(self, password):
        """
        هش کردن رمز عبور با استفاده از الگوریتم PBKDF2_HMAC به همراه salt
        خروجی: رشته‌ای متنی شامل salt و هش ترکیب شده
        """
        salt = os.urandom(16)  # تولید salt به اندازه 16 بایت (128 بیت)
        iterations = 100000  # تعداد تکرارها
        hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)
        return binascii.hexlify(salt + hash_bytes).decode('ascii')  # ترکیب salt و hash و تبدیل به رشته هگز

    def _verify_password(self, stored_hash, provided_password):
        """
        بررسی صحت رمز عبور وارد شده با استفاده از هش ذخیره‌شده
        """
        try:
            stored_bytes = binascii.unhexlify(stored_hash.encode('ascii'))  # تبدیل هش ذخیره شده به بایت
            salt = stored_bytes[:16]  # استخراج salt
            stored_hash_bytes = stored_bytes[16:]  # استخراج هش اصلی
            # تولید هش جدید با رمز عبور وارد شده
            new_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
            return new_hash == stored_hash_bytes  # مقایسه هش جدید با هش ذخیره‌شده
        except:
            return False  # در صورت خطا، False برمی‌گرداند

    def manager_pass(self, username):
        """
        دریافت رمز عبور هش‌شده‌ی مدیر با استفاده از نام کاربری
        """
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "SELECT password FROM manager_admin WHERE username = ?",
            (username,)
        )
        password = self.cursor.fetchone()  # دریافت نتیجه به صورت tuple یا None
        self.connect.close()
        return password  # خروجی: (password,) یا None

    def staff_pass(self, username):
        """
        دریافت رمز عبور هش‌شده‌ی کارمند با استفاده از نام کاربری
        """
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
        """
        دریافت پاسخ بازیابی رمز عبور برای مدیر (سؤال امنیتی)
        """
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "SELECT passRecovery FROM manager_admin WHERE username = ?",
            (username,)
        )
        passRecovery = self.cursor.fetchone()
        self.connect.close()
        return passRecovery  # خروجی: (پاسخ بازیابی,) یا None

    def update_pass(self, username, new_password):
        """
        به‌روزرسانی رمز عبور مدیر با رمز جدید هش‌شده
        """
        hashed_password = self._hash_password(new_password)  # هش کردن رمز جدید
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "UPDATE manager_admin SET password = ? WHERE username = ?",
            (hashed_password, username)
        )
        self.connect.commit()  # اعمال تغییرات در دیتابیس
        self.connect.close()
