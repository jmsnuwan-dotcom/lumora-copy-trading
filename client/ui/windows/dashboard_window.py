from datetime import UTC, datetime

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from client.api.dashboard_api import DashboardAPI
from client.api.subscription_api import SubscriptionAPI
from client.api.user_api import UserAPI
from client.ui.windows.mt5_setup_window import MT5SetupWindow
from client.ui.windows.payment_window import PaymentWindow


class DashboardWindow(QMainWindow):

    def __init__(self, token: str):
        super().__init__()

        self.token = token
        self.mt5_setup_window = None
        self.payment_window = None

        self.redirected_to_payment = False
        self.trial_ends_at = None

        self.setWindowTitle("Lumora Dashboard")
        self.resize(700, 650)

        page = QWidget()
        layout = QVBoxLayout(page)

        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(12)

        self.name = QLabel("Name : -")
        self.email = QLabel("Email : -")
        self.status = QLabel("Status : -")
        self.connection_status = QLabel(
            "Connection : -"
        )

        self.package = QLabel("Package : -")
        self.plan = QLabel("Plan : -")
        self.lot_size = QLabel("Lot Size : -")
        self.expiry = QLabel("Expiry : -")
        self.remaining = QLabel(
            "Remaining Days : -"
        )

        self.trial = QLabel("Trial : -")
        self.countdown = QLabel("")

        self.mt5_button = QPushButton("MT5 Setup")
        self.signal_button = QPushButton()

        self.mt5_button.clicked.connect(
            self.open_mt5_setup
        )

        self.signal_button.clicked.connect(
            self.toggle_signals
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

        layout.addWidget(self.trial)
        layout.addWidget(self.countdown)

        layout.addWidget(self.mt5_button)
        layout.addWidget(self.signal_button)

        self.setCentralWidget(page)

        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(
            self.update_countdown
        )

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(
            self.refresh_dashboard
        )
        self.refresh_timer.start(30000)

        self.load_dashboard()

    def load_dashboard(self):

        try:
            data = DashboardAPI.get_dashboard(
                self.token
            )

        except PermissionError:
            self.open_existing_payment()
            return

        if data is None:
            return

        self.name.setText(
            f"Name : {data['full_name']}"
        )

        self.email.setText(
            f"Email : {data['email']}"
        )

        if data["is_active"]:
            self.status.setText(
                f"Status : {data['status']}"
            )
        else:
            self.status.setText(
                "Status : DEACTIVATED"
            )

        self.connection_status.setText(
            f"Connection : "
            f"{data['connection_status']}"
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
                f"Expiry : "
                f"{data['expire_date'][:10]}"
            )
        else:
            self.expiry.setText(
                "Expiry : Not Started"
            )

        if data["remaining_days"] is None:
            self.remaining.setText(
                "Remaining Days : Not Started"
            )
        else:
            self.remaining.setText(
                f"Remaining Days : "
                f"{data['remaining_days']}"
            )

        if data.get("is_trial"):
            self.trial.setText(
                "Trial : 24 Hour Trial"
            )

            trial_ends_at = data.get(
                "trial_ends_at"
            )

            if trial_ends_at:
                self.start_countdown(
                    trial_ends_at
                )

        else:
            self.trial.setText(
                "Trial : No"
            )

            self.countdown.setText("")
            self.countdown_timer.stop()
            self.trial_ends_at = None

        if data["signals_enabled"]:
            self.signal_button.setText(
                "Signals : ON"
            )
        else:
            self.signal_button.setText(
                "Signals : OFF"
            )

    def refresh_dashboard(self):

        if self.redirected_to_payment:
            return

        self.load_dashboard()

    def open_existing_payment(self):

        subscription = (
            SubscriptionAPI.get_my_subscription(
                self.token
            )
        )

        if subscription is None:
            return

        package = subscription.get(
            "package"
        )

        plan = subscription.get(
            "plan"
        )

        if not package or not plan:
            return

        package_name = package.get(
            "name",
            "",
        )

        plan_name = plan.get(
            "name",
            "",
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

        self.redirected_to_payment = True

        self.refresh_timer.stop()
        self.countdown_timer.stop()

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

    def open_mt5_setup(self):

        self.mt5_setup_window = (
            MT5SetupWindow(
                token=self.token
            )
        )

        self.mt5_setup_window.show()
        self.mt5_setup_window.raise_()
        self.mt5_setup_window.activateWindow()

    def start_countdown(
        self,
        trial_ends_at: str,
    ):

        self.trial_ends_at = (
            self.parse_datetime(
                trial_ends_at
            )
        )

        if self.trial_ends_at is None:
            self.countdown.setText("")
            self.countdown_timer.stop()
            return

        self.update_countdown()
        self.countdown_timer.start(1000)

    def update_countdown(self):

        if not self.trial_ends_at:
            self.countdown_timer.stop()
            return

        now = datetime.now(UTC)

        remaining_seconds = int(
            (
                self.trial_ends_at - now
            ).total_seconds()
        )

        if remaining_seconds <= 0:
            self.countdown.setText(
                "Trial : EXPIRED"
            )

            self.countdown_timer.stop()

            self.load_dashboard()

            return

        hours = remaining_seconds // 3600

        minutes = (
            remaining_seconds % 3600
        ) // 60

        seconds = (
            remaining_seconds % 60
        )

        self.countdown.setText(
            f"Trial Remaining : "
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

    @staticmethod
    def parse_datetime(value):

        if not value:
            return None

        try:
            parsed = datetime.fromisoformat(
                value.replace(
                    "Z",
                    "+00:00",
                )
            )

            if parsed.tzinfo is None:
                parsed = parsed.replace(
                    tzinfo=UTC
                )

            return parsed

        except (
            TypeError,
            ValueError,
        ):
            return None

    def toggle_signals(self):

        result = UserAPI.toggle_signals(
            self.token
        )

        if result is None:
            return

        self.load_dashboard()

    def closeEvent(self, event):

        self.refresh_timer.stop()
        self.countdown_timer.stop()

        event.accept()