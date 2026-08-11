from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
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

        self.setWindowTitle("Lumora - MT5 Setup")
        self.resize(500, 500)

        self.init_ui()
        self.load_existing_connection()
        self.load_saved_symbol()

    def init_ui(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(12)

        title = QLabel("MT5 Setup")
        title.setAlignment(Qt.AlignCenter)

        info = QLabel(
            "Connect your MT5 account to Lumora."
        )

        self.login = QLineEdit()
        self.login.setPlaceholderText(
            "MT5 Login"
        )

        self.password = QLineEdit()
        self.password.setPlaceholderText(
            "MT5 Password"
        )
        self.password.setEchoMode(
            QLineEdit.Password
        )

        self.server = QLineEdit()
        self.server.setPlaceholderText(
            "MT5 Server"
        )

        self.gold_symbol = QComboBox()
        self.gold_symbol.addItem(
            "Select Gold Symbol"
        )

        self.detect_button = QPushButton(
            "Detect Gold Symbols"
        )

        self.save_button = QPushButton(
            "Save & Connect"
        )

        self.status = QLabel(
            "Status : Not connected"
        )

        self.detect_button.clicked.connect(
            self.detect_gold_symbols
        )

        self.save_button.clicked.connect(
            self.save_connection
        )

        layout.addWidget(title)
        layout.addWidget(info)

        layout.addWidget(
            QLabel("MT5 Login")
        )
        layout.addWidget(self.login)

        layout.addWidget(
            QLabel("MT5 Password")
        )
        layout.addWidget(self.password)

        layout.addWidget(
            QLabel("MT5 Server")
        )
        layout.addWidget(self.server)

        layout.addWidget(
            QLabel("Gold Symbol")
        )
        layout.addWidget(self.gold_symbol)

        layout.addWidget(
            self.detect_button
        )

        layout.addWidget(
            self.save_button
        )

        layout.addWidget(self.status)

        self.setCentralWidget(page)

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
            f"Status : {connection['status']}"
        )

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

    def detect_gold_symbols(self):

        login_text = self.login.text().strip()
        password = self.password.text()
        server = self.server.text().strip()

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

        if not MT5Client.connect(
            login=login,
            password=password,
            server=server,
        ):
            QMessageBox.warning(
                self,
                "MT5 Error",
                "Unable to connect to your MT5 account.",
            )
            return

        try:

            symbols = MT5Client.symbols()

            if not symbols:
                QMessageBox.warning(
                    self,
                    "MT5 Error",
                    "No MT5 symbols found.",
                )
                return

            gold_symbols = []

            for symbol in symbols:

                name = symbol.name.upper()

                if "XAUUSD" in name:
                    gold_symbols.append(
                        symbol.name
                    )

            self.gold_symbol.clear()

            if not gold_symbols:

                self.gold_symbol.addItem(
                    "No Gold Symbol Found"
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

                index = self.gold_symbol.findText(
                    saved_symbol
                )

                if index >= 0:
                    self.gold_symbol.setCurrentIndex(
                        index
                    )

            self.status.setText(
                f"Status : "
                f"{len(gold_symbols)} Gold symbol(s) found"
            )

        finally:
            MT5Client.shutdown()
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

        if not MT5Client.connect(
            login=login,
            password=password,
            server=server,
        ):

            QMessageBox.critical(
                self,
                "MT5 Connection Failed",
                "Unable to connect to MT5.",
            )
            return

        account = MT5Client.account_info()

        if account is None:

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
            "Success",
            "MT5 connected successfully.\n\n"
            f"Gold Symbol: {selected_symbol}\n\n"
            "Lumora is now connected.",
        )

        self.status.setText(
            "Status : Connected"
        )