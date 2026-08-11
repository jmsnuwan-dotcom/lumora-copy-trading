from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from client.api.payment_api import PaymentAPI


class PaymentWindow(QMainWindow):

    def __init__(
        self,
        token: str,
        package_name: str,
        plan_name: str,
        duration: str,
        final_price: str,
    ):
        super().__init__()

        self.token = token
        self.package_name = package_name
        self.plan_name = plan_name
        self.duration = duration
        self.final_price = final_price
        self.selected_file = None
        self.payment_submitted = False

        self.setWindowTitle("Lumora Payment")
        self.resize(600, 650)

        page = QWidget()
        layout = QVBoxLayout(page)

        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(12)

        title = QLabel("Complete Your Payment")
        title.setAlignment(Qt.AlignCenter)

        subscription_details = QLabel(
            f"Package: {self.package_name}\n"
            f"Plan: {self.plan_name}\n"
            f"Duration: {self.duration}\n"
            f"Final Price: ${self.final_price}"
        )
        subscription_details.setAlignment(Qt.AlignCenter)
        subscription_details.setWordWrap(True)

        self.status_label = QLabel(
            "Payment Status : Not Submitted"
        )
        self.status_label.setAlignment(Qt.AlignCenter)

        self.bank_details = QLabel(
            "Loading bank payment details..."
        )
        self.bank_details.setAlignment(Qt.AlignLeft)
        self.bank_details.setWordWrap(True)

        self.crypto_details = QLabel(
            "Loading crypto payment details..."
        )
        self.crypto_details.setAlignment(Qt.AlignLeft)
        self.crypto_details.setWordWrap(True)

        self.file_label = QLabel(
            "No payment slip selected."
        )
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setWordWrap(True)

        self.select_button = QPushButton(
            "Select Payment Slip"
        )

        self.submit_button = QPushButton(
            "Submit Payment"
        )

        self.select_button.clicked.connect(
            self.select_file
        )

        self.submit_button.clicked.connect(
            self.submit_payment
        )

        layout.addWidget(title)
        layout.addWidget(subscription_details)
        layout.addWidget(self.status_label)

        layout.addWidget(self.bank_details)
        layout.addWidget(self.crypto_details)

        layout.addWidget(self.file_label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.submit_button)

        self.setCentralWidget(page)

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(
            self.check_payment_status
        )

        self.load_payment_settings()

    def load_payment_settings(self):

        data = PaymentAPI.get_payment_settings()

        if data is None:
            self.bank_details.setText(
                "Bank payment details unavailable."
            )

            self.crypto_details.setText(
                "Crypto payment details unavailable."
            )

            return

        self.bank_details.setText(
            "BANK PAYMENT\n"
            "------------------------------\n"
            f"Bank : {data['bank_name']}\n"
            f"Account Name : {data['account_name']}\n"
            f"Account Number : {data['account_number']}\n"
            f"Branch : {data['branch']}\n"
            f"Instructions : {data['bank_instructions']}"
        )

        self.crypto_details.setText(
            "CRYPTO PAYMENT\n"
            "------------------------------\n"
            f"Currency : {data['crypto_currency']}\n"
            f"Network : {data['crypto_network']}\n"
            f"Address : {data['crypto_address']}\n"
            f"Instructions : {data['crypto_instructions']}"
        )

    def select_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Payment Slip",
            "",
            "Payment Files (*.jpg *.jpeg *.png *.pdf)",
        )

        if not file_path:
            return

        self.selected_file = file_path

        self.file_label.setText(
            f"Selected:\n{file_path}"
        )

    def submit_payment(self):

        if not self.selected_file:
            QMessageBox.warning(
                self,
                "Payment Slip Required",
                "Please select your payment slip.",
            )
            return

        result = PaymentAPI.submit_payment(
            token=self.token,
            file_path=self.selected_file,
        )

        if result is None:
            QMessageBox.warning(
                self,
                "Payment Failed",
                "Payment submission failed.\n"
                "Please try again.",
            )
            return

        QMessageBox.information(
            self,
            "Payment Submitted",
            "Payment slip submitted successfully.\n"
            "Please wait for admin approval.",
        )

        self.payment_submitted = True

        self.status_label.setText(
            "Payment Status : Submitted - Waiting for Approval"
        )

        self.submit_button.setEnabled(False)
        self.select_button.setEnabled(False)

        self.refresh_timer.start(30000)

    def check_payment_status(self):

        if not self.payment_submitted:
            return

        subscription = PaymentAPI.get_my_subscription(
            self.token
        )

        if subscription is None:
            return

        status = str(
            subscription.get("status", "")
        ).upper()

        if status not in {"APPROVED", "ACTIVE"}:
            return

        self.refresh_timer.stop()

        self.status_label.setText(
            "Payment Status : APPROVED"
            if status == "APPROVED"
            else "Payment Status : ACTIVE"
        )

        self.open_dashboard()

    def open_dashboard(self):

        from client.ui.windows.dashboard_window import (
            DashboardWindow,
        )

        self.dashboard = DashboardWindow(
            self.token
        )

        self.dashboard.show()
        self.dashboard.raise_()
        self.dashboard.activateWindow()

        self.close()

    def closeEvent(self, event):

        self.refresh_timer.stop()

        event.accept()