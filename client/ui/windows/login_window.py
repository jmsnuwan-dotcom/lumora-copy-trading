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
from client.api.subscription_api import SubscriptionAPI

from client.ui.windows.register_window import RegisterWindow
from client.ui.windows.dashboard_window import DashboardWindow
from client.ui.windows.admin_dashboard_window import (
    AdminDashboardWindow,
)
from client.ui.windows.package_selection_window import (
    PackageSelectionWindow,
)
from client.ui.windows.payment_window import PaymentWindow


class LoginWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.token = None

        self.admin_dashboard_window = None
        self.dashboard = None
        self.package_selection_window = None
        self.payment_window = None
        self.register_window = None

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
        self.register_button.clicked.connect(
            self.open_register
        )

        layout.addWidget(title)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setCentralWidget(page)

    def login(self):

        email = self.email.text().strip()
        password = self.password.text()

        if not email or not password:
            QMessageBox.warning(
                self,
                "Login Required",
                "Please enter your email and password.",
            )
            return

        result = AuthAPI.login_request(
            email,
            password,
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

        user = data["user"]

        # ==========================================
        # ADMIN
        # ==========================================

        if user["role"] == "admin":

            self.admin_dashboard_window = (
                AdminDashboardWindow(
                    self.token
                )
            )

            self.admin_dashboard_window.show()
            self.hide()

            return

        # ==========================================
        # CLIENT
        # ==========================================

        subscription = (
            SubscriptionAPI.get_my_subscription(
                self.token
            )
        )

        # ------------------------------------------
        # NO SUBSCRIPTION
        # ------------------------------------------

        if subscription is None:

            self.open_package_selection()

            return

        status = str(
            subscription.get(
                "status",
                "",
            )
        ).upper()

        payment_status = str(
            subscription.get(
                "payment_status",
                "",
            )
        ).upper()

        # ==========================================
        # PAYMENT WAITING
        # ==========================================

        if (
            status in {
                "PENDING",
                "SUBMITTED",
            }
            or payment_status in {
                "PENDING",
                "SUBMITTED",
            }
        ):

            self.open_pending_payment(
                subscription
            )

            return

        # ==========================================
        # APPROVED / ACTIVE
        # ==========================================

        if status in {
            "APPROVED",
            "ACTIVE",
        }:

            self.open_dashboard()

            return

        # ==========================================
        # UNKNOWN / EXPIRED / OTHER
        # ==========================================

        self.open_package_selection()

    def open_package_selection(self):

        self.package_selection_window = (
            PackageSelectionWindow(
                token=self.token,
            )
        )

        self.package_selection_window.show()
        self.package_selection_window.raise_()
        self.package_selection_window.activateWindow()

        self.hide()

    def open_pending_payment(
        self,
        subscription: dict,
    ):

        package = subscription.get(
            "package"
        ) or {}

        plan = subscription.get(
            "plan"
        ) or {}

        package_name = package.get(
            "name",
            "Unknown",
        )

        plan_name = plan.get(
            "name",
            "Unknown",
        )

        duration_days = plan.get(
            "duration_days"
        )

        price = plan.get(
            "price",
            0,
        )

        if duration_days is None:

            duration = "Lifetime"

        elif duration_days == 1:

            duration = "1 Day"

        else:

            duration = (
                f"{duration_days} Days"
            )

        self.payment_window = PaymentWindow(
            token=self.token,
            package_name=package_name,
            plan_name=plan_name,
            duration=duration,
            final_price=price,
        )

        self.payment_window.show()
        self.payment_window.raise_()
        self.payment_window.activateWindow()

        self.hide()

    def open_dashboard(self):

        self.dashboard = DashboardWindow(
            self.token
        )

        self.dashboard.show()
        self.dashboard.raise_()
        self.dashboard.activateWindow()

        self.hide()

    def open_register(self):

        self.register_window = RegisterWindow()
        self.register_window.show()
        self.register_window.raise_()
        self.register_window.activateWindow()