from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QMessageBox, QVBoxLayout, QHBoxLayout, QToolButton
)
from PyQt6.QtGui import QFont, QPixmap, QIcon, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QSize, QRegularExpression
from data_base import DataBase

import sys
import os

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller (.exe)
    """
    if hasattr(sys, '_MEIPASS'):
        # When bundled by PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class StaffLogin(QWidget):
    # سازنده کلاس که برای تنظیمات اولیه و راه‌اندازی رابط کاربری استفاده می‌شود
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # ذخیره پدر ویجت
        self.setup_ui()  # فراخوانی متد تنظیم رابط کاربری

    # متد تنظیم رابط کاربری
    def setup_ui(self):
        self.setStyleSheet("background-color: white;border-radius: 20px;")

        # چیدمان اصلی صفحه به صورت افقی
        outer_layout = QHBoxLayout(self)

        # پنل سمت چپ که اندازه ثابت دارد
        fixed_left_widget = QWidget()
        fixed_left_widget.setFixedSize(400, 600)
        fixed_left_layout = QVBoxLayout(fixed_left_widget)
        fixed_left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # عنوان صفحه (ورود کارکن)
        self.label = QLabel("ورود کارکن")
        self.label.setFont(QFont('nazanintar', 28))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(""" 
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                border-radius: 15px;
                padding: 8px 20px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(150, 150, 150, 220),
                    stop:0.5 rgba(120, 120, 120, 240),
                    stop:1 rgba(90, 90, 90, 220));
                border: 2px solid #e0e0e0;
                text-shadow: 2px 2px 3px black;
            }
        """)
        fixed_left_layout.addWidget(self.label)

        # تصویر مربوط به کارکنان
        self.staff_image = QLabel()
        staff_pixmap = QPixmap(resource_path("staff.png"))  # بارگذاری تصویر کارکن
        if not staff_pixmap.isNull():
            self.staff_image.setPixmap(staff_pixmap.scaled(
                300, 300,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        self.staff_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fixed_left_layout.addWidget(self.staff_image)

        # فرم ورود اطلاعات (نام کاربری و رمز عبور)
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)

        # فیلد ورودی نام کاربری
        self.username = QLineEdit()
        self.username.setFont(QFont('nazanintar', 16))
        self.username.setPlaceholderText("\u200Eنام کاربری")
        self.username.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        # حداکثر تعداد کاراکتر
        self.username.setMaxLength(20)

        # مقادیر قابل قبول (A-Z, a-z, 0-9, _, -, .)
        username_validator = QRegularExpressionValidator(
            QRegularExpression("^[a-zA-Z0-9_\\-\\.]+$"), self.username
        )
        self.username.setValidator(username_validator)
        self.username.textChanged.connect(self.update_username_style)

        self.username.setStyleSheet("""
                    QLineEdit {
                        background: white;
                        border: 2px solid #3498db;
                        border-radius: 5px;
                        padding: 5px;
                        min-width: 300px;
                    }
                """)
        form_layout.addWidget(self.username)

        # فیلد رمز عبور با آیکون چشم بزرگتر
        self.password = QLineEdit()
        self.password.setFont(QFont('nazanintar', 16))
        self.password.setPlaceholderText("\u200Eرمز عبور")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.password.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #3498db;
                border-radius: 5px;
                padding: 5px;
                min-width: 300px;
                padding-right: 40px;  /* فضای برای آیکون چشم */
            }
        """)
        self.password.setMaxLength(20)
        self.password.returnPressed.connect(self.check_login)

        # دکمه چشم برای نمایش/پنهان کردن رمز عبور
        self.eye_button = QToolButton(self.password)
        self.eye_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.eye_button.setStyleSheet("""
            QToolButton {
                border: none;
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
        """)

        # تنظیم اندازه آیکون (30x30)
        eye_icon = QIcon(resource_path("eye.png"))
        self.eye_button.setIconSize(QSize(30, 30))
        self.eye_button.setIcon(eye_icon)
        self.eye_button.clicked.connect(self.toggle_password_visibility)

        # موقعیت‌دهی دکمه چشم در داخل فیلد رمز عبور
        self.eye_button.move(self.password.width() - 35, 5)
        self.eye_button.resize(30, 30)

        # به‌روزرسانی موقعیت دکمه چشم در صورت تغییر اندازه فیلد رمز عبور
        self.password.resizeEvent = lambda event: self.eye_button.move(
            self.password.width() - 35, 5
        )

        form_layout.addWidget(self.password)

        # چیدمان دکمه‌ها
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        # دکمه بازگشت
        self.back_button = QPushButton("بازگشت")
        self.back_button.setFont(QFont('nazanintar', 20))
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                min-width: 120px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #e0392b;
            }
        """)
        self.back_button.clicked.connect(lambda: self.parent.init_main_menu())
        buttons_layout.addWidget(self.back_button)

        # دکمه ورود
        self.login_button = QPushButton("ورود")
        self.login_button.setFont(QFont('nazanintar', 20))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                min-width: 120px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.login_button.clicked.connect(self.check_login)
        self.login_button.setDefault(True)
        buttons_layout.addWidget(self.login_button)

        form_layout.addLayout(buttons_layout)

        # دکمه بازیابی رمز عبور
        self.help_button = QPushButton("بازیابی رمز عبور")
        self.help_button.setFont(QFont('nazanintar', 20))
        self.help_button.setStyleSheet("""
            QPushButton {
                background-color: #4a709b;
                color: white;
                border-radius: 5px;
                min-width: 180px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #6f86a1;
            }
        """)
        self.help_button.clicked.connect(self.show_help)
        form_layout.addWidget(self.help_button, alignment=Qt.AlignmentFlag.AlignCenter)

        fixed_left_layout.addLayout(form_layout)

        # اضافه کردن پنل به چیدمان
        left_side = QVBoxLayout()
        left_side.addStretch(1)
        left_side.addWidget(fixed_left_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        left_side.addStretch(1)

        outer_layout.addLayout(left_side, 1)
        outer_layout.addStretch(1)

    #استایل فیلد یوزرنیم
    def update_username_style(self):
        """استایل فیلد با توجه به صحت ان"""
        if self.username.hasAcceptableInput():
            self.username.setStyleSheet("""
                QLineEdit {
                    background: white;
                    border: 2px solid #3498db;
                    border-radius: 5px;
                    padding: 5px;
                    min-width: 300px;
                }
            """)
        else:
            self.username.setStyleSheet("""
                QLineEdit {
                    background: #FFEBEE;
                    border: 2px solid #e74c3c;
                    border-radius: 5px;
                    padding: 5px;
                    min-width: 300px;
                }
            """)

    # متد تغییر حالت نمایش رمز عبور
    def toggle_password_visibility(self):
        if self.password.echoMode() == QLineEdit.EchoMode.Password:
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.eye_button.setIcon(QIcon(resource_path("eye-off.png")))
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
            self.eye_button.setIcon(QIcon(resource_path("eye.png")))
        # حفظ اندازه آیکون
        self.eye_button.setIconSize(QSize(30, 30))

    # متد بررسی اطلاعات ورود
    def check_login(self):
        db = DataBase("project_db.db")  # اتصال به پایگاه داده
        username = self.username.text()
        password = self.password.text()

        try:
            correct_password = db.staff_pass(username)
            if correct_password and correct_password[0] == password:
                QMessageBox.information(self, "ورود", "ورود موفقیت آمیز بود", QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.warning(self, "خطا", "نام کاربری یا رمز عبور اشتباه است!", QMessageBox.StandardButton.Ok)
                self.password.setText("")  # پاک کردن رمز عبور در صورت اشتباه بودن
        except Exception as e:
            QMessageBox.critical(self, "خطا", "مشکلی در سیستم به وجود آمده است!", QMessageBox.StandardButton.Ok)
            self.password.setText("")  # پاک کردن رمز عبور در صورت بروز خطا

    # متد نمایش راهنما
    def show_help(self):
        QMessageBox.information(self, "راهنما", "در صورت نیاز به راهنمایی، با مدیر تماس بگیرید.",
                                QMessageBox.StandardButton.Ok)
