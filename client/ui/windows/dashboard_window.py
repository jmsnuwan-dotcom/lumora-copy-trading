from datetime import UTC, datetime

from PySide6.QtCore import QPointF, Qt, QTimer
from PySide6.QtGui import QFont, QPainter, QPen
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from client.api.dashboard_api import DashboardAPI
from client.api.subscription_api import SubscriptionAPI
from client.api.user_api import UserAPI
from client.services.market_data_service import (
    MarketDataService,
)
from client.storage.symbol_storage import SymbolStorage
from client.ui.windows.mt5_setup_window import MT5SetupWindow
from client.ui.windows.payment_window import PaymentWindow


class XAUUSDChart(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.prices = []
        self.current_price = None

        self.symbol = (
            SymbolStorage.get_gold_symbol()
            or "XAUUSD"
        )

        self.setMinimumHeight(260)

        self.timer = QTimer(self)
        self.timer.timeout.connect(
            self.update_price
        )
        self.timer.start(1000)

        self.update_price()

    def update_price(self):

        try:

            current_symbol = (
                SymbolStorage.get_gold_symbol()
            )

            if current_symbol:
                self.symbol = current_symbol

            price = (
                MarketDataService.update_gold_price()
            )

            if price is None:

                self.current_price = None
                self.update()

                return

            self.current_price = price

            self.prices.append(price)

            if len(self.prices) > 120:
                self.prices.pop(0)

            self.update()

        except Exception:

            self.current_price = None
            self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        # ======================================================
        # HEADER
        # ======================================================

        painter.setPen(
            QPen(Qt.white)
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                13,
                QFont.Bold,
            )
        )

        painter.drawText(
            18,
            25,
            self.symbol,
        )

        if self.current_price is not None:

            painter.setPen(
                QPen(Qt.cyan)
            )

            painter.setFont(
                QFont(
                    "Segoe UI",
                    13,
                    QFont.Bold,
                )
            )

            price_text = (
                f"{self.current_price:.2f}"
            )

            painter.drawText(
                self.width() - 140,
                25,
                price_text,
            )

        else:

            painter.setPen(
                QPen(Qt.gray)
            )

            painter.drawText(
                self.width() - 155,
                25,
                "Waiting for MT5...",
            )

        # ======================================================
        # CHART AREA
        # ======================================================

        left = 18
        top = 45
        right = self.width() - 18
        bottom = self.height() - 18

        painter.setPen(
            QPen(
                Qt.darkGray,
                1,
            )
        )

        painter.drawRect(
            left,
            top,
            right - left,
            bottom - top,
        )

        if len(self.prices) < 2:
            return

        minimum = min(
            self.prices
        )

        maximum = max(
            self.prices
        )

        difference = (
            maximum - minimum
        )

        if difference <= 0:
            difference = 0.01

        chart_width = (
            right - left
        )

        chart_height = (
            bottom - top
        )

        points = []

        total = len(
            self.prices
        )

        for index, price in enumerate(
            self.prices
        ):

            x = (
                left
                + (
                    index
                    / (total - 1)
                )
                * chart_width
            )

            normalized = (
                price - minimum
            ) / difference

            y = (
                bottom
                - normalized
                * chart_height
            )

            points.append(
                QPointF(
                    x,
                    y,
                )
            )

        # ======================================================
        # GRID
        # ======================================================

        painter.setPen(
            QPen(
                Qt.darkGray,
                1,
            )
        )

        for i in range(1, 5):

            y = (
                top
                + (
                    chart_height
                    * i
                    / 5
                )
            )

            painter.drawLine(
                left,
                int(y),
                right,
                int(y),
            )

        # ======================================================
        # PRICE LINE
        # ======================================================

        painter.setPen(
            QPen(
                Qt.cyan,
                2,
            )
        )

        for i in range(
            len(points) - 1
        ):

            painter.drawLine(
                points[i],
                points[i + 1],
            )

    def closeEvent(self, event):

        self.timer.stop()

        event.accept()


class DashboardWindow(QMainWindow):

    def __init__(self, token: str):
        super().__init__()

        self.token = token

        self.mt5_setup_window = None
        self.payment_window = None

        self.redirected_to_payment = False
        self.trial_ends_at = None
        self.chart = None

        self.setWindowTitle(
            "Lumora AI Trading - Dashboard"
        )

        self.resize(
            1050,
            720,
        )

        self.setMinimumSize(
            900,
            650,
        )

        self.init_ui()

        # ======================================================
        # TRIAL COUNTDOWN TIMER
        # ======================================================

        self.countdown_timer = QTimer(
            self
        )

        self.countdown_timer.timeout.connect(
            self.update_countdown
        )

        # ======================================================
        # DASHBOARD REFRESH TIMER
        # ======================================================

        self.refresh_timer = QTimer(
            self
        )

        self.refresh_timer.timeout.connect(
            self.refresh_dashboard
        )

        self.refresh_timer.start(
            30000
        )

        self.load_dashboard()

    # ==========================================================
    # UI
    # ==========================================================

    def init_ui(self):

        page = QWidget()
        page.setObjectName("page")

        main_layout = QVBoxLayout(
            page
        )

        main_layout.setContentsMargins(
            34,
            28,
            34,
            30,
        )

        main_layout.setSpacing(
            18
        )

        # ======================================================
        # HEADER
        # ======================================================

        header = QHBoxLayout()

        brand_layout = QVBoxLayout()
        brand_layout.setSpacing(1)

        brand = QLabel(
            "LUMORA"
        )

        brand.setObjectName(
            "brand"
        )

        brand_subtitle = QLabel(
            "AI TRADING"
        )

        brand_subtitle.setObjectName(
            "brandSubtitle"
        )

        brand_layout.addWidget(
            brand
        )

        brand_layout.addWidget(
            brand_subtitle
        )

        header.addLayout(
            brand_layout
        )

        header.addStretch()

        self.system_status = QLabel(
            "● SYSTEM ONLINE"
        )

        self.system_status.setObjectName(
            "systemStatus"
        )

        header.addWidget(
            self.system_status
        )

        main_layout.addLayout(
            header
        )

        # ======================================================
        # WELCOME CARD
        # ======================================================

        welcome_card = QFrame()

        welcome_card.setObjectName(
            "welcomeCard"
        )

        welcome_layout = QVBoxLayout(
            welcome_card
        )

        welcome_layout.setContentsMargins(
            24,
            20,
            24,
            20,
        )

        welcome_layout.setSpacing(
            5
        )

        welcome_title = QLabel(
            "Welcome to Lumora AI Trading"
        )

        welcome_title.setObjectName(
            "welcomeTitle"
        )

        welcome_info = QLabel(
            "Manage your trading connection, "
            "package and signal access."
        )

        welcome_info.setObjectName(
            "welcomeInfo"
        )

        welcome_layout.addWidget(
            welcome_title
        )

        welcome_layout.addWidget(
            welcome_info
        )

        main_layout.addWidget(
            welcome_card
        )

        # ======================================================
        # ACCOUNT + PACKAGE
        # ======================================================

        top_cards = QHBoxLayout()

        top_cards.setSpacing(
            18
        )

        # ------------------------------------------------------
        # ACCOUNT CARD
        # ------------------------------------------------------

        account_card = QFrame()

        account_card.setObjectName(
            "card"
        )

        account_layout = QVBoxLayout(
            account_card
        )

        account_layout.setContentsMargins(
            24,
            22,
            24,
            22,
        )

        account_layout.setSpacing(
            12
        )

        account_title = QLabel(
            "ACCOUNT"
        )

        account_title.setObjectName(
            "sectionTitle"
        )

        self.name = QLabel(
            "Name : -"
        )

        self.email = QLabel(
            "Email : -"
        )

        self.status = QLabel(
            "Status : -"
        )

        self.connection_status = QLabel(
            "Connection : -"
        )

        for label in (
            self.name,
            self.email,
            self.status,
            self.connection_status,
        ):

            label.setObjectName(
                "dataLabel"
            )

        account_layout.addWidget(
            account_title
        )

        account_layout.addWidget(
            self.name
        )

        account_layout.addWidget(
            self.email
        )

        account_layout.addWidget(
            self.status
        )

        account_layout.addWidget(
            self.connection_status
        )

        top_cards.addWidget(
            account_card
        )

        # ------------------------------------------------------
        # TRADING PACKAGE CARD
        # ------------------------------------------------------

        package_card = QFrame()

        package_card.setObjectName(
            "card"
        )

        package_layout = QVBoxLayout(
            package_card
        )

        package_layout.setContentsMargins(
            24,
            22,
            24,
            22,
        )

        package_layout.setSpacing(
            12
        )

        package_title = QLabel(
            "TRADING PACKAGE"
        )

        package_title.setObjectName(
            "sectionTitle"
        )

        self.package = QLabel(
            "Package : -"
        )

        self.plan = QLabel(
            "Plan : -"
        )

        self.lot_size = QLabel(
            "Lot Size : -"
        )

        self.expiry = QLabel(
            "Expiry : -"
        )

        self.remaining = QLabel(
            "Remaining Days : -"
        )

        for label in (
            self.package,
            self.plan,
            self.lot_size,
            self.expiry,
            self.remaining,
        ):

            label.setObjectName(
                "dataLabel"
            )

        package_layout.addWidget(
            package_title
        )

        package_layout.addWidget(
            self.package
        )

        package_layout.addWidget(
            self.plan
        )

        package_layout.addWidget(
            self.lot_size
        )

        package_layout.addWidget(
            self.expiry
        )

        package_layout.addWidget(
            self.remaining
        )

        top_cards.addWidget(
            package_card
        )

        main_layout.addLayout(
            top_cards
        )

        # ======================================================
        # LIVE MARKET CHART
        # ======================================================

        chart_card = QFrame()

        chart_card.setObjectName(
            "chartCard"
        )

        chart_layout = QVBoxLayout(
            chart_card
        )

        chart_layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )

        chart_title = QLabel(
            "XAUUSD LIVE MARKET"
        )

        chart_title.setObjectName(
            "sectionTitle"
        )

        self.chart = XAUUSDChart()

        chart_layout.addWidget(
            chart_title
        )

        chart_layout.addWidget(
            self.chart
        )

        main_layout.addWidget(
            chart_card
        )

        # ======================================================
        # TRIAL CARD
        # ======================================================

        trial_card = QFrame()

        trial_card.setObjectName(
            "trialCard"
        )

        trial_layout = QVBoxLayout(
            trial_card
        )

        trial_layout.setContentsMargins(
            24,
            20,
            24,
            20,
        )

        trial_layout.setSpacing(
            8
        )

        trial_title = QLabel(
            "TRIAL STATUS"
        )

        trial_title.setObjectName(
            "sectionTitle"
        )

        self.trial = QLabel(
            "Trial : -"
        )

        self.trial.setObjectName(
            "trialValue"
        )

        self.countdown = QLabel(
            ""
        )

        self.countdown.setObjectName(
            "countdown"
        )

        self.countdown.setAlignment(
            Qt.AlignCenter
        )

        trial_layout.addWidget(
            trial_title
        )

        trial_layout.addWidget(
            self.trial
        )

        trial_layout.addWidget(
            self.countdown
        )

        main_layout.addWidget(
            trial_card
        )

        # ======================================================
        # ACTION BUTTONS
        # ======================================================

        actions = QHBoxLayout()

        actions.setSpacing(
            14
        )

        self.mt5_button = QPushButton(
            "MT5 Setup"
        )

        self.mt5_button.setObjectName(
            "secondaryButton"
        )

        self.signal_button = QPushButton(
            "Signals : OFF"
        )

        self.signal_button.setObjectName(
            "signalOff"
        )

        self.mt5_button.clicked.connect(
            self.open_mt5_setup
        )

        self.signal_button.clicked.connect(
            self.toggle_signals
        )

        actions.addWidget(
            self.mt5_button
        )

        actions.addWidget(
            self.signal_button
        )

        main_layout.addLayout(
            actions
        )

        self.setCentralWidget(
            page
        )

        # ======================================================
        # STYLE
        # ======================================================

        self.setStyleSheet(
            """
            QMainWindow {
                background: #05050d;
            }

            QWidget#page {
                background:
                    qlineargradient(
                        x1: 0, y1: 0,
                        x2: 1, y2: 1,
                        stop: 0 #05050d,
                        stop: 0.55 #070713,
                        stop: 1 #100519
                    );
                color: #ffffff;
            }

            QLabel {
                font-family: "Segoe UI";
            }

            QLabel#brand {
                color: #18d8ff;
                font-size: 25px;
                font-weight: 800;
                letter-spacing: 2px;
            }

            QLabel#brandSubtitle {
                color: #b83cff;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 3px;
            }

            QLabel#systemStatus {
                color: #25e99a;
                background: #07150f;
                border: 1px solid #17744f;
                border-radius: 14px;
                padding: 9px 15px;
                font-size: 11px;
                font-weight: 700;
            }

            QFrame#welcomeCard {
                background: #080812;
                border: 1px solid #29293e;
                border-radius: 17px;
            }

            QLabel#welcomeTitle {
                color: #ffffff;
                font-size: 23px;
                font-weight: 700;
            }

            QLabel#welcomeInfo {
                color: #85859d;
                font-size: 13px;
            }

            QFrame#card {
                background: #080812;
                border: 1px solid #29293e;
                border-radius: 17px;
            }

            QFrame#card:hover {
                border: 1px solid #54328b;
            }

            QLabel#sectionTitle {
                color: #b65cff;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 2px;
            }

            QLabel#dataLabel {
                color: #dcdceb;
                font-size: 13px;
            }

            QFrame#trialCard {
                background: #080812;
                border: 1px solid #59328c;
                border-radius: 17px;
            }

            QLabel#trialValue {
                color: #ffffff;
                font-size: 14px;
                font-weight: 600;
            }

            QLabel#countdown {
                color: #22dfff;
                font-size: 23px;
                font-weight: 800;
                padding: 8px;
            }

            QPushButton {
                min-height: 48px;
                border-radius: 10px;
                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 700;
            }

            QPushButton#secondaryButton {
                background: #080812;
                color: #ffffff;
                border: 1px solid #1edcff;
            }

            QPushButton#secondaryButton:hover {
                background: #0e1220;
                border: 1px solid #a83cff;
            }

            QPushButton#signalOff {
                background: #100b14;
                color: #ff5d79;
                border: 1px solid #b52b50;
            }

            QPushButton#signalOff:hover {
                background: #1b0d17;
                border: 1px solid #ff4770;
            }

            QPushButton#signalOn {
                background: #071a12;
                color: #29efa0;
                border: 1px solid #1fc57c;
            }

            QPushButton#signalOn:hover {
                background: #0b2519;
                border: 1px solid #2cffae;
            }

            QFrame#chartCard {
                background: #080812;
                border: 1px solid #29293e;
                border-radius: 17px;
            }

            QFrame#chartCard:hover {
                border: 1px solid #54328b;
            }
            """
        )

    # ==========================================================
    # LOAD DASHBOARD
    # ==========================================================

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

            self.countdown.setText(
                ""
            )

            self.countdown_timer.stop()

            self.trial_ends_at = None

        if data["signals_enabled"]:

            self.signal_button.setText(
                "Signals : ON"
            )

            self.signal_button.setObjectName(
                "signalOn"
            )

        else:

            self.signal_button.setText(
                "Signals : OFF"
            )

            self.signal_button.setObjectName(
                "signalOff"
            )

        self.signal_button.style().unpolish(
            self.signal_button
        )

        self.signal_button.style().polish(
            self.signal_button
        )

    # ==========================================================
    # REFRESH
    # ==========================================================

    def refresh_dashboard(self):

        if self.redirected_to_payment:
            return

        self.load_dashboard()

    # ==========================================================
    # EXISTING PAYMENT
    # ==========================================================

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

        if self.chart is not None:
            self.chart.timer.stop()

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

    # ==========================================================
    # MT5 SETUP
    # ==========================================================

    def open_mt5_setup(self):

        self.mt5_setup_window = (
            MT5SetupWindow(
                token=self.token
            )
        )

        self.mt5_setup_window.show()
        self.mt5_setup_window.raise_()
        self.mt5_setup_window.activateWindow()

    # ==========================================================
    # TRIAL COUNTDOWN
    # ==========================================================

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

            self.countdown.setText(
                ""
            )

            self.countdown_timer.stop()

            return

        self.update_countdown()

        self.countdown_timer.start(
            1000
        )

    def update_countdown(self):

        if not self.trial_ends_at:

            self.countdown_timer.stop()

            return

        now = datetime.now(UTC)

        remaining_seconds = int(
            (
                self.trial_ends_at
                - now
            ).total_seconds()
        )

        if remaining_seconds <= 0:

            self.countdown.setText(
                "Trial : EXPIRED"
            )

            self.countdown_timer.stop()

            self.load_dashboard()

            return

        hours = (
            remaining_seconds
            // 3600
        )

        minutes = (
            remaining_seconds
            % 3600
        ) // 60

        seconds = (
            remaining_seconds
            % 60
        )

        self.countdown.setText(
            f"Trial Remaining : "
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

    # ==========================================================
    # DATETIME
    # ==========================================================

    @staticmethod
    def parse_datetime(value):

        if not value:
            return None

        try:

            parsed = (
                datetime.fromisoformat(
                    value.replace(
                        "Z",
                        "+00:00",
                    )
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

    # ==========================================================
    # SIGNAL TOGGLE
    # ==========================================================

    def toggle_signals(self):

        result = UserAPI.toggle_signals(
            self.token
        )

        if result is None:
            return

        self.load_dashboard()

    # ==========================================================
    # CLOSE
    # ==========================================================

    def closeEvent(self, event):

        self.refresh_timer.stop()
        self.countdown_timer.stop()

        if self.chart is not None:
            self.chart.timer.stop()

        event.accept()