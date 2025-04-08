from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QMessageBox, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from data_base import DataBase


class StaffLogin(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()


    def setup_ui(self):
        # Outer layout
        outer_layout = QHBoxLayout(self)

        # === Left fixed container ===
        fixed_left_widget = QWidget()
        fixed_left_widget.setFixedSize(400, 600)
        fixed_left_layout = QVBoxLayout(fixed_left_widget)
        fixed_left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title label
        self.label = QLabel("ورود کارکن")
        self.label.setFont(QFont('nazanintar', 28))
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
        fixed_left_layout.addWidget(self.label)

        # Staff image
        self.staff_image = QLabel()
        staff_pixmap = QPixmap("staff.png")
        if not staff_pixmap.isNull():
            self.staff_image.setPixmap(staff_pixmap.scaled(
                300, 300,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        self.staff_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fixed_left_layout.addWidget(self.staff_image)

        # Form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)

        self.username = QLineEdit()
        self.username.setFont(QFont('nazanintar', 16))
        self.username.setPlaceholderText("نام کاربری")
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

        self.password = QLineEdit()
        self.password.setFont(QFont('nazanintar', 16))
        self.password.setPlaceholderText("رمز عبور")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet(self.username.styleSheet())
        form_layout.addWidget(self.password)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

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
        buttons_layout.addWidget(self.login_button)

        form_layout.addLayout(buttons_layout)

        # New Help button below the row
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

        # --- Wrap fixed_left_widget with spacing to center in left half ---
        left_side = QVBoxLayout()
        left_side.addStretch(1)
        left_side.addWidget(fixed_left_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        left_side.addStretch(1)

        outer_layout.addLayout(left_side, 1)  # Left half
        outer_layout.addStretch(1)  # Right half (empty stretch)

    def check_login(self):
        db = DataBase("project_db.db")

        username = self.username.text()
        password = self.password.text()

        try:
            correct_password = db.staff_pass(username)
            if correct_password and correct_password[0] == password:
                QMessageBox.information(self, "ورود", "خوش آمدید", QMessageBox.StandardButton.Ok)
                # Proceed to staff dashboard or next screen
            else:
                QMessageBox.warning(self, "خطا", "نام کاربری یا رمز عبور اشتباه است!", QMessageBox.StandardButton.Ok)
                self.username.setText("")
                self.password.setText("")
        except Exception as e:
            QMessageBox.critical(self, "خطا", "مشکلی در سیستم به وجود آمده است!", QMessageBox.StandardButton.Ok)
            self.username.setText("")
            self.password.setText("")

    def show_help(self):
        QMessageBox.information(self, "راهنما", "در صورت نیاز به راهنمایی، با مدیر تماس بگیرید.", QMessageBox.StandardButton.Ok)
