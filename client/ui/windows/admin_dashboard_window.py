from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
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


class AdminDashboardWindow(QMainWindow):

    def __init__(self, token: str):
        super().__init__()

        self.token = token

        self.client_window = None
        self.package_window = None
        self.payment_window = None
        self.signal_window = None

        self.setWindowTitle(
            "Lumora AI Trading - Admin Dashboard"
        )

        self.resize(1200, 760)

        self.setStyleSheet(
            """
            QMainWindow {
                background: #05050d;
            }

            QWidget {
                color: #f5f5f7;
                font-family: "Segoe UI";
                font-size: 13px;
            }

            QLabel {
                color: #f5f5f7;
            }

            QLineEdit,
            QComboBox {
                background: #080811;
                border: 1px solid #292943;
                border-radius: 9px;
                padding: 11px;
                color: #f5f5f7;
                min-height: 18px;
            }

            QLineEdit:focus,
            QComboBox:focus {
                border: 1px solid #9b4dff;
            }

            QComboBox::drop-down {
                border: none;
                width: 28px;
            }

            QPushButton {
                background: #0a0a14;
                border: 1px solid #30304a;
                border-radius: 9px;
                padding: 11px 16px;
                color: white;
                font-weight: 600;
            }

            QPushButton:hover {
                border: 1px solid #9b4dff;
                background: #111020;
            }

            QPushButton:pressed {
                background: #17152a;
            }

            QGroupBox {
                background: #080811;
                border: 1px solid #28283f;
                border-radius: 14px;
                margin-top: 14px;
                padding: 18px;
                font-weight: 700;
                color: #b967ff;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
                color: #b967ff;
            }
            """
        )

        self.init_ui()

        self.load_dashboard_stats()

        self.refresh_timer = QTimer(self)

        self.refresh_timer.timeout.connect(
            self.load_dashboard_stats
        )

        self.refresh_timer.start(5000)

        self.load_quick_running_signals()

    # ==========================================================
    # UI
    # ==========================================================

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

        # ======================================================
        # SIDEBAR
        # ======================================================

        sidebar = QWidget()

        sidebar.setFixedWidth(225)

        sidebar.setStyleSheet(
            """
            QWidget {
                background: #070711;
                border-right: 1px solid #202035;
            }
            """
        )

        sidebar_layout = QVBoxLayout(
            sidebar
        )

        sidebar_layout.setContentsMargins(
            18,
            24,
            18,
            24,
        )

        sidebar_layout.setSpacing(8)

        logo = QLabel("LUMORA")

        logo.setAlignment(
            Qt.AlignCenter
        )

        logo.setStyleSheet(
            """
            QLabel {
                color: #19d8ff;
                font-size: 25px;
                font-weight: 800;
                letter-spacing: 2px;
                border: none;
            }
            """
        )

        ai_label = QLabel(
            "AI  TRADING"
        )

        ai_label.setAlignment(
            Qt.AlignCenter
        )

        ai_label.setStyleSheet(
            """
            QLabel {
                color: #c13cff;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 4px;
                border: none;
            }
            """
        )

        admin_label = QLabel(
            "ADMIN PANEL"
        )

        admin_label.setAlignment(
            Qt.AlignCenter
        )

        admin_label.setStyleSheet(
            """
            QLabel {
                color: #77778f;
                font-size: 10px;
                letter-spacing: 2px;
                border: none;
            }
            """
        )

        sidebar_layout.addWidget(
            logo
        )

        sidebar_layout.addWidget(
            ai_label
        )

        sidebar_layout.addWidget(
            admin_label
        )

        sidebar_layout.addSpacing(
            28
        )

        # ------------------------------------------------------
        # Navigation
        # ------------------------------------------------------

        dashboard_button = self.create_nav_button(
            "Dashboard",
            active=True,
        )

        clients_button = self.create_nav_button(
            "Clients"
        )

        packages_button = self.create_nav_button(
            "Packages"
        )

        payments_button = self.create_nav_button(
            "Payments"
        )

        signals_button = self.create_nav_button(
            "Signals"
        )

        settings_button = self.create_nav_button(
            "Settings"
        )

        clients_button.clicked.connect(
            self.open_clients
        )

        packages_button.clicked.connect(
            self.open_packages
        )

        payments_button.clicked.connect(
            self.open_payments
        )

        signals_button.clicked.connect(
            self.open_signals
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

        sidebar_layout.addStretch()

        footer = QLabel(
            "LUMORA AI TRADING\nADMINISTRATOR"
        )

        footer.setAlignment(
            Qt.AlignCenter
        )

        footer.setStyleSheet(
            """
            QLabel {
                color: #5d5d72;
                font-size: 9px;
                letter-spacing: 1px;
                border: none;
            }
            """
        )

        sidebar_layout.addWidget(
            footer
        )

        # ======================================================
        # CONTENT
        # ======================================================

        content = QWidget()

        content_layout = QVBoxLayout(
            content
        )

        content_layout.setContentsMargins(
            28,
            24,
            28,
            24,
        )

        content_layout.setSpacing(18)

        # ======================================================
        # HEADER
        # ======================================================

        header_layout = QHBoxLayout()

        header_box = QVBoxLayout()

        header = QLabel(
            "Admin Dashboard"
        )

        header.setStyleSheet(
            """
            QLabel {
                font-size: 28px;
                font-weight: 800;
                color: white;
            }
            """
        )

        subtitle = QLabel(
            "Manage your Lumora AI Trading platform."
        )

        subtitle.setStyleSheet(
            """
            QLabel {
                color: #8888a0;
                font-size: 13px;
            }
            """
        )

        header_box.addWidget(
            header
        )

        header_box.addWidget(
            subtitle
        )

        header_layout.addLayout(
            header_box
        )

        header_layout.addStretch()

        self.system_online = QLabel(
            "● SYSTEM ONLINE"
        )

        self.system_online.setAlignment(
            Qt.AlignCenter
        )

        self.system_online.setMinimumWidth(
            145
        )

        self.system_online.setMinimumHeight(
            42
        )

        self.system_online.setStyleSheet(
            """
            QLabel {
                background: #061711;
                border: 1px solid #087a55;
                border-radius: 12px;
                color: #00e69a;
                font-weight: 700;
                padding: 8px 14px;
            }
            """
        )

        header_layout.addWidget(
            self.system_online
        )

        content_layout.addLayout(
            header_layout
        )

        # ======================================================
        # STAT CARDS
        # ======================================================

        cards_layout = QHBoxLayout()

        cards_layout.setSpacing(14)

        self.total_clients_card = self.create_stat_card(
            "TOTAL CLIENTS",
            "0",
        )

        self.active_clients_card = self.create_stat_card(
            "ACTIVE CLIENTS",
            "0",
        )

        self.pending_payments_card = self.create_stat_card(
            "PENDING PAYMENTS",
            "0",
        )

        self.running_signals_card = self.create_stat_card(
            "RUNNING SIGNALS",
            "0",
        )

        cards_layout.addWidget(
            self.total_clients_card
        )

        cards_layout.addWidget(
            self.active_clients_card
        )

        cards_layout.addWidget(
            self.pending_payments_card
        )

        cards_layout.addWidget(
            self.running_signals_card
        )

        content_layout.addLayout(
            cards_layout
        )

        # ======================================================
        # SYSTEM STATUS
        # ======================================================

        status_box = QGroupBox(
            "SYSTEM STATUS"
        )

        status_layout = QHBoxLayout(
            status_box
        )

        self.api_status = QLabel(
            "● API : Checking..."
        )

        self.database_status = QLabel(
            "● Database : Connected"
        )

        self.websocket_status = QLabel(
            "● WebSocket : Active"
        )

        for label in (
            self.api_status,
            self.database_status,
            self.websocket_status,
        ):
            label.setStyleSheet(
                """
                QLabel {
                    color: #00e69a;
                    font-weight: 600;
                    padding: 6px;
                }
                """
            )

            status_layout.addWidget(
                label
            )

        content_layout.addWidget(
            status_box
        )

        # ======================================================
        # QUICK SIGNAL CONTROL
        # ======================================================

        signal_box = QGroupBox(
            "QUICK SIGNAL CONTROL"
        )

        signal_layout = QVBoxLayout(
            signal_box
        )

        signal_form = QFormLayout()

        signal_form.setSpacing(
            12
        )

        self.quick_symbol = QLineEdit()

        self.quick_symbol.setText(
            "XAUUSD"
        )

        self.quick_symbol.setPlaceholderText(
            "Trading symbol"
        )

        self.quick_trade_id = QLineEdit()

        self.quick_trade_id.setPlaceholderText(
            "Trade ID"
        )

        self.quick_running_signal = QComboBox()

        self.quick_running_signal.addItem(
            "No running signal",
            None,
        )

        signal_form.addRow(
            "Symbol",
            self.quick_symbol,
        )

        signal_form.addRow(
            "Trade ID",
            self.quick_trade_id,
        )

        signal_form.addRow(
            "Close Signal",
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
            """
            QPushButton {
                background: #063d28;
                border: 1px solid #00b878;
                color: #00e69a;
                min-height: 42px;
            }

            QPushButton:hover {
                background: #075b3a;
            }
            """
        )

        self.quick_sell_button.setStyleSheet(
            """
            QPushButton {
                background: #3b0b17;
                border: 1px solid #e53962;
                color: #ff5578;
                min-height: 42px;
            }

            QPushButton:hover {
                background: #551020;
            }
            """
        )

        self.quick_close_button.setStyleSheet(
            """
            QPushButton {
                background: #352b05;
                border: 1px solid #d7b21d;
                color: #ffe45c;
                min-height: 42px;
            }

            QPushButton:hover {
                background: #51420a;
            }
            """
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

        # ======================================================
        # MAIN
        # ======================================================

        main_layout.addWidget(
            sidebar
        )

        # ------------------------------------------------------
        # SCROLLABLE CONTENT
        # ------------------------------------------------------

        content_scroll = QScrollArea()

        content_scroll.setWidgetResizable(
            True
        )

        content_scroll.setStyleSheet(
            """
            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollArea > QWidget > QWidget {
                background: transparent;
            }

            QScrollBar:vertical {
                background: #080811;
                width: 10px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: #292943;
                border-radius: 5px;
                min-height: 40px;
            }

            QScrollBar::handle:vertical:hover {
                background: #8f42ff;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
            """
        )

        content_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        content_scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        content_scroll.setFrameShape(
            QFrame.NoFrame
        )

        content_scroll.setWidget(
            content
        )

        main_layout.addWidget(
            content_scroll
        )

        self.setCentralWidget(
            page
        )
    # ==========================================================
    # UI HELPERS
    # ==========================================================

    @staticmethod
    def create_nav_button(
        text: str,
        active: bool = False,
    ):

        button = QPushButton(
            text
        )

        button.setMinimumHeight(
            42
        )

        if active:

            button.setStyleSheet(
                """
                QPushButton {
                    background: #171126;
                    border: 1px solid #8f42ff;
                    border-radius: 9px;
                    color: #d68cff;
                    font-weight: 700;
                    text-align: left;
                    padding-left: 16px;
                }

                QPushButton:hover {
                    background: #201737;
                }
                """
            )

        else:

            button.setStyleSheet(
                """
                QPushButton {
                    background: transparent;
                    border: 1px solid transparent;
                    border-radius: 9px;
                    color: #aaaabd;
                    font-weight: 600;
                    text-align: left;
                    padding-left: 16px;
                }

                QPushButton:hover {
                    background: #11111e;
                    border: 1px solid #292943;
                    color: white;
                }
                """
            )

        return button

    @staticmethod
    def create_stat_card(
        title: str,
        value: str,
    ):

        card = QLabel(
            f"{title}\n\n{value}"
        )

        card.setAlignment(
            Qt.AlignCenter
        )

        card.setMinimumHeight(
            105
        )

        card.setStyleSheet(
            """
            QLabel {
                background: #080811;
                border: 1px solid #292943;
                border-radius: 14px;
                padding: 14px;
                color: white;
                font-size: 15px;
                font-weight: 700;
            }
            """
        )

        return card

    # ==========================================================
    # DASHBOARD DATA
    # ==========================================================

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
                "● API : Error"
            )

            self.api_status.setStyleSheet(
                """
                QLabel {
                    color: #ff5578;
                    font-weight: 600;
                    padding: 6px;
                }
                """
            )

            self.system_online.setText(
                "● SYSTEM ERROR"
            )

            self.system_online.setStyleSheet(
                """
                QLabel {
                    background: #210912;
                    border: 1px solid #9b2447;
                    border-radius: 12px;
                    color: #ff5578;
                    font-weight: 700;
                    padding: 8px 14px;
                }
                """
            )

            return

        self.api_status.setText(
            "● API : Connected"
        )

        self.api_status.setStyleSheet(
            """
            QLabel {
                color: #00e69a;
                font-weight: 600;
                padding: 6px;
            }
            """
        )

        self.system_online.setText(
            "● SYSTEM ONLINE"
        )

        active_clients = sum(
            1
            for client in clients
            if client.get("is_active")
        )

        self.total_clients_card.setText(
            f"TOTAL CLIENTS\n\n{len(clients)}"
        )

        self.active_clients_card.setText(
            f"ACTIVE CLIENTS\n\n{active_clients}"
        )

        self.pending_payments_card.setText(
            "PENDING PAYMENTS\n\n"
            f"{len(pending or [])}"
        )

        self.running_signals_card.setText(
            "RUNNING SIGNALS\n\n"
            f"{len(running or [])}"
        )

    # ==========================================================
    # QUICK BUY
    # ==========================================================

    def quick_buy(self):

        symbol = (
            self.quick_symbol
            .text()
            .strip()
        )

        trade_id = (
            self.quick_trade_id
            .text()
            .strip()
        )

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

    # ==========================================================
    # QUICK SELL
    # ==========================================================

    def quick_sell(self):

        symbol = (
            self.quick_symbol
            .text()
            .strip()
        )

        trade_id = (
            self.quick_trade_id
            .text()
            .strip()
        )

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

    # ==========================================================
    # QUICK CLOSE
    # ==========================================================

    def quick_close(self):

        signal = (
            self.quick_running_signal
            .currentData()
        )

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

    # ==========================================================
    # WINDOWS
    # ==========================================================

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

    # ==========================================================
    # RUNNING SIGNALS
    # ==========================================================

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

    # ==========================================================
    # CLOSE EVENT
    # ==========================================================

    def closeEvent(self, event):

        self.refresh_timer.stop()

        event.accept()