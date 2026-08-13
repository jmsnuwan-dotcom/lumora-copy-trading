from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
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


class AdminSignalWindow(QMainWindow):

    def __init__(self, token: str):
        super().__init__()

        self.token = token

        self.setWindowTitle(
            "Lumora AI Trading - Signal Control"
        )
        self.resize(1050, 760)

        self.init_ui()
        self.load_running_signals()
        self.load_signal_history()

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(
            self.refresh_data
        )
        self.refresh_timer.start(10000)

    def init_ui(self):

        page = QWidget()
        page.setObjectName("page")

        layout = QVBoxLayout(page)
        layout.setContentsMargins(
            30, 25, 30, 25
        )
        layout.setSpacing(18)

        # =====================================================
        # HEADER
        # =====================================================

        header = QGroupBox()
        header.setObjectName("header")

        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(
            22, 18, 22, 18
        )

        title = QLabel(
            "Signal Control"
        )
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Send and manage Lumora AI Trading signals."
        )
        subtitle.setObjectName("subtitle")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        layout.addWidget(header)

        # =====================================================
        # SIGNAL CONTROL
        # =====================================================

        trade_box = QGroupBox(
            "QUICK SIGNAL CONTROL"
        )
        trade_box.setObjectName(
            "sectionBox"
        )

        trade_layout = QVBoxLayout(
            trade_box
        )
        trade_layout.setContentsMargins(
            20, 22, 20, 20
        )
        trade_layout.setSpacing(14)

        form = QFormLayout()
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(12)

        self.symbol = QLineEdit()
        self.symbol.setText("XAUUSD")
        self.symbol.setPlaceholderText(
            "Trading Symbol"
        )

        self.trade_id = QLineEdit()
        self.trade_id.setPlaceholderText(
            "Trade ID"
        )

        form.addRow(
            "Symbol",
            self.symbol,
        )

        form.addRow(
            "Trade ID",
            self.trade_id,
        )

        trade_layout.addLayout(form)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.buy_button = QPushButton(
            "BUY SIGNAL"
        )
        self.buy_button.setObjectName(
            "buyButton"
        )

        self.sell_button = QPushButton(
            "SELL SIGNAL"
        )
        self.sell_button.setObjectName(
            "sellButton"
        )

        self.buy_button.clicked.connect(
            self.send_buy
        )

        self.sell_button.clicked.connect(
            self.send_sell
        )

        button_layout.addWidget(
            self.buy_button
        )

        button_layout.addWidget(
            self.sell_button
        )

        trade_layout.addLayout(
            button_layout
        )

        layout.addWidget(
            trade_box
        )

        # =====================================================
        # RUNNING SIGNALS
        # =====================================================

        running_box = QGroupBox(
            "RUNNING SIGNALS"
        )
        running_box.setObjectName(
            "sectionBox"
        )

        running_box_layout = QVBoxLayout(
            running_box
        )
        running_box_layout.setContentsMargins(
            20, 22, 20, 20
        )
        running_box_layout.setSpacing(10)

        self.running_status = QLabel(
            "Loading running signals..."
        )
        self.running_status.setObjectName(
            "statusLabel"
        )

        self.running_layout = QVBoxLayout()
        self.running_layout.setSpacing(8)

        running_container = QWidget()
        running_container.setLayout(
            self.running_layout
        )

        running_scroll = QScrollArea()
        running_scroll.setWidgetResizable(
            True
        )
        running_scroll.setWidget(
            running_container
        )

        running_box_layout.addWidget(
            self.running_status
        )

        running_box_layout.addWidget(
            running_scroll
        )

        layout.addWidget(
            running_box
        )

        # =====================================================
        # SIGNAL HISTORY
        # =====================================================

        history_box = QGroupBox(
            "SIGNAL HISTORY"
        )
        history_box.setObjectName(
            "sectionBox"
        )

        history_box_layout = QVBoxLayout(
            history_box
        )
        history_box_layout.setContentsMargins(
            20, 22, 20, 20
        )
        history_box_layout.setSpacing(10)

        self.history_status = QLabel(
            "Loading signal history..."
        )
        self.history_status.setObjectName(
            "statusLabel"
        )

        self.history_layout = QVBoxLayout()
        self.history_layout.setSpacing(6)

        history_container = QWidget()
        history_container.setLayout(
            self.history_layout
        )

        history_scroll = QScrollArea()
        history_scroll.setWidgetResizable(
            True
        )
        history_scroll.setWidget(
            history_container
        )

        history_box_layout.addWidget(
            self.history_status
        )

        history_box_layout.addWidget(
            history_scroll
        )

        layout.addWidget(
            history_box
        )

        self.setCentralWidget(page)

        # =====================================================
        # STYLE
        # =====================================================

        self.setStyleSheet(
            """
            QWidget#page {
                background: #05050d;
                color: #f5f5f5;
                font-family: "Segoe UI";
                font-size: 13px;
            }

            QGroupBox#header {
                background: #080811;
                border: 1px solid #25253b;
                border-radius: 16px;
            }

            QGroupBox#sectionBox {
                background: #080811;
                border: 1px solid #28283d;
                border-radius: 16px;
                margin-top: 12px;
                padding-top: 18px;
                color: #b94cff;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QGroupBox#sectionBox::title {
                subcontrol-origin: margin;
                left: 18px;
                padding: 0 8px;
                color: #b94cff;
            }

            QLabel#pageTitle {
                color: #ffffff;
                font-size: 28px;
                font-weight: 700;
            }

            QLabel#subtitle {
                color: #8e8ea8;
                font-size: 13px;
                margin-top: 4px;
            }

            QLabel#statusLabel {
                color: #00e6a8;
                font-weight: 600;
                padding: 4px 0;
            }

            QLineEdit {
                background: #07070f;
                border: 1px solid #2b2b42;
                border-radius: 9px;
                padding: 10px 12px;
                color: #ffffff;
                min-height: 22px;
                selection-background-color: #7b3cff;
            }

            QLineEdit:focus {
                border: 1px solid #9b3cff;
            }

            QFormLayout QLabel {
                color: #a9a9c2;
                font-weight: 600;
            }

            QPushButton {
                background: #0b0b16;
                border: 1px solid #30304a;
                border-radius: 9px;
                padding: 10px 16px;
                color: #ffffff;
                font-weight: 600;
                min-height: 20px;
            }

            QPushButton:hover {
                background: #121222;
                border: 1px solid #8b3dff;
            }

            QPushButton:pressed {
                background: #1b1730;
            }

            QPushButton#buyButton {
                background: #063b2c;
                border: 1px solid #00d9a0;
                color: #00e6a8;
                min-height: 42px;
                font-size: 14px;
            }

            QPushButton#buyButton:hover {
                background: #07563f;
            }

            QPushButton#sellButton {
                background: #3b0719;
                border: 1px solid #ff315f;
                color: #ff5478;
                min-height: 42px;
                font-size: 14px;
            }

            QPushButton#sellButton:hover {
                background: #570a25;
            }

            QPushButton#closeButton {
                background: #3a3000;
                border: 1px solid #e4c400;
                color: #ffe44d;
            }

            QPushButton#closeButton:hover {
                background: #504300;
            }

            QLabel#signalCard {
                background: #07070f;
                border: 1px solid #29293f;
                border-radius: 9px;
                padding: 12px;
                color: #dddded;
            }

            QScrollArea {
                background: #080811;
                border: none;
            }

            QScrollArea QWidget {
                background: #080811;
            }

            QScrollArea QViewport {
                background: #080811;
            }

            QScrollBar:horizontal {
                background: #080811;
                height: 8px;
                border-radius: 4px;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                background: #080811;
                border: none;
            }

            QScrollBar::handle:horizontal {
                background: #343450;
                border-radius: 4px;
            }

            QScrollBar:vertical {
                background: #07070f;
                width: 8px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background: #343450;
                border-radius: 4px;
            }
            """
        )

    # =========================================================
    # BUY
    # =========================================================

    def send_buy(self):

        symbol = self.symbol.text().strip()
        trade_id = self.trade_id.text().strip()

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

        self.trade_id.clear()

        self.refresh_data()

    # =========================================================
    # SELL
    # =========================================================

    def send_sell(self):

        symbol = self.symbol.text().strip()
        trade_id = self.trade_id.text().strip()

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

        self.trade_id.clear()

        self.refresh_data()

    # =========================================================
    # CLOSE
    # =========================================================

    def close_signal(
        self,
        signal: dict,
    ):

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

        self.refresh_data()

    # =========================================================
    # RUNNING SIGNALS
    # =========================================================

    def load_running_signals(self):

        signals = AdminAPI.get_running_signals(
            self.token
        )

        self.clear_layout(
            self.running_layout
        )

        if signals is None:

            self.running_status.setText(
                "Unable to load running signals."
            )

            return

        if not signals:

            self.running_status.setText(
                "• 0 RUNNING SIGNALS"
            )

            return

        self.running_status.setText(
            f"• {len(signals)} RUNNING SIGNAL(S)"
        )

        for signal in signals:

            row = QWidget()

            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(
                8, 6, 8, 6
            )
            row_layout.setSpacing(10)

            info = QLabel(
                f'{signal["action"]}   |   '
                f'{signal["symbol"]}   |   '
                f'Magic: {signal["magic_number"]}'
            )

            info.setObjectName(
                "signalCard"
            )

            close_button = QPushButton(
                "CLOSE SIGNAL"
            )

            close_button.setObjectName(
                "closeButton"
            )

            close_button.clicked.connect(
                lambda checked=False,
                data=signal:
                self.close_signal(data)
            )

            row_layout.addWidget(
                info,
                1,
            )

            row_layout.addWidget(
                close_button
            )

            self.running_layout.addWidget(
                row
            )

    # =========================================================
    # HISTORY
    # =========================================================

    def load_signal_history(self):

        signals = AdminAPI.get_signal_history(
            self.token
        )

        self.clear_layout(
            self.history_layout
        )

        if signals is None:

            self.history_status.setText(
                "Unable to load signal history."
            )

            return

        if not signals:

            self.history_status.setText(
                "• 0 SIGNAL HISTORY"
            )

            return

        self.history_status.setText(
            f"• {len(signals)} SIGNAL(S)"
        )

        for signal in signals:

            label = QLabel(
                f'{signal["action"]}   |   '
                f'{signal["symbol"]}   |   '
                f'Status: {signal["status"]}   |   '
                f'Magic: {signal["magic_number"]}'
            )

            label.setObjectName(
                "signalCard"
            )

            self.history_layout.addWidget(
                label
            )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh_data(self):

        self.load_running_signals()
        self.load_signal_history()

    @staticmethod
    def clear_layout(layout):

        while layout.count():

            item = layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def closeEvent(self, event):

        self.refresh_timer.stop()

        event.accept()