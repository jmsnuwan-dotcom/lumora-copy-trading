from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from client.api.dashboard_api import DashboardAPI
from client.api.user_api import UserAPI


class DashboardWindow(QMainWindow):

    def __init__(self, token: str):
        super().__init__()

        self.token = token

        self.setWindowTitle("Lumora Dashboard")
        self.resize(700, 600)

        page = QWidget()
        layout = QVBoxLayout(page)

        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(12)

        self.name = QLabel("Name : -")
        self.email = QLabel("Email : -")
        self.status = QLabel("Status : -")
        self.connection_status = QLabel("Connection : -")

        self.package = QLabel("Package : -")
        self.plan = QLabel("Plan : -")
        self.lot_size = QLabel("Lot Size : -")
        self.expiry = QLabel("Expiry : -")
        self.remaining = QLabel("Remaining Days : -")

        self.signal_button = QPushButton()
        self.signal_button.clicked.connect(
            self.toggle_signals,
        )

        layout.addWidget(self.name)
        layout.addWidget(self.email)
        layout.addWidget(self.status)
        layout.addWidget(self.connection_status)

        layout.addWidget(self.package)
        layout.addWidget(self.plan)
        layout.addWidget(self.lot_size)
        layout.addWidget(self.expiry)
        layout.addWidget(self.remaining)

        layout.addWidget(self.signal_button)

        self.setCentralWidget(page)

        self.load_dashboard()
        
    def load_dashboard(self):

        data = DashboardAPI.get_dashboard(self.token)

        if data is None:
            return

        self.name.setText(
            f"Name : {data['full_name']}"
        )

        self.email.setText(
            f"Email : {data['email']}"
        )

        self.status.setText(
            f"Status : {data['status']}"
        )

        self.connection_status.setText(
            f"Connection : {data['connection_status']}"
        )

        self.package.setText(
            f"Package : {data['package']}"
        )

        self.plan.setText(
            f"Plan : {data['plan']}"
        )

        self.lot_size.setText(
            f"Lot Size : {data['lot_size']}"
        )

        if data["expire_date"]:
            self.expiry.setText(
                f"Expiry : {data['expire_date'][:10]}"
            )
        else:
            self.expiry.setText(
                "Expiry : Lifetime"
            )

        if data["remaining_days"] is None:
            self.remaining.setText(
                "Remaining Days : Unlimited"
            )
        else:
            self.remaining.setText(
                f"Remaining Days : {data['remaining_days']}"
            )

        if data["signals_enabled"]:
            self.signal_button.setText("Signals : ON")
        else:
            self.signal_button.setText("Signals : OFF")

    def toggle_signals(self):

        result = UserAPI.toggle_signals(
            self.token,
        )

        if result is None:
            return

        self.load_dashboard()