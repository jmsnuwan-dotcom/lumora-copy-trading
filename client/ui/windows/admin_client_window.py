from typing import Optional

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from client.api.admin_api import AdminAPI


class AdminClientWindow(QMainWindow):

    def __init__(self, token: str):
        super().__init__()

        self.token = token

        self.setWindowTitle(
            "Lumora AI Trading - Client Management"
        )

        self.resize(1150, 760)

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

            QPushButton {
                background: #0a0a14;
                border: 1px solid #30304a;
                border-radius: 8px;
                padding: 9px 14px;
                color: white;
                font-weight: 600;
            }

            QPushButton:hover {
                background: #121223;
                border: 1px solid #9b4dff;
            }

            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollBar:vertical {
                background: #070711;
                width: 10px;
                margin: 4px;
            }

            QScrollBar::handle:vertical {
                background: #292943;
                border-radius: 5px;
                min-height: 40px;
            }

            QScrollBar::handle:vertical:hover {
                background: #713d9f;
            }
            """
        )

        self.init_ui()
        self.load_clients()

        self.refresh_timer = QTimer(self)

        self.refresh_timer.timeout.connect(
            self.load_clients
        )

        self.refresh_timer.start(60000)

    # ==========================================================
    # UI
    # ==========================================================

    def init_ui(self):

        page = QWidget()

        layout = QVBoxLayout(page)

        layout.setContentsMargins(
            28,
            24,
            28,
            24,
        )

        layout.setSpacing(18)

        # ======================================================
        # HEADER
        # ======================================================

        header_layout = QHBoxLayout()

        title_box = QVBoxLayout()

        title = QLabel(
            "Client Management"
        )

        title.setStyleSheet(
            """
            QLabel {
                font-size: 28px;
                font-weight: 800;
                color: white;
            }
            """
        )

        subtitle = QLabel(
            "Manage Lumora AI Trading client accounts and packages."
        )

        subtitle.setStyleSheet(
            """
            QLabel {
                color: #8888a0;
                font-size: 13px;
            }
            """
        )

        title_box.addWidget(
            title
        )

        title_box.addWidget(
            subtitle
        )

        header_layout.addLayout(
            title_box
        )

        header_layout.addStretch()

        self.status = QLabel(
            "● Loading clients..."
        )

        self.status.setAlignment(
            Qt.AlignCenter
        )

        self.status.setMinimumWidth(
            180
        )

        self.status.setMinimumHeight(
            40
        )

        self.status.setStyleSheet(
            """
            QLabel {
                background: #11101b;
                border: 1px solid #36304b;
                border-radius: 10px;
                color: #b967ff;
                font-weight: 700;
                padding: 6px 14px;
            }
            """
        )

        header_layout.addWidget(
            self.status
        )

        layout.addLayout(
            header_layout
        )

        # ======================================================
        # CLIENT LIST PANEL
        # ======================================================

        clients_panel = QFrame()

        clients_panel.setStyleSheet(
            """
            QFrame {
                background: #080811;
                border: 1px solid #28283f;
                border-radius: 14px;
            }
            """
        )

        clients_panel_layout = QVBoxLayout(
            clients_panel
        )

        clients_panel_layout.setContentsMargins(
            18,
            18,
            18,
            18,
        )

        clients_panel_layout.setSpacing(
            10
        )

        clients_title = QLabel(
            "REGISTERED CLIENTS"
        )

        clients_title.setStyleSheet(
            """
            QLabel {
                color: #b967ff;
                font-size: 12px;
                font-weight: 800;
                letter-spacing: 2px;
                border: none;
            }
            """
        )

        clients_panel_layout.addWidget(
            clients_title
        )

        # ------------------------------------------------------
        # CLIENT LIST
        # ------------------------------------------------------

        self.client_layout = QVBoxLayout()

        self.client_layout.setSpacing(
            10
        )

        self.client_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        clients_panel_layout.addLayout(
            self.client_layout
        )

        layout.addWidget(
            clients_panel
        )

        # ======================================================
        # FULL PAGE SCROLL
        # ======================================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        scroll.setFrameShape(
            QFrame.NoFrame
        )

        scroll.setStyleSheet(
            """
            QScrollArea {
                background: #05050d;
                border: none;
            }

            QScrollArea > QWidget {
                background: #05050d;
            }

            QScrollArea > QWidget > QWidget {
                background: #05050d;
            }

            QScrollBar:vertical {
                background: #070711;
                width: 10px;
                margin: 0px;
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
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
            """
        )

        scroll.setWidget(
            page
        )

        self.setCentralWidget(
            scroll
        )

    # ==========================================================
    # LOAD CLIENTS
    # ==========================================================

    def load_clients(self):

        clients = AdminAPI.get_clients(
            self.token
        )

        while self.client_layout.count():

            item = self.client_layout.takeAt(
                0
            )

            widget = item.widget()

            if widget:
                widget.deleteLater()

        if clients is None:

            self.status.setText(
                "● Unable to load clients"
            )

            self.status.setStyleSheet(
                """
                QLabel {
                    background: #210912;
                    border: 1px solid #9b2447;
                    border-radius: 10px;
                    color: #ff5578;
                    font-weight: 700;
                    padding: 6px 14px;
                }
                """
            )

            return

        self.status.setText(
            f"● {len(clients)} CLIENTS"
        )

        self.status.setStyleSheet(
            """
            QLabel {
                background: #061711;
                border: 1px solid #087a55;
                border-radius: 10px;
                color: #00e69a;
                font-weight: 700;
                padding: 6px 14px;
            }
            """
        )

        if not clients:

            empty = QLabel(
                "No registered clients found."
            )

            empty.setAlignment(
                Qt.AlignCenter
            )

            empty.setMinimumHeight(
                120
            )

            empty.setStyleSheet(
                """
                QLabel {
                    color: #777790;
                    border: none;
                }
                """
            )

            self.client_layout.addWidget(
                empty
            )

            return

        for client in clients:

            self.add_client_row(
                client
            )

        self.client_layout.addStretch()

    # ==========================================================
    # CLIENT ROW
    # ==========================================================

    def add_client_row(
        self,
        client: dict,
    ):

        row = QWidget()

        row.setMinimumHeight(
            82
        )

        row.setStyleSheet(
            """
            QWidget {
                background: #0a0a14;
                border: 1px solid #27273e;
                border-radius: 11px;
            }

            QWidget:hover {
                border: 1px solid #4b3865;
            }
            """
        )

        row_layout = QHBoxLayout(
            row
        )

        row_layout.setContentsMargins(
            14,
            10,
            14,
            10,
        )

        row_layout.setSpacing(
            10
        )

        name = client.get(
            "full_name",
            client.get(
                "name",
                "Unknown",
            ),
        )

        email = client.get(
            "email",
            "-",
        )

        user_id = client.get(
            "id",
            client.get(
                "user_id",
                "-",
            ),
        )

        is_active = client.get(
            "is_active",
            False,
        )

        account_status = (
            "ACTIVE"
            if is_active
            else "DEACTIVATED"
        )

        # ======================================================
        # CLIENT INFO
        # ======================================================

        info_box = QVBoxLayout()

        info_box.setSpacing(
            4
        )

        name_label = QLabel(
            str(name)
        )

        name_label.setStyleSheet(
            """
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: 700;
                border: none;
            }
            """
        )

        email_label = QLabel(
            f"{email}   •   Client #{user_id}"
        )

        email_label.setStyleSheet(
            """
            QLabel {
                color: #777790;
                font-size: 11px;
                border: none;
            }
            """
        )

        info_box.addWidget(
            name_label
        )

        email_status_layout = QHBoxLayout()

        email_status_layout.setSpacing(
            10
        )

        email_status_layout.addWidget(
            email_label
        )

        status_label = QLabel(
            account_status
        )

        status_label.setAlignment(
            Qt.AlignCenter
        )

        status_label.setMinimumWidth(
            90
        )

        if is_active:

            status_label.setStyleSheet(
                """
                QLabel {
                    background: #063d28;
                    border: 1px solid #008f61;
                    border-radius: 6px;
                    color: #00e69a;
                    font-size: 9px;
                    font-weight: 800;
                    padding: 4px 8px;
                    border: none;
                }
                """
            )

        else:

            status_label.setStyleSheet(
                """
                QLabel {
                    background: #35101a;
                    border: 1px solid #9b2447;
                    border-radius: 6px;
                    color: #ff5578;
                    font-size: 9px;
                    font-weight: 800;
                    padding: 4px 8px;
                    border: none;
                }
                """
            )

        email_status_layout.addWidget(
            status_label
        )

        email_status_layout.addStretch()

        info_box.addLayout(
            email_status_layout
        )

        row_layout.addLayout(
            info_box,
            1,
        )

        # ======================================================
        # SUBSCRIPTION DATA
        # ======================================================

        subscription_id = client.get(
            "subscription_id"
        )

        subscription_status = str(
            client.get(
                "status",
                "",
            )
        ).upper()

        payment_status = str(
            client.get(
                "payment_status",
                "",
            )
        ).upper()

        is_trial = bool(
            client.get(
                "is_trial",
                False,
            )
        )

        # ======================================================
        # ACTIONS
        # ======================================================

        details_button = self.create_action_button(
            "VIEW DETAILS"
        )

        details_button.clicked.connect(
            lambda checked=False,
            data=client:
            self.show_client_details(
                data
            )
        )

        toggle_button = self.create_action_button(
            "Deactivate"
            if is_active
            else "Activate"
        )

        if is_active:

            toggle_button.setStyleSheet(
                """
                QPushButton {
                    background: #35101a;
                    border: 1px solid #9b2447;
                    border-radius: 8px;
                    color: #ff5578;
                    padding: 8px 12px;
                    font-weight: 700;
                }

                QPushButton:hover {
                    background: #501321;
                }
                """
            )

        else:

            toggle_button.setStyleSheet(
                """
                QPushButton {
                    background: #063d28;
                    border: 1px solid #008f61;
                    border-radius: 8px;
                    color: #00e69a;
                    padding: 8px 12px;
                    font-weight: 700;
                }

                QPushButton:hover {
                    background: #075b3a;
                }
                """
            )

        toggle_button.clicked.connect(
            lambda checked=False,
            uid=user_id:
            self.toggle_client(
                uid
            )
        )

        row_layout.addWidget(
            details_button
        )

        row_layout.addWidget(
            toggle_button
        )

        # ======================================================
        # PACKAGE ACTIONS
        # ======================================================

        if (
            subscription_id is not None
            and subscription_status == "APPROVED"
            and payment_status == "APPROVED"
            and not is_trial
        ):

            activate_package_button = (
                self.create_action_button(
                    "ACTIVATE PACKAGE"
                )
            )

            activate_package_button.setStyleSheet(
                """
                QPushButton {
                    background: #101a3a;
                    border: 1px solid #3d78ff;
                    border-radius: 8px;
                    color: #67a1ff;
                    padding: 8px 12px;
                    font-weight: 700;
                }

                QPushButton:hover {
                    background: #172754;
                }
                """
            )

            activate_package_button.clicked.connect(
                lambda checked=False,
                sid=subscription_id:
                self.activate_package(
                    sid
                )
            )

            trial_button = (
                self.create_action_button(
                    "GIVE 24H TRIAL"
                )
            )

            trial_button.setStyleSheet(
                """
                QPushButton {
                    background: #171126;
                    border: 1px solid #9b4dff;
                    border-radius: 8px;
                    color: #c878ff;
                    padding: 8px 12px;
                    font-weight: 700;
                }

                QPushButton:hover {
                    background: #24183a;
                }
                """
            )

            trial_button.clicked.connect(
                lambda checked=False,
                sid=subscription_id:
                self.give_trial(
                    sid
                )
            )

            row_layout.addWidget(
                activate_package_button
            )

            row_layout.addWidget(
                trial_button
            )

        self.client_layout.addWidget(
            row
        )

    # ==========================================================
    # BUTTON HELPER
    # ==========================================================

    @staticmethod
    def create_action_button(
        text: str,
    ):

        button = QPushButton(
            text
        )

        button.setMinimumHeight(
            36
        )

        button.setStyleSheet(
            """
            QPushButton {
                background: #0d0d19;
                border: 1px solid #30304a;
                border-radius: 8px;
                color: #e5e5ee;
                padding: 8px 12px;
                font-size: 10px;
                font-weight: 700;
            }

            QPushButton:hover {
                background: #17152a;
                border: 1px solid #9b4dff;
                color: white;
            }
            """
        )

        return button

    # ==========================================================
    # ACCOUNT TOGGLE
    # ==========================================================

    def toggle_client(
        self,
        user_id: int,
    ):

        result = AdminAPI.toggle_client_active(
            token=self.token,
            user_id=user_id,
        )

        if result is None:

            QMessageBox.warning(
                self,
                "Update Failed",
                "Client status could not be updated.",
            )

            return

        QMessageBox.information(
            self,
            "Client Updated",
            "Client status updated successfully.",
        )

        self.load_clients()

    # ==========================================================
    # TRIAL
    # ==========================================================

    def give_trial(
        self,
        subscription_id: Optional[int],
    ):

        if subscription_id is None:

            QMessageBox.warning(
                self,
                "Trial Failed",
                "Subscription not found.",
            )

            return

        result = AdminAPI.give_trial(
            token=self.token,
            subscription_id=subscription_id,
        )

        if result is None:

            QMessageBox.warning(
                self,
                "Trial Failed",
                "24H trial could not be activated.",
            )

            return

        QMessageBox.information(
            self,
            "Trial Activated",
            "24H trial activated successfully.",
        )

        self.load_clients()

    # ==========================================================
    # ACTIVATE PACKAGE
    # ==========================================================

    def activate_package(
        self,
        subscription_id: Optional[int],
    ):

        if subscription_id is None:

            QMessageBox.warning(
                self,
                "Activation Failed",
                "Subscription not found.",
            )

            return

        result = AdminAPI.activate_package(
            token=self.token,
            subscription_id=subscription_id,
        )

        if result is None:

            QMessageBox.warning(
                self,
                "Activation Failed",
                "Package could not be activated.",
            )

            return

        QMessageBox.information(
            self,
            "Package Activated",
            "Package activated successfully.",
        )

        self.load_clients()

    # ==========================================================
    # CLIENT DETAILS
    # ==========================================================

    def show_client_details(
        self,
        client: dict,
    ):

        details = (
            f"Full Name : "
            f"{client.get('full_name', '-')}\n\n"

            f"Email : "
            f"{client.get('email', '-')}\n\n"

            f"Phone : "
            f"{client.get('phone_number') or '-'}\n\n"

            f"Account Status : "
            f"{client.get('status', '-')}\n\n"

            f"Active : "
            f"{'YES' if client.get('is_active') else 'NO'}\n\n"

            f"Package : "
            f"{client.get('package') or '-'}\n\n"

            f"Plan : "
            f"{client.get('plan') or '-'}\n\n"

            f"Payment Status : "
            f"{client.get('payment_status') or '-'}\n\n"

            f"Trial : "
            f"{'YES' if client.get('is_trial') else 'NO'}\n\n"

            f"Trial Ends : "
            f"{client.get('trial_ends_at') or '-'}\n\n"

            f"Start Date : "
            f"{client.get('start_date') or '-'}\n\n"

            f"Expire Date : "
            f"{client.get('end_date') or '-'}"
        )

        message_box = QMessageBox(self)

        message_box.setWindowTitle("Client Details")
        message_box.setIcon(QMessageBox.Information)
        message_box.setText(details)

        message_box.setStandardButtons(
            QMessageBox.Ok
        )

        message_box.setStyleSheet("""
            QMessageBox {
                background-color: #070711;
                color: #F5F5F7;
                border: 1px solid #28283D;
            }

            QMessageBox QLabel {
                color: #E8E8F0;
                font-size: 13px;
                background-color: transparent;
            }

            QMessageBox QPushButton {
                background-color: #080814;
                color: #FFFFFF;
                border: 1px solid #00D9FF;
                border-radius: 8px;
                padding: 8px 22px;
                min-width: 55px;
                font-weight: bold;
            }

            QMessageBox QPushButton:hover {
                background-color: #17172A;
                border: 1px solid #B83CFF;
            }

            QMessageBox QPushButton:pressed {
                background-color: #24243A;
            }
        """)

        message_box.exec()

    # ==========================================================
    # CLOSE
    # ==========================================================

    def closeEvent(self, event):

        self.refresh_timer.stop()

        event.accept()