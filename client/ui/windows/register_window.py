from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QMessageBox,
)

from client.api.register_api import RegisterAPI
from client.api.package_api import PackageAPI


class RegisterWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create Account")
        self.resize(500, 700)

        page = QWidget()
        layout = QVBoxLayout(page)

        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)

        title = QLabel("Create Your Lumora Account")
        title.setAlignment(Qt.AlignCenter)

        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText("Full Name")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Phone Number")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm Password")
        self.confirm_password.setEchoMode(QLineEdit.Password)

        self.package = QComboBox()

        self.plan = QComboBox()

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        self.load_packages()

        layout.addWidget(title)
        layout.addWidget(self.full_name)
        layout.addWidget(self.email)
        layout.addWidget(self.phone)
        layout.addWidget(self.password) 
        layout.addWidget(self.confirm_password)
        layout.addWidget(self.package)
        layout.addWidget(self.plan)
        layout.addWidget(self.register_button)

        self.setCentralWidget(page)

    def register(self):

        result = RegisterAPI.register(
            full_name=self.full_name.text().strip(),
            email=self.email.text().strip(),
            phone=self.phone.text().strip(),
            password=self.password.text(),
            confirm_password=self.confirm_password.text(),
            package_id=self.package.currentData(),
            plan_id=self.plan.currentData(),
        )

        if result is None:
            QMessageBox.warning(
                self,
                "Registration Failed",
                "Registration failed.",
            )
            return

        QMessageBox.information(
            self,
            "Success",
            "Registration successful.\nWaiting for payment approval.",
        )

        self.close()

    def load_packages(self):

        self.package.clear()

        packages = PackageAPI.get_packages()

        if packages is None:
            return

        for package in packages:
            self.package.addItem(
                package["name"],
                package["id"],
            )

        self.package.currentIndexChanged.connect(self.load_plans)

        self.load_plans()


    def load_plans(self):

        self.plan.clear()

        package_id = self.package.currentData()

        if package_id is None:
            return

        plans = PackageAPI.get_plans(package_id)

        if plans is None:
            return

        for plan in plans:
            self.plan.addItem(
                plan["name"],
                plan["id"],
            )