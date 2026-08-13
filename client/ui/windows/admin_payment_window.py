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
            "Lumora AI Trading - Payment Management"
        )
        self.resize(1100, 760)

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
            "Payment Management"
        )
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Manage payment settings and approve client payments."
        )
        subtitle.setObjectName("subtitle")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        layout.addWidget(header)

        # =====================================================
        # PAYMENT SETTINGS
        # =====================================================

        settings_box = QGroupBox(
            "PAYMENT SETTINGS"
        )
        settings_box.setObjectName(
            "sectionBox"
        )

        settings_layout = QVBoxLayout(
            settings_box
        )
        settings_layout.setContentsMargins(
            20, 22, 20, 20
        )
        settings_layout.setSpacing(14)

        form = QFormLayout()
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(12)

        self.bank_name = QLineEdit()
        self.account_name = QLineEdit()
        self.account_number = QLineEdit()
        self.branch = QLineEdit()
        self.bank_instructions = QTextEdit()

        self.crypto_currency = QLineEdit()
        self.crypto_network = QLineEdit()
        self.crypto_address = QLineEdit()
        self.crypto_instructions = QTextEdit()

        self.bank_instructions.setFixedHeight(80)
        self.crypto_instructions.setFixedHeight(80)

        form.addRow(
            "Bank Name",
            self.bank_name,
        )

        form.addRow(
            "Account Name",
            self.account_name,
        )

        form.addRow(
            "Account Number",
            self.account_number,
        )

        form.addRow(
            "Branch",
            self.branch,
        )

        form.addRow(
            "Bank Instructions",
            self.bank_instructions,
        )

        form.addRow(
            "Crypto Currency",
            self.crypto_currency,
        )

        form.addRow(
            "Crypto Network",
            self.crypto_network,
        )

        form.addRow(
            "Crypto Address",
            self.crypto_address,
        )

        form.addRow(
            "Crypto Instructions",
            self.crypto_instructions,
        )

        settings_layout.addLayout(form)

        self.save_button = QPushButton(
            "Save Payment Settings"
        )
        self.save_button.setObjectName(
            "primaryButton"
        )

        self.save_button.clicked.connect(
            self.save_settings
        )

        settings_layout.addWidget(
            self.save_button
        )

        layout.addWidget(
            settings_box
        )

        # =====================================================
        # PENDING PAYMENTS
        # =====================================================

        pending_box = QGroupBox(
            "PENDING PAYMENTS"
        )
        pending_box.setObjectName(
            "sectionBox"
        )

        pending_box_layout = QVBoxLayout(
            pending_box
        )
        pending_box_layout.setContentsMargins(
            20, 22, 20, 20
        )
        pending_box_layout.setSpacing(12)

        self.pending_status = QLabel(
            "Loading pending payments..."
        )
        self.pending_status.setObjectName(
            "statusLabel"
        )

        self.pending_layout = QVBoxLayout()
        self.pending_layout.setSpacing(10)

        pending_box_layout.addWidget(
            self.pending_status
        )

        pending_box_layout.addLayout(
            self.pending_layout
        )

        layout.addWidget(
            pending_box
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
                padding: 5px 0;
            }

            QLineEdit,
            QTextEdit {
                background: #07070f;
                border: 1px solid #2b2b42;
                border-radius: 9px;
                padding: 10px 12px;
                color: #ffffff;
                selection-background-color: #7b3cff;
            }

            QLineEdit:focus,
            QTextEdit:focus {
                border: 1px solid #9b3cff;
            }

            QLabel {
                color: #dddded;
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
            }

            QPushButton:hover {
                border: 1px solid #8b3dff;
                background: #121222;
            }

            QPushButton:pressed {
                background: #1b1730;
            }

            QPushButton#primaryButton {
                background: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 1, y2: 0,
                    stop: 0 #0799e8,
                    stop: 0.5 #4d66ff,
                    stop: 1 #d11cff
                );
                border: none;
                min-height: 42px;
                font-size: 14px;
            }

            QPushButton#primaryButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 1, y2: 0,
                    stop: 0 #16a9f5,
                    stop: 0.5 #6278ff,
                    stop: 1 #df35ff
                );
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

        # =====================================================
        # INITIAL LOAD
        # =====================================================

        self.load_settings()
        self.load_pending_payments()

        # =====================================================
        # AUTO REFRESH
        # =====================================================

        self.refresh_timer = QTimer(self)

        self.refresh_timer.timeout.connect(
            self.load_pending_payments
        )

        self.refresh_timer.start(30000)

    # =========================================================
    # PAYMENT SETTINGS
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
    # PENDING PAYMENTS
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
                "• 0 PENDING PAYMENTS"
            )

            return

        self.pending_status.setText(
            f"• {len(payments)} PENDING PAYMENT(S)"
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

        row = QGroupBox()
        row.setObjectName(
            "paymentCard"
        )

        row.setStyleSheet(
            """
            QGroupBox#paymentCard {
                background: #07070f;
                border: 1px solid #29293f;
                border-radius: 12px;
            }

            QGroupBox#paymentCard:hover {
                border: 1px solid #713cff;
            }
            """
        )

        row_layout = QVBoxLayout(row)
        row_layout.setContentsMargins(
            16, 14, 16, 14
        )
        row_layout.setSpacing(8)

        name_button = QPushButton(
            f"›  {payment['full_name']}"
        )

        name_button.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
                text-align: left;
                padding: 5px;
                color: #ffffff;
                font-size: 15px;
                font-weight: 700;
            }

            QPushButton:hover {
                color: #bd4cff;
            }
            """
        )

        details = QWidget()
        details.hide()

        details_layout = QVBoxLayout(
            details
        )
        details_layout.setContentsMargins(
            10, 8, 10, 5
        )
        details_layout.setSpacing(6)

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

        view_slip_button.setStyleSheet(
            """
            QPushButton {
                border: 1px solid #00d9ff;
                color: #00d9ff;
                min-height: 34px;
            }

            QPushButton:hover {
                background: #09202a;
            }
            """
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
            "ACCEPT PAYMENT"
        )

        accept_button.setStyleSheet(
            """
            QPushButton {
                background: #063b2c;
                border: 1px solid #00d9a0;
                color: #00e6a8;
                min-height: 38px;
            }

            QPushButton:hover {
                background: #07563f;
            }
            """
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
                    f"›  {payment['full_name']}"
                )

            else:

                name_button.setText(
                    f"⌄  {payment['full_name']}"
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

    # =========================================================
    # VIEW PAYMENT SLIP
    # =========================================================

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

    # =========================================================
    # ACCEPT PAYMENT
    # =========================================================

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
    # CLOSE
    # =========================================================

    def closeEvent(self, event):

        self.refresh_timer.stop()

        event.accept()