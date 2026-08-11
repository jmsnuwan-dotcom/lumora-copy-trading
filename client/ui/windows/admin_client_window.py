from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QGroupBox,
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
            "Lumora - Client Management"
        )
        self.resize(750, 700)

        self.init_ui()
        self.load_clients()

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(
            self.load_clients
        )
        self.refresh_timer.start(30000)

    def init_ui(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setSpacing(10)

        self.status = QLabel(
            "Loading clients..."
        )

        self.client_layout = QVBoxLayout()
        self.client_layout.setSpacing(8)

        container = QWidget()
        container.setLayout(
            self.client_layout
        )

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)

        clients_box = QGroupBox(
            "Registered Clients"
        )

        clients_box_layout = QVBoxLayout(
            clients_box
        )

        clients_box_layout.addWidget(
            self.status
        )

        clients_box_layout.addWidget(
            scroll
        )

        layout.addWidget(
            clients_box
        )

        self.setCentralWidget(page)

    def load_clients(self):

        clients = AdminAPI.get_clients(
            self.token
        )

        while self.client_layout.count():

            item = self.client_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        if clients is None:

            self.status.setText(
                "Unable to load clients."
            )

            return

        self.status.setText(
            f"Clients : {len(clients)}"
        )

        for client in clients:

            self.add_client_row(
                client
            )

    def add_client_row(
        self,
        client: dict,
    ):

        row = QWidget()

        row_layout = QHBoxLayout(row)

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

        info = QLabel(
            f"#{user_id}  "
            f"{name}  |  "
            f"{email}  |  "
            f"{account_status}"
        )

        # ------------------------------------------
        # VIEW DETAILS
        # ------------------------------------------

        details_button = QPushButton(
            "VIEW DETAILS"
        )

        details_button.clicked.connect(
            lambda checked=False,
            data=client:
            self.show_client_details(data)
        )

        # ------------------------------------------
        # ACCOUNT ACTIVATE / DEACTIVATE
        # ------------------------------------------

        toggle_button = QPushButton(
            "Deactivate"
            if is_active
            else "Activate"
        )

        toggle_button.clicked.connect(
            lambda checked=False,
            uid=user_id:
            self.toggle_client(uid)
        )

        # ------------------------------------------
        # SUBSCRIPTION DATA
        # ------------------------------------------

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

        # ------------------------------------------
        # PACKAGE ACTIONS
        # ------------------------------------------

        activate_package_button = QPushButton(
            "Activate Package"
        )

        activate_package_button.clicked.connect(
            lambda checked=False,
            sid=subscription_id:
            self.activate_package(sid)
        )

        trial_button = QPushButton(
            "Give 24H Trial"
        )

        trial_button.clicked.connect(
            lambda checked=False,
            sid=subscription_id:
            self.give_trial(sid)
        )

        # ------------------------------------------
        # ADD BASIC BUTTONS
        # ------------------------------------------

        row_layout.addWidget(
            details_button
        )

        row_layout.addWidget(
            info
        )

        row_layout.addWidget(
            toggle_button
        )

        # ------------------------------------------
        # SHOW PACKAGE ACTIONS
        # ONLY AFTER PAYMENT APPROVAL
        # ------------------------------------------

        if (
            subscription_id is not None
            and subscription_status == "APPROVED"
            and payment_status == "APPROVED"
            and not is_trial
        ):

            row_layout.addWidget(
                activate_package_button
            )

            row_layout.addWidget(
                trial_button
            )

        self.client_layout.addWidget(
            row
        )

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

    def give_trial(
        self,
        subscription_id: int | None,
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


    def activate_package(
        self,
        subscription_id: int | None,
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

    def closeEvent(self, event):

        self.refresh_timer.stop()

        event.accept()

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

        QMessageBox.information(
            self,
            "Client Details",
            details,
        )