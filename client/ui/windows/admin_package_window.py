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

        self.setWindowTitle(
            "Lumora - Package Management"
        )
        self.resize(700, 700)

        self.init_ui()
        self.load_packages()

    def init_ui(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setSpacing(12)

        # ==========================================
        # Package Form
        # ==========================================

        form_box = QGroupBox(
            "Package"
        )

        form = QFormLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText(
            "Package name"
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

        form.addRow(
            "Package Name :",
            self.name,
        )

        form.addRow(
            "Lot Size :",
            self.lot_size,
        )

        form.addRow(
            "Trade Copies :",
            self.trade_copies,
        )

        form_box.setLayout(form)

        # ==========================================
        # Buttons
        # ==========================================

        button_layout = QHBoxLayout()

        self.create_button = QPushButton(
            "Create Package"
        )

        self.update_button = QPushButton(
            "Update Selected"
        )

        self.disable_button = QPushButton(
            "Disable Selected"
        )

        self.clear_button = QPushButton(
            "Clear"
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

        # ==========================================
        # Package List
        # ==========================================

        self.status = QLabel(
            "Loading packages..."
        )

        self.package_layout = QVBoxLayout()
        self.package_layout.setSpacing(8)

        list_box = QGroupBox(
            "Existing Packages"
        )

        list_layout = QVBoxLayout(
            list_box
        )

        list_layout.addWidget(
            self.status
        )

        list_layout.addLayout(
            self.package_layout
        )

        # ==========================================
        # Main Layout
        # ==========================================

        layout.addWidget(
            form_box
        )

        layout.addLayout(
            button_layout
        )

        layout.addWidget(
            list_box
        )

        layout.setAlignment(
            Qt.AlignTop
        )

        self.setCentralWidget(page)

    # ==========================================
    # Load Packages
    # ==========================================

    def load_packages(self):

        packages = PackageAPI.get_packages()

        self.packages = packages or []

        while self.package_layout.count():

            item = self.package_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        if packages is None:

            self.status.setText(
                "Unable to load packages."
            )

            return

        if not packages:

            self.status.setText(
                "No packages found."
            )

            return

        self.status.setText(
            f"Packages : {len(packages)}"
        )

        for package in packages:

            self.add_package_row(
                package
            )

    # ==========================================
    # Package Row
    # ==========================================

    def add_package_row(
        self,
        package: dict,
    ):

        row = QWidget()

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(
            4,
            4,
            4,
            4,
        )

        info = QLabel(
            f'#{package["id"]}  '
            f'{package["name"]}  |  '
            f'Lot: {package["lot_size"]}  |  '
            f'Copies: '
            f'{package["trades_per_signal"]}'
        )

        select_button = QPushButton(
            "Edit"
        )

        select_button.clicked.connect(
            lambda checked=False,
            data=package:
            self.select_package(data)
        )

        row_layout.addWidget(
            info
        )

        row_layout.addWidget(
            select_button
        )

        self.package_layout.addWidget(
            row
        )

    # ==========================================
    # Select Package
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
            float(package["lot_size"])
        )

        self.trade_copies.setValue(
            int(
                package["trades_per_signal"]
            )
        )

        self.update_button.setEnabled(
            True
        )

        self.disable_button.setEnabled(
            True
        )

    # ==========================================
    # Create
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
    # Update
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
        )

        if result is None:

            QMessageBox.warning(
                self,
                "Update Failed",
                "Package could not be updated.",
            )

            return

        QMessageBox.information(
            self,
            "Package Updated",
            "Package updated successfully.",
        )

        self.clear_form()
        self.load_packages()

    # ==========================================
    # Disable
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
    # Clear
    # ==========================================

    def clear_form(self):

        self.selected_package = None

        self.name.clear()

        self.lot_size.setValue(
            0.01
        )

        self.trade_copies.setValue(
            1
        )