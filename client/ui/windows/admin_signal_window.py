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
            "Lumora - Signal Control"
        )
        self.resize(850, 750)

        self.init_ui()
        self.load_running_signals()

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(
            self.refresh_data
        )
        self.refresh_timer.start(10000)

    def init_ui(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setSpacing(12)

        # ==========================================
        # SEND SIGNAL
        # ==========================================

        trade_box = QGroupBox(
            "Signal Control"
        )

        trade_layout = QVBoxLayout(
            trade_box
        )

        form = QFormLayout()

        self.symbol = QLineEdit()
        self.symbol.setText("XAUUSD")

        self.trade_id = QLineEdit()

        form.addRow(
            "Symbol :",
            self.symbol,
        )

        form.addRow(
            "Trade ID :",
            self.trade_id,
        )

        trade_layout.addLayout(form)

        button_layout = QHBoxLayout()

        self.buy_button = QPushButton(
            "BUY"
        )

        self.sell_button = QPushButton(
            "SELL"
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

        # ==========================================
        # RUNNING SIGNALS
        # ==========================================

        self.running_status = QLabel(
            "Loading running signals..."
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

        running_box = QGroupBox(
            "Running Signals"
        )

        running_box_layout = QVBoxLayout(
            running_box
        )

        running_box_layout.addWidget(
            self.running_status
        )

        running_box_layout.addWidget(
            running_scroll
        )

        # ==========================================
        # SIGNAL HISTORY
        # ==========================================

        self.history_status = QLabel(
            "Loading signal history..."
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

        history_box = QGroupBox(
            "Signal History"
        )

        history_box_layout = QVBoxLayout(
            history_box
        )

        history_box_layout.addWidget(
            self.history_status
        )

        history_box_layout.addWidget(
            history_scroll
        )

        # ==========================================
        # MAIN
        # ==========================================

        layout.addWidget(
            trade_box
        )

        layout.addWidget(
            running_box
        )

        layout.addWidget(
            history_box
        )

        self.setCentralWidget(page)

    # ==========================================
    # BUY
    # ==========================================

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

    # ==========================================
    # SELL
    # ==========================================

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

    # ==========================================
    # CLOSE
    # ==========================================

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

    # ==========================================
    # RUNNING SIGNALS
    # ==========================================

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
                "No running signals."
            )

            return

        self.running_status.setText(
            f"Running Signals : {len(signals)}"
        )

        for signal in signals:

            row = QWidget()

            row_layout = QHBoxLayout(row)

            info = QLabel(
                f'{signal["action"]} | '
                f'{signal["symbol"]} | '
                f'Magic: '
                f'{signal["magic_number"]}'
            )

            close_button = QPushButton(
                "CLOSE"
            )

            close_button.clicked.connect(
                lambda checked=False,
                data=signal:
                self.close_signal(data)
            )

            row_layout.addWidget(
                info
            )

            row_layout.addWidget(
                close_button
            )

            self.running_layout.addWidget(
                row
            )

    # ==========================================
    # HISTORY
    # ==========================================

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
                "No signal history."
            )

            return

        self.history_status.setText(
            f"History : {len(signals)} signal(s)"
        )

        for signal in signals:

            label = QLabel(
                f'{signal["action"]} | '
                f'{signal["symbol"]} | '
                f'Status: {signal["status"]} | '
                f'Magic: {signal["magic_number"]}'
            )

            self.history_layout.addWidget(
                label
            )

    # ==========================================
    # REFRESH
    # ==========================================

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