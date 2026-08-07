from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMainWindow,
    QMessageBox,
)

from client.api.auth_api import AuthAPI
from client.ui.windows.register_window import RegisterWindow
from client.ui.windows.dashboard_window import DashboardWindow
from client.services.client_service import ClientService


class LoginWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.token = None

        self.setWindowTitle("Lumora Copy Trading")
        self.resize(420, 520)

        self.init_ui()

    def init_ui(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("Lumora Copy Trading")
        title.setAlignment(Qt.AlignCenter)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Create Account")

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.open_register)

        layout.addWidget(title)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setCentralWidget(page)

    def login(self):

        result = AuthAPI.login_request(
            self.email.text().strip(),
            self.password.text(),
        )

        if not result["success"]:
            QMessageBox.warning(
                self,
                "Login Failed",
                result["message"],
            )
            return

        data = result["data"]

        self.token = data["access_token"]

        print("TOKEN =", self.token)

        QMessageBox.information(
            self,
            "Success",
            "Login Successful.",
        )

        ClientService.start(self.token)

        self.dashboard = DashboardWindow(self.token)
        self.dashboard.show()

        self.hide()
        
    def open_register(self):

        self.register_window = RegisterWindow()
        self.register_window.show()