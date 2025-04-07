from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
import sqlite3


class DB:
    def __init__(self, name):
        self._name = name

    def select(self, username):
        self.connect = sqlite3.connect(self._name)
        self.cursor = self.connect.cursor()
        self.cursor.execute("SELECT password FROM staff WHERE username = ?", (username,))
        password = self.cursor.fetchone()
        self.connect.close()
        return password


class StaffLogin(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setFixedSize(1100, 700)

        # Title Label
        self.label = QLabel("ورود کارکن", self)
        self.label.setFont(QFont('nazanintar', 28))
        self.label.setGeometry(150, 50, 300, 50)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px 20px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(150, 150, 150, 220),
                    stop:0.5 rgba(120, 120, 120, 240),
                    stop:1 rgba(90, 90, 90, 220));
                border: 2px solid #e0e0e0;
                text-shadow: 2px 2px 3px black;
            }
        """)

        # Staff Image
        self.staff_image = QLabel(self)
        staff_pixmap = QPixmap("staff.png")
        self.staff_image.setPixmap(staff_pixmap.scaled(
            300, 300,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        self.staff_image.setGeometry(150, 120, 300, 350)
        self.staff_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Username Field
        self.username = QLineEdit(self)
        self.username.setFont(QFont('nazanintar', 16))
        self.username.setPlaceholderText("نام کاربری")
        self.username.setGeometry(150, 450, 300, 40)
        self.username.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #3498db;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # Password Field
        self.password = QLineEdit(self)
        self.password.setFont(QFont('nazanintar', 16))
        self.password.setPlaceholderText("رمز عبور")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setGeometry(150, 500, 300, 40)
        self.password.setStyleSheet(self.username.styleSheet())

        # Login Button
        self.login_button = QPushButton("ورود", self)
        self.login_button.setGeometry(150, 550, 300, 40)
        self.login_button.setFont(QFont('nazanintar', 20))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                font-size: 22px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.login_button.clicked.connect(self.check_login)

        # Back Button
        self.back_button = QPushButton("بازگشت", self)
        self.back_button.setGeometry(150, 600, 300, 40)
        self.back_button.setFont(QFont('nazanintar', 20))
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                font-size: 22px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.back_button.clicked.connect(parent.init_main_menu)

    def check_login(self):
        db = DB("project_db.db")
        username = self.username.text()
        password = self.password.text()

        try:
            correct_password = db.select(username)
            if correct_password and correct_password[0] == password:
                pass
                # Proceed to staff dashboard or next screen
            else:
                QMessageBox.critical(
                    self,
                    "خطا",
                    "نام کاربری یا رمز عبور اشتباه است!",
                    QMessageBox.StandardButton.Ok
                )
                self.username.setText("")
                self.password.setText("")
        except Exception as e:
            print(f"Error: {e}")
            QMessageBox.critical(
                self,
                "خطا",
                "نام کاربری یا رمز عبور اشتباه است!",
                QMessageBox.StandardButton.Ok
            )
            self.username.setText("")
            self.password.setText("")