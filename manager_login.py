from PyQt6.QtGui import QFont, QPainter, QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt


class ManagerLogin(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(1100, 700)

        # Title Label (moved slightly higher)
        self.label = QLabel("ورود مالک", self)
        self.label.setFont(QFont('nazanintar', 28))
        self.label.setGeometry(150, 50, 300, 50)  # Centered horizontally
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # For maximum visibility
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
        # Add manager image (between label and username fields)
        self.manager_image = QLabel(self)
        manager_pixmap = QPixmap("manager.png")  # Your image path

        # Scale image proportionally to reasonable size
        self.manager_image.setPixmap(manager_pixmap.scaled(
            300, 300,  # Width and height
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        self.manager_image.setGeometry(
            150,  # x-position (centered)
            120,  # y-position (below title)
            300,  # width
            350  # height
        )
        self.manager_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Username Field (moved down to accommodate image)
        self.username = QLineEdit(self)
        self.username.setFont(QFont('nazanintar', 16))
        self.username.setPlaceholderText("نام کاربری")
        self.username.setGeometry(150, 450, 300, 40)  # Centered
        self.username.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #3498db;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # Password Field (moved down and centered)
        self.password = QLineEdit(self)
        self.password.setFont(QFont('nazanintar', 16))
        self.password.setPlaceholderText("رمزعبور")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setGeometry(150, 500, 300, 40)  # Centered
        self.password.setStyleSheet(self.username.styleSheet())

        # Login Button (centered)
        self.login_button = QPushButton("ورود", self)
        self.login_button.setGeometry(150, 550, 300, 40)  # Centered
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

        # Back Button (centered)
        self.back_button = QPushButton("بازگشت", self)
        self.back_button.setGeometry(150, 600, 300, 40)  # Centered
        self.back_button.setFont(QFont('nazanintar', 20))
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.back_button.clicked.connect(parent.init_main_menu)