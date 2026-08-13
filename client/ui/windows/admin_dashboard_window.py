from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from client.api.admin_api import AdminAPI
from client.ui.windows.admin_client_window import (
    AdminClientWindow,
)
from client.ui.windows.admin_package_window import (
    AdminPackageWindow,
)
from client.ui.windows.admin_payment_window import (
    AdminPaymentWindow,
)
from client.ui.windows.admin_signal_window import (
    AdminSignalWindow,
)
from PySide6.QtCore import Qt, QTimer


class AdminDashboardWindow(QMainWindow):

    def __init__(self, token: str):
        super().__init__()

        self.token = token
        self.client_window = None
        self.package_window = None
        self.payment_window = None
        self.signal_window = None

        self.setWindowTitle(
            "Lumora - Admin Dashboard"
        )
        self.resize(1100, 700)

        self.init_ui()

        self.load_dashboard_stats()

        self.refresh_timer = QTimer(self)

        self.refresh_timer.timeout.connect(
            self.load_dashboard_stats
        )

        self.refresh_timer.start(5000)

        self.load_quick_running_signals()

    def init_ui(self):

        page = QWidget()

        main_layout = QHBoxLayout(page)
        main_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        main_layout.setSpacing(0)

        # ==========================================
        # SIDEBAR
        # ==========================================

        sidebar = QWidget()
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(
            sidebar
        )

        sidebar_layout.setAlignment(
            Qt.AlignTop
        )

        title = QLabel(
            "LUMORA"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        dashboard_button = QPushButton(
            "Dashboard"
        )

        clients_button = QPushButton(
            "Clients"
        )

        clients_button.clicked.connect(
            self.open_clients
        )

        packages_button = QPushButton(
            "Packages"
        )

        packages_button.clicked.connect(
            self.open_packages
        )

        payments_button = QPushButton(
            "Payments"
        )

        payments_button.clicked.connect(
            self.open_payments
        )

        signals_button = QPushButton(
            "Signals"
        )

        signals_button.clicked.connect(
            self.open_signals
        )

        settings_button = QPushButton(
            "Settings"
        )

        sidebar_layout.addWidget(
            title
        )

        sidebar_layout.addSpacing(
            20
        )

        sidebar_layout.addWidget(
            dashboard_button
        )

        sidebar_layout.addWidget(
            clients_button
        )

        sidebar_layout.addWidget(
            packages_button
        )

        sidebar_layout.addWidget(
            payments_button
        )

        sidebar_layout.addWidget(
            signals_button
        )

        sidebar_layout.addWidget(
            settings_button
        )

        # ==========================================
        # CONTENT
        # ==========================================

        content = QWidget()

        content_layout = QVBoxLayout(
            content
        )

        content_layout.setSpacing(18)

        header = QLabel(
            "Admin Dashboard"
        )

        header.setStyleSheet(
            "font-size: 26px; "
            "font-weight: bold;"
        )

        subtitle = QLabel(
            "Lumora Copy Trading"
        )

        content_layout.addWidget(
            header
        )

        content_layout.addWidget(
            subtitle
        )

        # ==========================================
        # STAT CARDS
        # ==========================================

        cards_layout = QHBoxLayout()

        self.total_clients_card = QLabel(
            "Total Clients\n0"
        )

        self.active_clients_card = QLabel(
            "Active Clients\n0"
        )

        self.pending_payments_card = QLabel(
            "Pending Payments\n0"
        )

        self.running_signals_card = QLabel(
            "Running Signals\n0"
        )

        cards = [
            self.total_clients_card,
            self.active_clients_card,
            self.pending_payments_card,
            self.running_signals_card,
        ]

        for card in cards:

            card.setMinimumHeight(100)

            card.setAlignment(
                Qt.AlignCenter
            )

            card.setStyleSheet(
                """
                QLabel {
                    border: 1px solid #333333;
                    border-radius: 10px;
                    padding: 15px;
                    font-size: 16px;
                    font-weight: bold;
                }
                """
            )

            cards_layout.addWidget(
                card
            )

        content_layout.addLayout(
            cards_layout
        )

        # ==========================================
        # SYSTEM STATUS
        # ==========================================

        status_box = QGroupBox(
            "System Status"
        )

        status_layout = QVBoxLayout(
            status_box
        )

        self.api_status = QLabel(
            "API : Checking..."
        )

        self.database_status = QLabel(
            "Database : Connected"
        )

        self.websocket_status = QLabel(
            "WebSocket : Active"
        )

        status_layout.addWidget(
            self.api_status
        )

        status_layout.addWidget(
            self.database_status
        )

        status_layout.addWidget(
            self.websocket_status
        )

        content_layout.addWidget(
            status_box
        )

        # ==========================================
        # QUICK SIGNAL CONTROL
        # ==========================================

        signal_box = QGroupBox(
            "Quick Signal Control"
        )

        signal_layout = QVBoxLayout(
            signal_box
        )

        signal_form = QFormLayout()

        self.quick_symbol = QLineEdit()
        self.quick_symbol.setText("XAUUSD")

        self.quick_trade_id = QLineEdit()

        self.quick_running_signal = QComboBox()
        self.quick_running_signal.addItem(
            "No running signal",
            None,
        )

        signal_form.addRow(
            "Symbol :",
            self.quick_symbol,
        )

        signal_form.addRow(
            "Trade ID :",
            self.quick_trade_id,
        )

        signal_form.addRow(
            "Close Signal :",
            self.quick_running_signal,
        )

        signal_layout.addLayout(
            signal_form
        )

        quick_button_layout = QHBoxLayout()

        self.quick_buy_button = QPushButton(
            "BUY SIGNAL"
        )

        self.quick_sell_button = QPushButton(
            "SELL SIGNAL"
        )

        self.quick_close_button = QPushButton(
            "CLOSE SIGNAL"
        )

        self.quick_buy_button.setStyleSheet(
            "background-color: green; color: white;"
        )

        self.quick_sell_button.setStyleSheet(
            "background-color: red; color: white;"
        )

        self.quick_close_button.setStyleSheet(
            "background-color: yellow; color: black;"
        )

        self.quick_buy_button.clicked.connect(
            self.quick_buy
        )

        self.quick_sell_button.clicked.connect(
            self.quick_sell
        )

        self.quick_close_button.clicked.connect(
            self.quick_close
        )

        quick_button_layout.addWidget(
            self.quick_buy_button
        )

        quick_button_layout.addWidget(
            self.quick_sell_button
        )

        quick_button_layout.addWidget(
            self.quick_close_button
        )

        signal_layout.addLayout(
            quick_button_layout
        )

        content_layout.addWidget(
            signal_box
        )

        content_layout.addStretch()

        # ==========================================
        # MAIN
        # ==========================================

        main_layout.addWidget(
            sidebar
        )

        main_layout.addWidget(
            content
        )

        self.setCentralWidget(page)

    def load_dashboard_stats(self):

        clients = AdminAPI.get_clients(
            self.token
        )

        pending = AdminAPI.get_pending_payments(
            self.token
        )

        running = AdminAPI.get_running_signals(
            self.token
        )

        if clients is None:
            self.api_status.setText(
                "API : Error"
            )
            return

        self.api_status.setText(
            "API : Connected"
        )

        active_clients = sum(
            1
            for client in clients
            if client.get("is_active")
        )

        self.total_clients_card.setText(
            f"Total Clients\n{len(clients)}"
        )

        self.active_clients_card.setText(
            f"Active Clients\n{active_clients}"
        )

        self.pending_payments_card.setText(
            "Pending Payments\n"
            f"{len(pending or [])}"
        )

        self.running_signals_card.setText(
            "Running Signals\n"
            f"{len(running or [])}"
        )

    def quick_buy(self):

        symbol = self.quick_symbol.text().strip()
        trade_id = self.quick_trade_id.text().strip()

        if not symbol:
            QMessageBox.warning(
                self,
                "BUY Failed",
                "Symbol is required.",
            )
            return

        if not trade_id:
            QMessageBox.warning(
                self,
                "BUY Failed",
                "Trade ID is required.",
            )
            return

        result = AdminAPI.buy_trade(
            token=self.token,
            symbol=symbol,
            trade_id=trade_id,
            magic_number=1,
        )

        if result is None:
            QMessageBox.warning(
                self,
                "BUY Failed",
                "Unable to send BUY signal.",
            )
            return

        QMessageBox.information(
            self,
            "BUY Sent",
            "BUY signal sent successfully.",
        )

        self.quick_trade_id.clear()
        self.load_dashboard_stats()
        self.load_quick_running_signals()


    def quick_sell(self):

        symbol = self.quick_symbol.text().strip()
        trade_id = self.quick_trade_id.text().strip()

        if not symbol:
            QMessageBox.warning(
                self,
                "SELL Failed",
                "Symbol is required.",
            )
            return

        if not trade_id:
            QMessageBox.warning(
                self,
                "SELL Failed",
                "Trade ID is required.",
            )
            return

        result = AdminAPI.sell_trade(
            token=self.token,
            symbol=symbol,
            trade_id=trade_id,
            magic_number=1,
        )

        if result is None:
            QMessageBox.warning(
                self,
                "SELL Failed",
                "Unable to send SELL signal.",
            )
            return

        QMessageBox.information(
            self,
            "SELL Sent",
            "SELL signal sent successfully.",
        )

        self.quick_trade_id.clear()
        self.load_dashboard_stats()
        self.load_quick_running_signals()


    def quick_close(self):

        signal = self.quick_running_signal.currentData()

        if signal is None:
            QMessageBox.warning(
                self,
                "CLOSE Failed",
                "Please select a running signal.",
            )
            return

        result = AdminAPI.close_trade(
            token=self.token,
            trade_id=signal["public_id"],
            magic_number=signal["magic_number"],
        )

        if result is None:
            QMessageBox.warning(
                self,
                "CLOSE Failed",
                "Unable to send CLOSE signal.",
            )
            return

        QMessageBox.information(
            self,
            "CLOSE Sent",
            (
                "CLOSE signal sent successfully.\n\n"
                f'Symbol: {signal["symbol"]}\n'
                f'Magic: {signal["magic_number"]}'
            ),
        )

        self.load_dashboard_stats()
        self.load_quick_running_signals()

    def open_clients(self):

        self.client_window = AdminClientWindow(
            self.token
        )

        self.client_window.show()
        self.client_window.raise_()
        self.client_window.activateWindow()

    def open_packages(self):

        self.package_window = AdminPackageWindow(
            self.token
        )

        self.package_window.show()
        self.package_window.raise_()
        self.package_window.activateWindow()

    def open_payments(self):

        self.payment_window = AdminPaymentWindow(
            self.token
        )

        self.payment_window.show()
        self.payment_window.raise_()
        self.payment_window.activateWindow()

    def open_signals(self):

        self.signal_window = AdminSignalWindow(
            self.token
        )

        self.signal_window.show()
        self.signal_window.raise_()
        self.signal_window.activateWindow()

    def load_quick_running_signals(self):

        signals = AdminAPI.get_running_signals(
            self.token
        )

        self.quick_running_signal.clear()

        if signals is None:
            self.quick_running_signal.addItem(
                "Unable to load running signals",
                None,
            )
            return

        if not signals:
            self.quick_running_signal.addItem(
                "No running signal",
                None,
            )
            return

        for signal in signals:

            label = (
                f'{signal["action"]} | '
                f'{signal["symbol"]} | '
                f'Magic: '
                f'{signal["magic_number"]}'
            )

            self.quick_running_signal.addItem(
                label,
                signal,
            )