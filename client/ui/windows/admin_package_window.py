from PySide6.QtCore import Qt
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
    QSpinBox,
    QDoubleSpinBox,
    QVBoxLayout,
    QWidget,
)

from client.api.package_api import PackageAPI


class AdminPackageWindow(QMainWindow):

    def __init__(self, token: str):
        super().__init__()

        self.token = token
        self.packages = []
        self.selected_package = None
        self.plans = []

        self.setWindowTitle(
            "Lumora AI Trading - Package Management"
        )
        self.resize(1000, 750)

        self.init_ui()
        self.load_packages()

    def init_ui(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(
            28,
            24,
            28,
            24,
        )
        layout.setSpacing(16)

        # ==========================================
        # HEADER
        # ==========================================

        header_layout = QHBoxLayout()

        header_text = QVBoxLayout()
        header_text.setSpacing(4)

        title = QLabel(
            "Package Management"
        )
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Manage Lumora AI Trading packages and pricing."
        )
        subtitle.setObjectName("pageSubtitle")

        header_text.addWidget(title)
        header_text.addWidget(subtitle)

        header_layout.addLayout(
            header_text
        )

        header_layout.addStretch()

        self.package_count = QLabel(
            "• 0 PACKAGES"
        )
        self.package_count.setObjectName(
            "statusBadge"
        )

        header_layout.addWidget(
            self.package_count
        )

        layout.addLayout(
            header_layout
        )

        # ==========================================
        # PACKAGE FORM
        # ==========================================

        form_box = QGroupBox(
            "PACKAGE SETTINGS"
        )
        form_box.setObjectName(
            "sectionBox"
        )

        form = QFormLayout()

        form.setContentsMargins(
            20,
            22,
            20,
            22,
        )

        form.setSpacing(14)

        self.name = QLineEdit()
        self.name.setPlaceholderText(
            "Enter package name"
        )

        self.lot_size = QDoubleSpinBox()
        self.lot_size.setDecimals(2)
        self.lot_size.setRange(
            0.01,
            100.0,
        )
        self.lot_size.setSingleStep(
            0.01
        )
        self.lot_size.setValue(
            0.01
        )

        self.trade_copies = QSpinBox()
        self.trade_copies.setRange(
            1,
            100,
        )
        self.trade_copies.setValue(
            1
        )

        self.monthly_price = QDoubleSpinBox()
        self.monthly_price.setDecimals(2)
        self.monthly_price.setRange(
            0.00,
            1000000.0,
        )
        self.monthly_price.setValue(
            0.00
        )

        self.lifetime_price = QDoubleSpinBox()
        self.lifetime_price.setDecimals(2)
        self.lifetime_price.setRange(
            0.00,
            1000000.0,
        )
        self.lifetime_price.setValue(
            0.00
        )

        form.addRow(
            "Package Name",
            self.name,
        )

        form.addRow(
            "Lot Size",
            self.lot_size,
        )

        form.addRow(
            "Trade Copies",
            self.trade_copies,
        )

        form.addRow(
            "Monthly Price ($)",
            self.monthly_price,
        )

        form.addRow(
            "Lifetime Price ($)",
            self.lifetime_price,
        )

        form_box.setLayout(
            form
        )

        layout.addWidget(
            form_box
        )

        # ==========================================
        # ACTION BUTTONS
        # ==========================================

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.create_button = QPushButton(
            "Create Package"
        )
        self.create_button.setObjectName(
            "primaryButton"
        )

        self.update_button = QPushButton(
            "Update Selected"
        )
        self.update_button.setObjectName(
            "updateButton"
        )

        self.disable_button = QPushButton(
            "Disable Selected"
        )
        self.disable_button.setObjectName(
            "dangerButton"
        )

        self.clear_button = QPushButton(
            "Clear"
        )
        self.clear_button.setObjectName(
            "secondaryButton"
        )

        self.create_button.clicked.connect(
            self.create_package
        )

        self.update_button.clicked.connect(
            self.update_package
        )

        self.disable_button.clicked.connect(
            self.disable_package
        )

        self.clear_button.clicked.connect(
            self.clear_form
        )

        button_layout.addWidget(
            self.create_button
        )

        button_layout.addWidget(
            self.update_button
        )

        button_layout.addWidget(
            self.disable_button
        )

        button_layout.addWidget(
            self.clear_button
        )

        layout.addLayout(
            button_layout
        )

        # ==========================================
        # PACKAGE LIST
        # ==========================================

        list_box = QGroupBox(
            "REGISTERED PACKAGES"
        )
        list_box.setObjectName(
            "sectionBox"
        )

        list_layout = QVBoxLayout(
            list_box
        )

        list_layout.setContentsMargins(
            16,
            18,
            16,
            16,
        )

        self.status = QLabel(
            "Loading packages..."
        )
        self.status.setObjectName(
            "listStatus"
        )

        list_layout.addWidget(
            self.status
        )

        # Header row
        header = QWidget()

        header_layout = QHBoxLayout(
            header
        )

        header_layout.setContentsMargins(
            12,
            6,
            12,
            6,
        )

        client_header = QLabel(
            "PACKAGE"
        )
        client_header.setObjectName(
            "tableHeader"
        )

        action_header = QLabel(
            "ACTIONS"
        )
        action_header.setObjectName(
            "tableHeader"
        )
        action_header.setAlignment(
            Qt.AlignRight
        )

        header_layout.addWidget(
            client_header
        )

        header_layout.addStretch()

        header_layout.addWidget(
            action_header
        )

        list_layout.addWidget(
            header
        )

        # Scroll area
        self.package_layout = QVBoxLayout()
        self.package_layout.setSpacing(8)

        container = QWidget()
        container.setLayout(
            self.package_layout
        )

        scroll = QScrollArea()
        scroll.setWidgetResizable(
            True
        )
        scroll.setWidget(
            container
        )
        scroll.setFrameShape(
            QScrollArea.NoFrame
        )

        list_layout.addWidget(
            scroll
        )

        layout.addWidget(
            list_box
        )

        self.setCentralWidget(
            page
        )

        self.update_button.setEnabled(
            False
        )

        self.disable_button.setEnabled(
            False
        )

        self.setStyleSheet(
            self.get_stylesheet()
        )

    # ==========================================
    # LOAD PACKAGES
    # ==========================================

    def load_packages(self):

        packages = PackageAPI.get_packages()

        self.packages = packages or []

        while self.package_layout.count():

            item = self.package_layout.takeAt(
                0
            )

            widget = item.widget()

            if widget:
                widget.deleteLater()

        if packages is None:

            self.status.setText(
                "Unable to load packages."
            )

            self.package_count.setText(
                "• OFFLINE"
            )

            return

        if not packages:

            self.status.setText(
                "No packages found."
            )

            self.package_count.setText(
                "• 0 PACKAGES"
            )

            return

        self.status.setText(
            f"{len(packages)} package(s) available"
        )

        self.package_count.setText(
            f"• {len(packages)} PACKAGES"
        )

        for package in packages:

            self.add_package_row(
                package
            )

    # ==========================================
    # PACKAGE ROW
    # ==========================================

    def add_package_row(
        self,
        package: dict,
    ):

        row = QWidget()
        row.setObjectName(
            "packageRow"
        )

        row_layout = QHBoxLayout(
            row
        )

        row_layout.setContentsMargins(
            14,
            12,
            14,
            12,
        )

        row_layout.setSpacing(12)

        name = QLabel(
            package.get(
                "name",
                "Unknown",
            )
        )
        name.setObjectName(
            "packageName"
        )

        package_id = QLabel(
            f'Package #{package["id"]}'
        )
        package_id.setObjectName(
            "packageId"
        )

        price = package.get(
            "price",
            0,
        )

        lot_size = package.get(
            "lot_size",
            0,
        )

        copies = package.get(
            "trades_per_signal",
            0,
        )

        info_layout = QVBoxLayout()
        info_layout.setSpacing(3)

        info_layout.addWidget(
            name
        )

        details = QLabel(
            f"{package_id.text()}   •   "
            f"Price: ${price}   •   "
            f"Lot: {lot_size}   •   "
            f"Copies: {copies}"
        )

        details.setObjectName(
            "packageDetails"
        )

        info_layout.addWidget(
            details
        )

        row_layout.addLayout(
            info_layout
        )

        row_layout.addStretch()

        edit_button = QPushButton(
            "EDIT"
        )
        edit_button.setObjectName(
            "editButton"
        )

        edit_button.clicked.connect(
            lambda checked=False,
            data=package:
            self.select_package(data)
        )

        row_layout.addWidget(
            edit_button
        )

        self.package_layout.addWidget(
            row
        )

    # ==========================================
    # SELECT PACKAGE
    # ==========================================

    def select_package(
        self,
        package: dict,
    ):

        self.selected_package = package

        self.name.setText(
            package["name"]
        )

        self.lot_size.setValue(
            float(
                package["lot_size"]
            )
        )

        self.trade_copies.setValue(
            int(
                package[
                    "trades_per_signal"
                ]
            )
        )

        self.monthly_price.setValue(
            0.00
        )

        self.lifetime_price.setValue(
            0.00
        )

        plans = PackageAPI.get_plans(
            package["id"]
        )

        self.plans = plans or []

        for plan in self.plans:

            if plan["name"] == "Monthly":

                self.monthly_price.setValue(
                    float(
                        plan["price"]
                    )
                )

            elif plan["name"] == "Lifetime":

                self.lifetime_price.setValue(
                    float(
                        plan["price"]
                    )
                )

        self.update_button.setEnabled(
            True
        )

        self.disable_button.setEnabled(
            True
        )

    # ==========================================
    # CREATE
    # ==========================================

    def create_package(self):

        name = self.name.text().strip()

        if not name:

            QMessageBox.warning(
                self,
                "Invalid Package",
                "Package name is required.",
            )

            return

        result = PackageAPI.create_package(
            token=self.token,
            name=name,
            lot_size=self.lot_size.value(),
            trades_per_signal=self.trade_copies.value(),
            monthly_price=self.monthly_price.value(),
            lifetime_price=self.lifetime_price.value(),
        )

        if result is None:

            QMessageBox.warning(
                self,
                "Create Failed",
                "Package could not be created.",
            )

            return

        QMessageBox.information(
            self,
            "Package Created",
            "Package created successfully.",
        )

        self.clear_form()
        self.load_packages()

    # ==========================================
    # UPDATE
    # ==========================================

    def update_package(self):

        package = getattr(
            self,
            "selected_package",
            None,
        )

        if package is None:

            QMessageBox.warning(
                self,
                "No Package",
                "Please select a package first.",
            )

            return

        name = self.name.text().strip()

        if not name:

            QMessageBox.warning(
                self,
                "Invalid Package",
                "Package name is required.",
            )

            return

        result = PackageAPI.update_package(
            token=self.token,
            package_id=package["id"],
            name=name,
            lot_size=self.lot_size.value(),
            trades_per_signal=self.trade_copies.value(),
            monthly_price=self.monthly_price.value(),
            lifetime_price=self.lifetime_price.value(),
        )

        if result is None:

            QMessageBox.warning(
                self,
                "Update Failed",
                "Package could not be updated.",
            )

            return

        for plan in self.plans:

            if plan["name"] == "Monthly":

                PackageAPI.update_plan_price(
                    plan_id=plan["id"],
                    price=self.monthly_price.value(),
                )

            elif plan["name"] == "Lifetime":

                PackageAPI.update_plan_price(
                    plan_id=plan["id"],
                    price=self.lifetime_price.value(),
                )

        QMessageBox.information(
            self,
            "Package Updated",
            "Package updated successfully.",
        )

        self.clear_form()
        self.load_packages()

    # ==========================================
    # DISABLE
    # ==========================================

    def disable_package(self):

        package = getattr(
            self,
            "selected_package",
            None,
        )

        if package is None:

            QMessageBox.warning(
                self,
                "No Package",
                "Please select a package first.",
            )

            return

        answer = QMessageBox.question(
            self,
            "Disable Package",
            (
                "Are you sure you want to "
                f'disable "{package["name"]}"?'
            ),
            QMessageBox.Yes
            | QMessageBox.No,
            QMessageBox.No,
        )

        if answer != QMessageBox.Yes:
            return

        result = PackageAPI.disable_package(
            token=self.token,
            package_id=package["id"],
        )

        if result is None:

            QMessageBox.warning(
                self,
                "Disable Failed",
                "Package could not be disabled.",
            )

            return

        QMessageBox.information(
            self,
            "Package Disabled",
            "Package disabled successfully.",
        )

        self.clear_form()
        self.load_packages()

    # ==========================================
    # CLEAR
    # ==========================================

    def clear_form(self):

        self.selected_package = None
        self.plans = []

        self.name.clear()

        self.lot_size.setValue(
            0.01
        )

        self.trade_copies.setValue(
            1
        )

        self.monthly_price.setValue(
            0.00
        )

        self.lifetime_price.setValue(
            0.00
        )

        self.update_button.setEnabled(
            False
        )

        self.disable_button.setEnabled(
            False
        )

    # ==========================================
    # STYLESHEET
    # ==========================================

    def get_stylesheet(self):

        return """
        QMainWindow {
            background-color: #05050F;
        }

        QWidget {
            background-color: #05050F;
            color: #F5F5F7;
            font-family: "Segoe UI";
            font-size: 13px;
        }

        QLabel#pageTitle {
            font-size: 30px;
            font-weight: 700;
            color: #FFFFFF;
        }

        QLabel#pageSubtitle {
            color: #8D8DAA;
            font-size: 13px;
        }

        QLabel#statusBadge {
            background-color: #061C18;
            color: #00E89A;
            border: 1px solid #087653;
            border-radius: 14px;
            padding: 16px 24px;
            font-weight: 700;
            min-width: 130px;
        }

        QGroupBox#sectionBox {
            background-color: #070711;
            border: 1px solid #29293D;
            border-radius: 16px;
            margin-top: 10px;
            padding-top: 10px;
        }

        QGroupBox#sectionBox::title {
            color: #C34CFF;
            subcontrol-origin: margin;
            left: 18px;
            padding: 0 8px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        QLineEdit,
        QSpinBox,
        QDoubleSpinBox {
            background-color: #070711;
            color: #F5F5F7;
            border: 1px solid #303044;
            border-radius: 9px;
            padding: 11px 12px;
            selection-background-color: #713CFF;
        }

        QLineEdit:focus,
        QSpinBox:focus,
        QDoubleSpinBox:focus {
            border: 1px solid #A83CFF;
        }

        QFormLayout QLabel {
            color: #B8B8D0;
            font-weight: 600;
        }

        QPushButton {
            min-height: 38px;
            border-radius: 9px;
            padding: 0 18px;
            font-weight: 700;
        }

        QPushButton#primaryButton {
            background-color: #168FEF;
            color: white;
            border: 1px solid #168FEF;
        }

        QPushButton#primaryButton:hover {
            background-color: #257CFF;
        }

        QPushButton#updateButton {
            background-color: #14142A;
            color: #4FA0FF;
            border: 1px solid #397FFF;
        }

        QPushButton#updateButton:hover {
            background-color: #1A1A35;
        }

        QPushButton#dangerButton {
            background-color: #210B16;
            color: #FF4F78;
            border: 1px solid #D51F58;
        }

        QPushButton#dangerButton:hover {
            background-color: #351020;
        }

        QPushButton#secondaryButton {
            background-color: #0B0B18;
            color: #E7E7EF;
            border: 1px solid #3A3A50;
        }

        QPushButton#secondaryButton:hover {
            border: 1px solid #8A3CFF;
        }

        QPushButton#editButton {
            background-color: #0A0A16;
            color: #FFFFFF;
            border: 1px solid #7A3CFF;
            min-width: 70px;
        }

        QPushButton#editButton:hover {
            background-color: #17132A;
        }

        QLabel#listStatus {
            color: #8D8DAA;
            padding: 4px 4px 8px 4px;
        }

        QLabel#tableHeader {
            color: #747493;
            font-size: 11px;
            font-weight: 700;
        }

        QWidget#packageRow {
            background-color: #080812;
            border: 1px solid #28283D;
            border-radius: 12px;
        }

        QWidget#packageRow:hover {
            border: 1px solid #6034A0;
            background-color: #0B0B17;
        }

        QLabel#packageName {
            color: #FFFFFF;
            font-size: 15px;
            font-weight: 700;
        }

        QLabel#packageId,
        QLabel#packageDetails {
            color: #8585A4;
            font-size: 12px;
        }

        QScrollArea {
            background-color: transparent;
            border: none;
        }

        QMessageBox {
            background-color: #070711;
            color: #F5F5F7;
        }

        QMessageBox QLabel {
            color: #E8E8F0;
        }

        QMessageBox QPushButton {
            background-color: #080814;
            color: #FFFFFF;
            border: 1px solid #00D9FF;
            border-radius: 8px;
            padding: 8px 22px;
            min-width: 60px;
        }

        QMessageBox QPushButton:hover {
            background-color: #17172A;
            border: 1px solid #B83CFF;
        }
        """