from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from client.api.admin_api import AdminAPI


class AdminPaymentWindow(QMainWindow):

    def __init__(self, token: str):
        super().__init__()

        self.token = token

        self.setWindowTitle(
            "Lumora - Admin Payment Management"
        )
        self.resize(750, 700)

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(12)

        # =====================================================
        # Payment Settings
        # =====================================================

        form = QFormLayout()

        self.bank_name = QLineEdit()
        self.account_name = QLineEdit()
        self.account_number = QLineEdit()
        self.branch = QLineEdit()
        self.bank_instructions = QTextEdit()

        self.crypto_currency = QLineEdit()
        self.crypto_network = QLineEdit()
        self.crypto_address = QLineEdit()
        self.crypto_instructions = QTextEdit()

        form.addRow(
            "Bank Name :",
            self.bank_name,
        )

        form.addRow(
            "Account Name :",
            self.account_name,
        )

        form.addRow(
            "Account Number :",
            self.account_number,
        )

        form.addRow(
            "Branch :",
            self.branch,
        )

        form.addRow(
            "Bank Instructions :",
            self.bank_instructions,
        )

        form.addRow(
            "Crypto Currency :",
            self.crypto_currency,
        )

        form.addRow(
            "Crypto Network :",
            self.crypto_network,
        )

        form.addRow(
            "Crypto Address :",
            self.crypto_address,
        )

        form.addRow(
            "Crypto Instructions :",
            self.crypto_instructions,
        )

        self.save_button = QPushButton(
            "Save Payment Settings"
        )

        self.save_button.clicked.connect(
            self.save_settings
        )

        settings_box = QGroupBox(
            "Payment Details"
        )

        settings_layout = QVBoxLayout(
            settings_box
        )

        settings_layout.addLayout(form)

        settings_layout.addWidget(
            self.save_button
        )

        # =====================================================
        # Pending Payments
        # =====================================================

        self.pending_status = QLabel(
            "Loading pending payments..."
        )

        self.pending_layout = QVBoxLayout()
        self.pending_layout.setSpacing(8)

        pending_box = QGroupBox(
            "Client Payments Awaiting Approval"
        )

        pending_box_layout = QVBoxLayout(
            pending_box
        )

        pending_box_layout.addWidget(
            self.pending_status
        )

        pending_box_layout.addLayout(
            self.pending_layout
        )

        # =====================================================
        # Main Layout
        # =====================================================

        layout.addWidget(
            settings_box
        )

        layout.addWidget(
            pending_box
        )

        self.setCentralWidget(page)

        # =====================================================
        # Initial Load
        # =====================================================

        self.load_settings()
        self.load_pending_payments()

        # =====================================================
        # Refresh Pending Payments
        # =====================================================

        self.refresh_timer = QTimer(self)

        self.refresh_timer.timeout.connect(
            self.load_pending_payments
        )

        self.refresh_timer.start(30000)

    # =========================================================
    # Payment Settings
    # =========================================================

    def load_settings(self):

        data = AdminAPI.get_payment_settings(
            self.token
        )

        if data is None:

            QMessageBox.warning(
                self,
                "Error",
                "Unable to load payment settings.",
            )

            return

        self.bank_name.setText(
            data["bank_name"]
        )

        self.account_name.setText(
            data["account_name"]
        )

        self.account_number.setText(
            data["account_number"]
        )

        self.branch.setText(
            data["branch"]
        )

        self.bank_instructions.setPlainText(
            data["bank_instructions"]
        )

        self.crypto_currency.setText(
            data["crypto_currency"]
        )

        self.crypto_network.setText(
            data["crypto_network"]
        )

        self.crypto_address.setText(
            data["crypto_address"]
        )

        self.crypto_instructions.setPlainText(
            data["crypto_instructions"]
        )

    def save_settings(self):

        data = {
            "bank_name":
                self.bank_name.text().strip(),

            "account_name":
                self.account_name.text().strip(),

            "account_number":
                self.account_number.text().strip(),

            "branch":
                self.branch.text().strip(),

            "bank_instructions":
                self.bank_instructions
                .toPlainText()
                .strip(),

            "crypto_currency":
                self.crypto_currency
                .text()
                .strip(),

            "crypto_network":
                self.crypto_network
                .text()
                .strip(),

            "crypto_address":
                self.crypto_address
                .text()
                .strip(),

            "crypto_instructions":
                self.crypto_instructions
                .toPlainText()
                .strip(),
        }

        result = AdminAPI.update_payment_settings(
            token=self.token,
            data=data,
        )

        if result is None:

            QMessageBox.warning(
                self,
                "Update Failed",
                "Payment settings update failed.",
            )

            return

        QMessageBox.information(
            self,
            "Success",
            "Payment settings updated successfully.",
        )

    # =========================================================
    # Pending Payments
    # =========================================================

    def load_pending_payments(self):

        payments = AdminAPI.get_pending_payments(
            self.token
        )

        self.clear_pending_layout()

        if payments is None:

            self.pending_status.setText(
                "Unable to load pending payments."
            )

            return

        if not payments:

            self.pending_status.setText(
                "No pending payments."
            )

            return

        self.pending_status.setText(
            f"{len(payments)} pending payment(s)"
        )

        for payment in payments:

            self.add_pending_payment(
                payment
            )

    def clear_pending_layout(self):

        while self.pending_layout.count():

            item = self.pending_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def add_pending_payment(
        self,
        payment: dict,
    ):

        row = QWidget()

        row_layout = QVBoxLayout(row)
        row_layout.setSpacing(6)

        name_button = QPushButton(
            f"> {payment['full_name']}"
        )

        details = QWidget()
        details.hide()

        details_layout = QVBoxLayout(
            details
        )

        details_layout.addWidget(
            QLabel(
                f"Email : {payment['email']}"
            )
        )

        details_layout.addWidget(
            QLabel(
                f"Phone : {payment['phone_number']}"
            )
        )

        details_layout.addWidget(
            QLabel(
                f"Package : {payment['package']}"
            )
        )

        details_layout.addWidget(
            QLabel(
                f"Plan : {payment['plan']}"
            )
        )

        details_layout.addWidget(
            QLabel(
                f"Amount : {payment['amount']}"
            )
        )

        details_layout.addWidget(
            QLabel(
                f"Payment Status : "
                f"{payment['payment_status']}"
            )
        )

        details_layout.addWidget(
            QLabel(
                f"Submitted At : "
                f"{payment['payment_submitted_at']}"
            )
        )

        slip_label = QLabel(
            f"Payment Slip : "
            f"{payment['payment_slip']}"
        )

        slip_label.setWordWrap(True)

        details_layout.addWidget(
            slip_label
        )

        view_slip_button = QPushButton(
            "VIEW PAYMENT SLIP"
        )

        view_slip_button.clicked.connect(
            lambda checked=False,
            subscription_id=payment["id"]:
                self.view_payment_slip(
                    subscription_id
                )
        )

        details_layout.addWidget(
            view_slip_button
        )

        accept_button = QPushButton(
            "ACCEPT"
        )

        accept_button.clicked.connect(
            lambda checked=False,
            subscription_id=payment["id"]:
                self.accept_payment(
                    subscription_id
                )
        )

        details_layout.addWidget(
            accept_button
        )

        def toggle_details():

            visible = details.isVisible()

            details.setVisible(
                not visible
            )

            if visible:

                name_button.setText(
                    f"> {payment['full_name']}"
                )

            else:

                name_button.setText(
                    f"v {payment['full_name']}"
                )

        name_button.clicked.connect(
            toggle_details
        )

        row_layout.addWidget(
            name_button
        )

        row_layout.addWidget(
            details
        )

        self.pending_layout.addWidget(
            row
        )

    def view_payment_slip(
        self,
        subscription_id: int,
    ):

        file_data = AdminAPI.get_payment_slip(
            token=self.token,
            subscription_id=subscription_id,
        )

        if file_data is None:

            QMessageBox.warning(
                self,
                "Payment Slip",
                "Unable to load payment slip.",
            )

            return

        payment = next(
            (
                item
                for item in (
                    AdminAPI.get_pending_payments(
                        self.token
                    ) or []
                )
                if item.get("id")
                == subscription_id
            ),
            None,
        )

        if payment is None:

            QMessageBox.warning(
                self,
                "Payment Slip",
                "Payment information not found.",
            )

            return

        payment_slip = payment.get(
            "payment_slip"
        )

        if not payment_slip:

            QMessageBox.warning(
                self,
                "Payment Slip",
                "Payment slip file not found.",
            )

            return

        from pathlib import Path
        import os
        import tempfile

        extension = Path(
            payment_slip
        ).suffix.lower()

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension,
        )

        try:
            temp_file.write(file_data)
            temp_file.close()

            os.startfile(
                temp_file.name
            )

        except Exception as e:

            temp_file.close()

            try:
                os.unlink(
                    temp_file.name
                )
            except OSError:
                pass

            QMessageBox.warning(
                self,
                "Payment Slip",
                f"Unable to open payment slip.\n\n{e}",
            )

    def accept_payment(
        self,
        subscription_id: int,
    ):

        result = AdminAPI.approve_payment(
            token=self.token,
            subscription_id=subscription_id,
        )

        if result is None:

            QMessageBox.warning(
                self,
                "Approval Failed",
                "Payment approval failed.",
            )

            return

        QMessageBox.information(
            self,
            "Payment Approved",
            "Payment approved successfully.",
        )

        self.load_pending_payments()

    # =========================================================
    # Close
    # =========================================================

    def closeEvent(self, event):

        self.refresh_timer.stop()

        event.accept()