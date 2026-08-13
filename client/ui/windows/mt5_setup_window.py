from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from client.api.connection_api import ConnectionAPI
from client.mt5.mt5_client import MT5Client
from client.storage.symbol_storage import SymbolStorage
from client.services.client_service import ClientService


class MT5SetupWindow(QMainWindow):

    def __init__(self, token: str):
        super().__init__()

        self.token = token

        self.setWindowTitle(
            "Lumora AI Trading - MT5 Setup"
        )
        self.resize(760, 680)
        self.setMinimumSize(680, 600)

        self.init_ui()
        self.load_existing_connection()
        self.load_saved_symbol()

    # ==========================================================
    # UI
    # ==========================================================

    def init_ui(self):

        page = QWidget()
        page.setObjectName("page")

        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(
            35, 28, 35, 30
        )
        main_layout.setSpacing(18)

        # ======================================================
        # HEADER
        # ======================================================

        header = QHBoxLayout()

        brand_layout = QVBoxLayout()
        brand_layout.setSpacing(1)

        brand = QLabel("LUMORA")
        brand.setObjectName("brand")

        brand_subtitle = QLabel(
            "AI TRADING"
        )
        brand_subtitle.setObjectName(
            "brandSubtitle"
        )

        brand_layout.addWidget(brand)
        brand_layout.addWidget(
            brand_subtitle
        )

        header.addLayout(brand_layout)
        header.addStretch()

        connection_badge = QLabel(
            "● MT5 CONNECTION"
        )
        connection_badge.setObjectName(
            "connectionBadge"
        )

        header.addWidget(
            connection_badge
        )

        main_layout.addLayout(header)

        # ======================================================
        # TITLE
        # ======================================================

        title = QLabel(
            "Connect Your MT5 Account"
        )
        title.setObjectName("title")
        title.setAlignment(
            Qt.AlignCenter
        )

        info = QLabel(
            "Connect your MetaTrader 5 account "
            "to start using Lumora AI Trading."
        )
        info.setObjectName("info")
        info.setAlignment(
            Qt.AlignCenter
        )
        info.setWordWrap(True)

        main_layout.addWidget(title)
        main_layout.addWidget(info)

        # ======================================================
        # MT5 ACCOUNT CARD
        # ======================================================

        account_card = QFrame()
        account_card.setObjectName(
            "card"
        )

        account_layout = QVBoxLayout(
            account_card
        )
        account_layout.setContentsMargins(
            25, 22, 25, 22
        )
        account_layout.setSpacing(10)

        account_title = QLabel(
            "MT5 ACCOUNT"
        )
        account_title.setObjectName(
            "sectionTitle"
        )

        account_layout.addWidget(
            account_title
        )

        login_label = QLabel(
            "MT5 Login"
        )
        login_label.setObjectName(
            "fieldLabel"
        )

        self.login = QLineEdit()
        self.login.setPlaceholderText(
            "Enter MT5 Login"
        )

        password_label = QLabel(
            "MT5 Password"
        )
        password_label.setObjectName(
            "fieldLabel"
        )

        self.password = QLineEdit()
        self.password.setPlaceholderText(
            "Enter MT5 Password"
        )
        self.password.setEchoMode(
            QLineEdit.Password
        )

        server_label = QLabel(
            "MT5 Server"
        )
        server_label.setObjectName(
            "fieldLabel"
        )

        self.server = QLineEdit()
        self.server.setPlaceholderText(
            "Enter MT5 Server"
        )

        account_layout.addWidget(
            login_label
        )
        account_layout.addWidget(
            self.login
        )

        account_layout.addWidget(
            password_label
        )
        account_layout.addWidget(
            self.password
        )

        account_layout.addWidget(
            server_label
        )
        account_layout.addWidget(
            self.server
        )

        main_layout.addWidget(
            account_card
        )

        # ======================================================
        # GOLD SYMBOL CARD
        # ======================================================

        symbol_card = QFrame()
        symbol_card.setObjectName(
            "card"
        )

        symbol_layout = QVBoxLayout(
            symbol_card
        )
        symbol_layout.setContentsMargins(
            25, 22, 25, 22
        )
        symbol_layout.setSpacing(10)

        symbol_title = QLabel(
            "GOLD TRADING SYMBOL"
        )
        symbol_title.setObjectName(
            "sectionTitle"
        )

        symbol_info = QLabel(
            "Detect the Gold / XAUUSD symbol "
            "available in your MT5 terminal."
        )
        symbol_info.setObjectName(
            "smallInfo"
        )

        self.gold_symbol = QComboBox()
        self.gold_symbol.addItem(
            "Select Gold Symbol"
        )

        self.detect_button = QPushButton(
            "Detect Gold Symbols"
        )
        self.detect_button.setObjectName(
            "secondaryButton"
        )

        symbol_layout.addWidget(
            symbol_title
        )
        symbol_layout.addWidget(
            symbol_info
        )
        symbol_layout.addWidget(
            self.gold_symbol
        )
        symbol_layout.addWidget(
            self.detect_button
        )

        main_layout.addWidget(
            symbol_card
        )

        # ======================================================
        # STATUS CARD
        # ======================================================

        status_card = QFrame()
        status_card.setObjectName(
            "statusCard"
        )

        status_layout = QHBoxLayout(
            status_card
        )
        status_layout.setContentsMargins(
            18, 13, 18, 13
        )

        status_title = QLabel(
            "STATUS"
        )
        status_title.setObjectName(
            "statusTitle"
        )

        self.status = QLabel(
            "Not connected"
        )
        self.status.setObjectName(
            "statusValue"
        )

        status_layout.addWidget(
            status_title
        )
        status_layout.addStretch()
        status_layout.addWidget(
            self.status
        )

        main_layout.addWidget(
            status_card
        )

        # ======================================================
        # SAVE BUTTON
        # ======================================================

        self.save_button = QPushButton(
            "Save & Connect"
        )
        self.save_button.setObjectName(
            "primaryButton"
        )

        main_layout.addWidget(
            self.save_button
        )

        # ======================================================
        # CONNECTIONS
        # ======================================================

        self.detect_button.clicked.connect(
            self.detect_gold_symbols
        )

        self.save_button.clicked.connect(
            self.save_connection
        )

        self.setCentralWidget(page)

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
                color: #e9e9f5;
                font-family: "Segoe UI";
                font-size: 13px;
            }

            QLabel#brand {
                color: #20d6ff;
                font-size: 24px;
                font-weight: 800;
                letter-spacing: 2px;
            }

            QLabel#brandSubtitle {
                color: #b44cff;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 3px;
            }

            QLabel#connectionBadge {
                color: #20dfff;
                background: #07131a;
                border: 1px solid #155d72;
                border-radius: 14px;
                padding: 8px 14px;
                font-size: 11px;
                font-weight: 700;
            }

            QLabel#title {
                color: #ffffff;
                font-size: 25px;
                font-weight: 700;
                margin-top: 4px;
            }

            QLabel#info {
                color: #85859d;
                font-size: 13px;
                margin-bottom: 4px;
            }

            QFrame#card {
                background: rgba(8, 8, 18, 245);
                border: 1px solid #28283d;
                border-radius: 17px;
            }

            QFrame#card:hover {
                border: 1px solid #5b36a0;
            }

            QLabel#sectionTitle {
                color: #b96cff;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 2px;
            }

            QLabel#fieldLabel {
                color: #a7a7bb;
                font-size: 12px;
                font-weight: 600;
                margin-top: 2px;
            }

            QLabel#smallInfo {
                color: #73738b;
                font-size: 11px;
            }

            QLineEdit {
                background: #070711;
                color: #ffffff;
                border: 1px solid #29293d;
                border-radius: 9px;
                padding: 11px 13px;
                min-height: 20px;
                font-size: 13px;
            }

            QLineEdit:focus {
                border: 1px solid #8c38ff;
                background: #090914;
            }

            QLineEdit::placeholder {
                color: #646477;
            }

            QComboBox {
                background: #070711;
                color: #ffffff;
                border: 1px solid #29293d;
                border-radius: 9px;
                padding: 11px 13px;
                min-height: 20px;
                font-size: 13px;
            }

            QComboBox:hover {
                border: 1px solid #5931a0;
            }

            QComboBox:focus {
                border: 1px solid #8c38ff;
            }

            QComboBox QAbstractItemView {
                background: #090914;
                color: #ffffff;
                border: 1px solid #38384e;
                selection-background-color: #54259a;
                selection-color: #ffffff;
                padding: 5px;
            }

            QPushButton {
                min-height: 44px;
                border-radius: 9px;
                font-size: 13px;
                font-weight: 700;
            }

            QPushButton#secondaryButton {
                background: #090912;
                color: #ffffff;
                border: 1px solid #20d9ff;
            }

            QPushButton#secondaryButton:hover {
                background: #101426;
                border: 1px solid #9d3cff;
            }

            QPushButton#secondaryButton:pressed {
                background: #15152a;
            }

            QPushButton#primaryButton {
                background:
                    qlineargradient(
                        x1: 0, y1: 0,
                        x2: 1, y2: 0,
                        stop: 0 #079ff0,
                        stop: 0.5 #5364ff,
                        stop: 1 #d52aff
                    );
                color: #ffffff;
                border: none;
                min-height: 50px;
                font-size: 14px;
            }

            QPushButton#primaryButton:hover {
                background:
                    qlineargradient(
                        x1: 0, y1: 0,
                        x2: 1, y2: 0,
                        stop: 0 #12b8ff,
                        stop: 0.5 #685cff,
                        stop: 1 #e53aff
                    );
            }

            QPushButton#primaryButton:pressed {
                background: #6030bd;
            }

            QFrame#statusCard {
                background: #070711;
                border: 1px solid #28283d;
                border-radius: 12px;
            }

            QLabel#statusTitle {
                color: #77778e;
                font-size: 10px;
                font-weight: 800;
                letter-spacing: 2px;
            }

            QLabel#statusValue {
                color: #27df92;
                font-size: 13px;
                font-weight: 700;
            }
            """
        )

    # ==========================================================
    # LOAD EXISTING CONNECTION
    # ==========================================================

    def load_existing_connection(self):

        connection = (
            ConnectionAPI.get_my_connection(
                self.token
            )
        )

        if connection is None:
            return

        self.login.setText(
            str(connection["mt5_login"])
        )

        self.server.setText(
            connection["mt5_server"]
        )

        self.status.setText(
            str(connection["status"])
        )

    # ==========================================================
    # LOAD SAVED SYMBOL
    # ==========================================================

    def load_saved_symbol(self):

        saved_symbol = (
            SymbolStorage.get_gold_symbol()
        )

        if not saved_symbol:
            return

        index = self.gold_symbol.findText(
            saved_symbol
        )

        if index >= 0:
            self.gold_symbol.setCurrentIndex(
                index
            )

    # ==========================================================
    # DETECT GOLD SYMBOLS
    # ==========================================================

    def detect_gold_symbols(self):

        login_text = (
            self.login.text().strip()
        )

        password = self.password.text()

        server = (
            self.server.text().strip()
        )

        if not login_text:
            QMessageBox.warning(
                self,
                "Validation",
                "Enter MT5 Login.",
            )
            return

        if not password:
            QMessageBox.warning(
                self,
                "Validation",
                "Enter MT5 Password.",
            )
            return

        if not server:
            QMessageBox.warning(
                self,
                "Validation",
                "Enter MT5 Server.",
            )
            return

        try:
            login = int(login_text)

        except ValueError:
            QMessageBox.warning(
                self,
                "Validation",
                "MT5 Login must be a number.",
            )
            return

        self.status.setText(
            "Connecting to MT5..."
        )

        if not MT5Client.connect(
            login=login,
            password=password,
            server=server,
        ):
            self.status.setText(
                "Connection failed"
            )

            QMessageBox.warning(
                self,
                "MT5 Error",
                "Unable to connect to your MT5 account.",
            )
            return

        try:

            symbols = MT5Client.symbols()

            if not symbols:

                self.status.setText(
                    "No symbols found"
                )

                QMessageBox.warning(
                    self,
                    "MT5 Error",
                    "No MT5 symbols found.",
                )
                return

            gold_symbols = []

            for symbol in symbols:

                name = (
                    symbol.name or ""
                ).upper()

                description = (
                    symbol.description or ""
                ).upper()

                path = (
                    symbol.path or ""
                ).upper()

                is_xau_usd = (
                    "XAUUSD" in name
                )

                is_gold_symbol = (
                    "GOLD" in name
                    and "STOCKS" not in path
                    and "ETF" not in path
                )

                is_gold_description = (
                    "GOLD" in description
                    and (
                        "METAL" in path
                        or "SPOT" in path
                    )
                    and "STOCKS" not in path
                    and "ETF" not in path
                )

                if (
                    is_xau_usd
                    or is_gold_symbol
                    or is_gold_description
                ):
                    gold_symbols.append(
                        symbol.name
                    )

            self.gold_symbol.clear()

            if not gold_symbols:

                self.gold_symbol.addItem(
                    "No Gold Symbol Found"
                )

                self.status.setText(
                    "No Gold symbol found"
                )

                QMessageBox.warning(
                    self,
                    "Gold Symbol",
                    "No Gold symbol was found "
                    "in your MT5 terminal.",
                )

                return

            self.gold_symbol.addItems(
                sorted(set(gold_symbols))
            )

            saved_symbol = (
                SymbolStorage.get_gold_symbol()
            )

            if saved_symbol:

                index = (
                    self.gold_symbol.findText(
                        saved_symbol
                    )
                )

                if index >= 0:
                    self.gold_symbol.setCurrentIndex(
                        index
                    )

            self.status.setText(
                f"{len(gold_symbols)} "
                "Gold symbol(s) found"
            )

        finally:
            MT5Client.shutdown()

    # ==========================================================
    # SAVE CONNECTION
    # ==========================================================

    def save_connection(self):

        login_text = (
            self.login.text().strip()
        )

        password = (
            self.password.text()
        )

        server = (
            self.server.text().strip()
        )

        selected_symbol = (
            self.gold_symbol.currentText()
        )

        if not login_text:
            QMessageBox.warning(
                self,
                "Validation",
                "Enter MT5 Login.",
            )
            return

        if not password:
            QMessageBox.warning(
                self,
                "Validation",
                "Enter MT5 Password.",
            )
            return

        if not server:
            QMessageBox.warning(
                self,
                "Validation",
                "Enter MT5 Server.",
            )
            return

        if (
            not selected_symbol
            or selected_symbol
            == "Select Gold Symbol"
            or selected_symbol
            == "No Gold Symbol Found"
        ):
            QMessageBox.warning(
                self,
                "Validation",
                "Select your Gold symbol.",
            )
            return

        try:
            login = int(login_text)

        except ValueError:

            QMessageBox.warning(
                self,
                "Validation",
                "MT5 Login must be a number.",
            )
            return

        self.status.setText(
            "Connecting to MT5..."
        )

        if not MT5Client.connect(
            login=login,
            password=password,
            server=server,
        ):

            self.status.setText(
                "Connection failed"
            )

            QMessageBox.critical(
                self,
                "MT5 Connection Failed",
                "Unable to connect to MT5.",
            )
            return

        account = MT5Client.account_info()

        if account is None:

            self.status.setText(
                "Account information unavailable"
            )

            QMessageBox.critical(
                self,
                "MT5 Error",
                "MT5 account information "
                "is unavailable.",
            )

            MT5Client.shutdown()
            return

        success = ConnectionAPI.save(
            self.token
        )

        if not success:

            self.status.setText(
                "Save failed"
            )

            QMessageBox.critical(
                self,
                "Save Failed",
                "MT5 connection could not "
                "be saved.",
            )

            MT5Client.shutdown()
            return

        SymbolStorage.save_gold_symbol(
            selected_symbol
        )

        MT5Client.shutdown()

        ClientService.start(
            token=self.token,
            mt5_login=login,
            mt5_password=password,
            mt5_server=server,
        )

        QMessageBox.information(
            self,
            "Connection Successful",
            "MT5 connected successfully.\n\n"
            f"Gold Symbol: {selected_symbol}\n\n"
            "Lumora AI Trading is now connected.",
        )

        self.status.setText(
            "Connected"
        )