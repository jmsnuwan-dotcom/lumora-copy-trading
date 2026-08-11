from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from client.api.package_api import PackageAPI
from client.api.subscription_api import SubscriptionAPI
from client.ui.windows.payment_window import PaymentWindow


class PackageSelectionWindow(QMainWindow):

    def __init__(self, token: str):
        super().__init__()

        self.token = token

        self.setWindowTitle(
            "Lumora - Select Package"
        )
        self.resize(500, 500)

        page = QWidget()
        layout = QVBoxLayout(page)

        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)

        title = QLabel(
            "Select Your Package"
        )
        title.setAlignment(Qt.AlignCenter)

        self.package = QComboBox()
        self.plan = QComboBox()

        self.selection_label = QLabel(
            "Select a package and plan."
        )
        self.selection_label.setAlignment(
            Qt.AlignCenter
        )
        self.selection_label.setWordWrap(True)

        self.continue_button = QPushButton(
            "Continue to Payment"
        )

        self.package.currentIndexChanged.connect(
            self.load_plans
        )

        self.plan.currentIndexChanged.connect(
            self.update_selection
        )

        self.continue_button.clicked.connect(
            self.create_subscription
        )

        layout.addWidget(title)
        layout.addWidget(self.package)
        layout.addWidget(self.plan)
        layout.addWidget(
            self.selection_label
        )
        layout.addWidget(
            self.continue_button
        )

        self.setCentralWidget(page)

        self.load_packages()

    def load_packages(self):

        self.package.blockSignals(True)
        self.package.clear()

        packages = PackageAPI.get_packages()

        if packages is None:

            self.package.blockSignals(False)

            self.selection_label.setText(
                "Unable to load packages."
            )

            return

        for package in packages:

            if not package.get(
                "is_active",
                False,
            ):
                continue

            self.package.addItem(
                package["name"],
                package["id"],
            )

        self.package.blockSignals(False)

        self.load_plans()

    def load_plans(self):

        self.plan.blockSignals(True)
        self.plan.clear()

        package_id = (
            self.package.currentData()
        )

        if package_id is None:

            self.plan.blockSignals(False)

            self.update_selection()

            return

        plans = PackageAPI.get_plans(
            package_id
        )

        if plans is None:

            self.plan.blockSignals(False)

            self.selection_label.setText(
                "Unable to load plans."
            )

            return

        for plan in plans:

            if not plan.get(
                "is_active",
                False,
            ):
                continue

            if (
                plan["name"]
                .strip()
                .lower()
                == "trial"
            ):
                continue

            self.plan.addItem(
                plan["name"],
                plan,
            )

        self.plan.blockSignals(False)

        self.update_selection()

    def update_selection(self):

        package_name = (
            self.package.currentText().strip()
        )

        plan_data = (
            self.plan.currentData()
        )

        if not package_name or not plan_data:

            self.selection_label.setText(
                "Select a package and plan."
            )

            return

        plan_name = plan_data["name"]

        duration_days = plan_data.get(
            "duration_days"
        )

        price = plan_data["price"]

        if duration_days is None:

            duration = "Lifetime"

        elif duration_days == 1:

            duration = "1 Day"

        else:

            duration = (
                f"{duration_days} Days"
            )

        self.selection_label.setText(
            f"Package: {package_name}\n"
            f"Plan: {plan_name}\n"
            f"Duration: {duration}\n"
            f"Final Price: ${price}"
        )

    def create_subscription(self):

        package_id = (
            self.package.currentData()
        )

        plan_data = (
            self.plan.currentData()
        )

        if (
            package_id is None
            or plan_data is None
        ):

            QMessageBox.warning(
                self,
                "Selection Required",
                "Please select a package and plan.",
            )

            return

        result = (
            SubscriptionAPI.create_subscription(
                token=self.token,
                package_id=package_id,
                plan_id=plan_data["id"],
            )
        )

        if result is None:

            QMessageBox.warning(
                self,
                "Subscription Failed",
                "Unable to create subscription.",
            )

            return

        package_name = (
            self.package.currentText().strip()
        )

        plan_name = plan_data["name"]

        duration_days = (
            plan_data.get("duration_days")
        )

        price = plan_data["price"]

        if duration_days is None:

            duration = "Lifetime"

        elif duration_days == 1:

            duration = "1 Day"

        else:

            duration = (
                f"{duration_days} Days"
            )

        self.payment_window = PaymentWindow(
            token=self.token,
            package_name=package_name,
            plan_name=plan_name,
            duration=duration,
            final_price=price,
        )

        self.payment_window.show()
        self.payment_window.raise_()
        self.payment_window.activateWindow()

        self.hide()