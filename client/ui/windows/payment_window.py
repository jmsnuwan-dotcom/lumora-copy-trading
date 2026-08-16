from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QFrame,
    QScrollArea,
    QCheckBox,
)

from client.api.payment_api import PaymentAPI
from client.api.subscription_api import SubscriptionAPI


class PaymentWindow(QMainWindow):

    def __init__(
        self,
        token: str,
        package_name: str,
        plan_name: str,
        duration: str,
        final_price: str,
        remaining_payment: bool = False,
        is_trial: bool = False,
    ):
        super().__init__()

        self.token = token
        self.package_name = package_name
        self.plan_name = plan_name
        self.duration = duration
        self.final_price = final_price
        self.is_trial = is_trial
        self.remaining_payment = remaining_payment

        self.selected_file = None
        self.payment_submitted = False

        self.setWindowTitle(
            "Lumora AI Trading - Payment"
        )

        self.resize(950, 700)

        self.setMinimumSize(
            850,
            620,
        )

        self.init_ui()

        self.refresh_timer = QTimer(self)

        self.refresh_timer.timeout.connect(
            self.check_payment_status
        )

        self.load_payment_settings()

        self.check_existing_payment()

    def init_ui(self):

        page = QWidget()

        page.setObjectName(
            "paymentPage"
        )

        main_layout = QVBoxLayout(page)

        main_layout.setContentsMargins(
            35,
            30,
            35,
            30,
        )

        main_layout.setSpacing(
            18,
        )

        # ==========================================
        # HEADER
        # ==========================================

        title = QLabel(
            "Complete Your Payment"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setObjectName(
            "title"
        )

        subtitle = QLabel(
            "SECURE YOUR LUMORA AI TRADING PACKAGE"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        subtitle.setObjectName(
            "subtitle"
        )

        main_layout.addWidget(
            title
        )

        main_layout.addWidget(
            subtitle
        )

        # ==========================================
        # SUBSCRIPTION CARD
        # ==========================================

        subscription_card = QFrame()

        subscription_card.setObjectName(
            "infoCard"
        )

        subscription_layout = QVBoxLayout(
            subscription_card
        )

        subscription_layout.setContentsMargins(
            25,
            18,
            25,
            18,
        )

        subscription_title = QLabel(
            "YOUR PACKAGE"
        )

        if self.remaining_payment:

            remaining_notice = QLabel(
                "⚠ 24H TRIAL EXPIRED — REMAINING 50% PAYMENT REQUIRED"
            )

            remaining_notice.setAlignment(
                Qt.AlignCenter
            )

            remaining_notice.setObjectName(
                "remainingPaymentNotice"
            )

            subscription_layout.addWidget(
                remaining_notice
            )

        subscription_title.setObjectName(
            "sectionTitle"
        )

        subscription_title.setAlignment(
            Qt.AlignCenter
        )

        subscription_layout.addWidget(
            subscription_title
        )

        if self.remaining_payment or self.is_trial:

            try:
                original_price = float(self.final_price)
            except (TypeError, ValueError):
                original_price = 0.0

            half_price = original_price / 2

            if self.remaining_payment:

                subscription_text = (
                    f"Package: {self.package_name}\n"
                    f"Plan: {self.plan_name}\n"
                    f"Duration: {self.duration}\n"
                    f"Original Price: ${original_price:.2f}\n"
                    f"Trial Payment (50%): ${half_price:.2f}\n"
                    f"Remaining Payment (50%): ${half_price:.2f}"
                )

            else:

                subscription_text = (
                    f"Package: {self.package_name}\n"
                    f"Plan: {self.plan_name}\n"
                    f"Duration: {self.duration}\n"
                    f"Original Price: ${original_price:.2f}\n"
                    f"Trial Payment (50%): ${half_price:.2f}"
                )

        else:

            subscription_text = (
                f"Package: {self.package_name}\n"
                f"Plan: {self.plan_name}\n"
                f"Duration: {self.duration}\n"
                f"Final Price: ${self.final_price}"
            )

        self.subscription_details = QLabel(
            subscription_text
        )

        self.subscription_details.setAlignment(
            Qt.AlignCenter
        )

        self.subscription_details.setObjectName(
            "subscriptionDetails"
        )

        subscription_layout.addWidget(
            self.subscription_details
        )

        if self.remaining_payment:

            self.trial_checkbox = None

        else:

            self.trial_checkbox = QCheckBox(
                "24H Trial — Pay 50%"
            )

            self.trial_checkbox.setObjectName(
                "trialCheckbox"
            )

            self.trial_checkbox.stateChanged.connect(
                self.toggle_trial
            )

            subscription_layout.addWidget(
                self.trial_checkbox
            )

        main_layout.addWidget(
            subscription_card
        )

        # ==========================================
        # STATUS
        # ==========================================

        self.status_label = QLabel(
            "Payment Status : Checking..."
        )

        self.status_label.setAlignment(
            Qt.AlignCenter
        )

        self.status_label.setObjectName(
            "status"
        )

        main_layout.addWidget(
            self.status_label
        )

        # ==========================================
        # PAYMENT METHODS
        # ==========================================

        methods_layout = QHBoxLayout()

        methods_layout.setSpacing(
            18,
        )

        # ------------------------------------------
        # BANK
        # ------------------------------------------

        bank_card = QFrame()

        bank_card.setObjectName(
            "paymentCard"
        )

        bank_layout = QVBoxLayout(
            bank_card
        )

        bank_layout.setContentsMargins(
            22,
            20,
            22,
            20,
        )

        bank_title = QLabel(
            "BANK PAYMENT"
        )

        bank_title.setObjectName(
            "paymentTitle"
        )

        bank_layout.addWidget(
            bank_title
        )

        self.bank_details = QLabel(
            "Loading bank payment details..."
        )

        self.bank_details.setAlignment(
            Qt.AlignLeft
        )

        self.bank_details.setWordWrap(
            True
        )

        self.bank_details.setObjectName(
            "paymentDetails"
        )

        bank_layout.addWidget(
            self.bank_details
        )

        methods_layout.addWidget(
            bank_card
        )

        # ------------------------------------------
        # CRYPTO
        # ------------------------------------------

        crypto_card = QFrame()

        crypto_card.setObjectName(
            "paymentCard"
        )

        crypto_layout = QVBoxLayout(
            crypto_card
        )

        crypto_layout.setContentsMargins(
            22,
            20,
            22,
            20,
        )

        crypto_title = QLabel(
            "CRYPTO PAYMENT"
        )

        crypto_title.setObjectName(
            "paymentTitle"
        )

        crypto_layout.addWidget(
            crypto_title
        )

        self.crypto_details = QLabel(
            "Loading crypto payment details..."
        )

        self.crypto_details.setAlignment(
            Qt.AlignLeft
        )

        self.crypto_details.setWordWrap(
            True
        )

        self.crypto_details.setObjectName(
            "paymentDetails"
        )

        crypto_layout.addWidget(
            self.crypto_details
        )

        methods_layout.addWidget(
            crypto_card
        )

        main_layout.addLayout(
            methods_layout
        )

        # ==========================================
        # PAYMENT SLIP
        # ==========================================

        slip_card = QFrame()

        slip_card.setObjectName(
            "slipCard"
        )

        slip_layout = QVBoxLayout(
            slip_card
        )

        slip_layout.setContentsMargins(
            22,
            18,
            22,
            18,
        )

        slip_title = QLabel(
            "PAYMENT SLIP"
        )

        slip_title.setObjectName(
            "sectionTitle"
        )

        slip_title.setAlignment(
            Qt.AlignCenter
        )

        slip_layout.addWidget(
            slip_title
        )

        self.file_label = QLabel(
            "No payment slip selected."
        )

        self.file_label.setAlignment(
            Qt.AlignCenter
        )

        self.file_label.setWordWrap(
            True
        )

        self.file_label.setObjectName(
            "fileLabel"
        )

        slip_layout.addWidget(
            self.file_label
        )

        # ------------------------------------------
        # BUTTONS
        # ------------------------------------------

        buttons_layout = QHBoxLayout()

        buttons_layout.setSpacing(
            12,
        )

        self.select_button = QPushButton(
            "Select Payment Slip"
        )

        self.select_button.setObjectName(
            "secondaryButton"
        )

        self.select_button.setMinimumHeight(
            48
        )

        self.submit_button = QPushButton(
            "Submit Payment"
        )

        self.submit_button.setObjectName(
            "primaryButton"
        )

        self.submit_button.setMinimumHeight(
            48
        )

        buttons_layout.addWidget(
            self.select_button
        )

        buttons_layout.addWidget(
            self.submit_button
        )

        slip_layout.addLayout(
            buttons_layout
        )

        main_layout.addWidget(
            slip_card
        )

        # ==========================================
        # SIGNALS
        # ==========================================

        self.select_button.clicked.connect(
            self.select_file
        )

        self.submit_button.clicked.connect(
            self.submit_payment
        )

        # ==========================================
        # FULL PAGE SCROLL
        # ==========================================

        page_content = QWidget()
        page_content.setObjectName(
            "pageContent"
        )
        page_content.setLayout(
            main_layout
        )

        scroll = QScrollArea()
        scroll.setWidgetResizable(
            True
        )
        scroll.setFrameShape(
            QFrame.NoFrame
        )
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )
        scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )
        scroll.setWidget(
            page_content
        )

        # ==========================================
        # STYLE
        # ==========================================

        self.setCentralWidget(
            scroll
        )

        self.apply_style()

    def apply_style(self):

        self.setStyleSheet(
            """
            QMainWindow {
                background: #03040A;
            }

            QScrollArea {
                background: #03040A;
                border: none;
            }

            QScrollArea > QWidget {
                background: #03040A;
                border: none;
            }

            QScrollArea > QWidget > QWidget {
                background: #03040A;
                border: none;
            }

            QWidget#pageContent {
                background: #03040A;
                color: #FFFFFF;
            }

            QScrollBar:vertical {
                background: #070711;
                width: 10px;
                margin: 4px 0 4px 0;
                border: none;
            }

            QScrollBar::handle:vertical {
                background: #292943;
                border-radius: 5px;
                min-height: 40px;
            }

            QScrollBar::handle:vertical:hover {
                background: #713d9f;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                background: transparent;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }

            QLabel#title {
                color: #FFFFFF;
                font-size: 30px;
                font-weight: 700;
            }

            QLabel#subtitle {
                color: #A3A3B4;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 2px;
            }

            QFrame#infoCard,
            QFrame#paymentCard,
            QFrame#slipCard {
                background: #070913;
                border: 1px solid #29283B;
                border-radius: 16px;
            }

            QLabel#sectionTitle {
                color: #B8B8C8;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#subscriptionDetails {
                color: #FFFFFF;
                font-size: 14px;
                line-height: 1.5;
            }

            QLabel#status {
                color: #D2D2DF;
                background: #080A14;
                border: 1px solid #343047;
                border-radius: 10px;
                padding: 12px;
                font-size: 13px;
                font-weight: 600;
            }

            QLabel#paymentTitle {
                color: #FFFFFF;
                font-size: 16px;
                font-weight: 700;
                padding-bottom: 8px;
            }

            QLabel#paymentDetails {
                color: #C2C2D0;
                font-size: 12px;
                line-height: 1.5;
            }

            QLabel#fileLabel {
                color: #9999A9;
                background: #05060D;
                border: 1px dashed #39364F;
                border-radius: 10px;
                padding: 12px;
                min-height: 35px;
            }

            QPushButton#primaryButton {
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 700;
                border: none;
                border-radius: 10px;

                background: qlineargradient(
                    x1: 0,
                    y1: 0,
                    x2: 1,
                    y2: 0,
                    stop: 0 #079DF5,
                    stop: 0.5 #5858FF,
                    stop: 1 #D42CFF
                );
            }

            QPushButton#primaryButton:hover {
                background: qlineargradient(
                    x1: 0,
                    y1: 0,
                    x2: 1,
                    y2: 0,
                    stop: 0 #16B5FF,
                    stop: 0.5 #7474FF,
                    stop: 1 #E348FF
                );
            }

            QPushButton#secondaryButton {
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 600;
                background: #080A14;
                border: 1px solid #34324A;
                border-radius: 10px;
            }

            QPushButton#secondaryButton:hover {
                border: 1px solid #7B4CFF;
                background: #0D0B1C;
            }

            QPushButton#secondaryButton:disabled,
            QPushButton#primaryButton:disabled {
                color: #686878;
                background: #10111A;
                border: 1px solid #20202D;
            }
            """
        )

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
            "Bank : "
            f"{data['bank_name']}\n"
            "Account Name : "
            f"{data['account_name']}\n"
            "Account Number : "
            f"{data['account_number']}\n"
            "Branch : "
            f"{data['branch']}\n\n"
            "Instructions :\n"
            f"{data['bank_instructions']}"
        )

        self.crypto_details.setText(
            "Currency : "
            f"{data['crypto_currency']}\n"
            "Network : "
            f"{data['crypto_network']}\n"
            "Address : "
            f"{data['crypto_address']}\n\n"
            "Instructions :\n"
            f"{data['crypto_instructions']}"
        )

    def check_existing_payment(self):

        subscription = (
            SubscriptionAPI.get_my_subscription(
                self.token
            )
        )

        if subscription is None:

            self.set_waiting_state(
                submitted=False
            )

            return

        status = str(
            subscription.get(
                "status",
                "",
            )
        ).upper()

        payment_status = str(
            subscription.get(
                "payment_status",
                "",
            )
        ).upper()

        if payment_status == "SUBMITTED":

            self.set_waiting_state(
                submitted=True
            )

            return

        if status in {
            "APPROVED",
            "ACTIVE",
        }:

            self.open_dashboard()

            return

        self.set_waiting_state(
            submitted=False
        )

    def set_waiting_state(
        self,
        submitted: bool,
    ):

        self.payment_submitted = submitted

        if submitted:

            self.status_label.setText(
                "Payment Status : "
                "Submitted - "
                "Waiting for Approval"
            )

            self.select_button.setEnabled(
                False
            )

            self.submit_button.setEnabled(
                False
            )

            self.refresh_timer.start(
                30000
            )

        else:

            self.status_label.setText(
                "Payment Status : Not Submitted"
            )

            self.select_button.setEnabled(
                True
            )

            self.submit_button.setEnabled(
                True
            )

    def select_file(self):

        if self.payment_submitted:
            return

        file_path, _ = (
            QFileDialog.getOpenFileName(
                self,
                "Select Payment Slip",
                "",
                "Payment Files "
                "(*.jpg *.jpeg *.png *.pdf)",
            )
        )

        if not file_path:
            return

        self.selected_file = file_path

        self.file_label.setText(
            f"Selected:\n{file_path}"
        )

    def toggle_trial(self, state):
        self.is_trial = bool(state)

        print("TRIAL TOGGLE:", self.is_trial)

        try:
            price = float(self.final_price)
        except (TypeError, ValueError):
            return

        if self.is_trial:

            display_price = price / 2

            self.subscription_details.setText(
                f"Package: {self.package_name}\n"
                f"Plan: {self.plan_name}\n"
                f"Duration: {self.duration}\n"
                f"Original Price: ${price:.2f}\n"
                f"Trial Payment (50%): ${display_price:.2f}"
            )

        else:

            self.subscription_details.setText(
                f"Package: {self.package_name}\n"
                f"Plan: {self.plan_name}\n"
                f"Duration: {self.duration}\n"
                f"Final Price: ${price:.2f}"
            )

    def submit_payment(self):

        if self.payment_submitted:
            return

        if not self.selected_file:

            QMessageBox.warning(
                self,
                "Payment Slip Required",
                "Please select your payment slip.",
            )

            return

        # ==================================================
        # GET TRIAL STATE DIRECTLY FROM CHECKBOX
        # ==================================================

        if self.remaining_payment:

            trial_selected = False

        elif self.trial_checkbox is not None:

            trial_selected = (
                self.trial_checkbox.isChecked()
            )

        else:

            trial_selected = False

        print(
            "PAYMENT DEBUG:",
            "REMAINING_PAYMENT =",
            self.remaining_payment,
            "TRIAL_SELECTED =",
            trial_selected,
        )

        result = PaymentAPI.submit_payment(
            token=self.token,
            file_path=self.selected_file,
            is_trial=trial_selected,
        )

        if result is None:

            QMessageBox.warning(
                self,
                "Payment Failed",
                "Payment submission failed.\n"
                "Please try again.",
            )

            return

        self.set_waiting_state(
            submitted=True
        )

        QMessageBox.information(
            self,
            "Payment Submitted",
            "Payment slip submitted "
            "successfully.\n\n"
            "Please wait for admin approval.",
        )

    def check_payment_status(self):

        subscription = (
            SubscriptionAPI.get_my_subscription(
                self.token
            )
        )

        if subscription is None:
            return

        status = str(
            subscription.get(
                "status",
                "",
            )
        ).upper()

        payment_status = str(
            subscription.get(
                "payment_status",
                "",
            )
        ).upper()

        if (
            status in {
                "APPROVED",
                "ACTIVE",
            }
            or payment_status == "APPROVED"
        ):

            self.refresh_timer.stop()

            self.status_label.setText(
                "Payment Status : APPROVED"
            )

            self.open_dashboard()

    def open_dashboard(self):

        from client.ui.windows.dashboard_window import (
            DashboardWindow,
        )

        self.refresh_timer.stop()

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