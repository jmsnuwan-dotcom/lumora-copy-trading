from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import (
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QBrush,
)
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QMessageBox,
    QHBoxLayout,
    QFrame,
    QScrollArea,
    QGraphicsDropShadowEffect,
)

from client.api.register_api import RegisterAPI
from client.api.package_api import PackageAPI
from client.ui.windows.payment_window import PaymentWindow


class LumoraRegisterBackground(QWidget):

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()

        # ==========================================
        # DARK BACKGROUND
        # ==========================================

        gradient = QLinearGradient(
            0,
            0,
            rect.width(),
            rect.height(),
        )

        gradient.setColorAt(
            0.0,
            QColor("#03040A"),
        )

        gradient.setColorAt(
            0.5,
            QColor("#060817"),
        )

        gradient.setColorAt(
            1.0,
            QColor("#12051B"),
        )

        painter.fillRect(
            rect,
            gradient,
        )

        # ==========================================
        # NETWORK NODES
        # ==========================================

        nodes = [
            (0.04, 0.08),
            (0.12, 0.11),
            (0.07, 0.22),
            (0.18, 0.17),
            (0.88, 0.10),
            (0.95, 0.14),
            (0.91, 0.25),
            (0.82, 0.18),
        ]

        points = []

        for x_ratio, y_ratio in nodes:

            point = QPointF(
                rect.width() * x_ratio,
                rect.height() * y_ratio,
            )

            points.append(point)

        painter.setPen(
            QPen(
                QColor(100, 55, 220, 45),
                1,
            )
        )

        for i in range(len(points)):

            for j in range(i + 1, len(points)):

                if (
                    abs(points[i].x() - points[j].x())
                    < rect.width() * 0.25
                ):

                    painter.drawLine(
                        points[i],
                        points[j],
                    )

        painter.setPen(Qt.NoPen)

        for point in points:

            painter.setBrush(
                QColor(
                    110,
                    55,
                    255,
                    120,
                )
            )

            painter.drawEllipse(
                point,
                3,
                3,
            )

        # ==========================================
        # CURVED TRADING LINES
        # ==========================================

        path = QPainterPath()

        path.moveTo(
            -20,
            rect.height() * 0.72,
        )

        path.cubicTo(
            rect.width() * 0.18,
            rect.height() * 0.55,
            rect.width() * 0.32,
            rect.height() * 0.90,
            rect.width() * 0.52,
            rect.height() * 0.72,
        )

        path.cubicTo(
            rect.width() * 0.70,
            rect.height() * 0.55,
            rect.width() * 0.82,
            rect.height() * 0.84,
            rect.width() + 20,
            rect.height() * 0.63,
        )

        painter.setPen(
            QPen(
                QColor(
                    130,
                    55,
                    255,
                    80,
                ),
                2,
            )
        )

        painter.drawPath(path)

        # ==========================================
        # SECOND CURVE
        # ==========================================

        path2 = QPainterPath()

        path2.moveTo(
            -20,
            rect.height() * 0.76,
        )

        path2.cubicTo(
            rect.width() * 0.20,
            rect.height() * 0.60,
            rect.width() * 0.34,
            rect.height() * 0.94,
            rect.width() * 0.53,
            rect.height() * 0.76,
        )

        path2.cubicTo(
            rect.width() * 0.70,
            rect.height() * 0.60,
            rect.width() * 0.83,
            rect.height() * 0.87,
            rect.width() + 20,
            rect.height() * 0.68,
        )

        painter.setPen(
            QPen(
                QColor(
                    20,
                    180,
                    255,
                    45,
                ),
                1,
            )
        )

        painter.drawPath(path2)

        # ==========================================
        # CANDLESTICKS
        # ==========================================

        candles = [
            (0.13, 0.67, 0.07),
            (0.17, 0.63, 0.08),
            (0.21, 0.59, 0.09),
            (0.25, 0.55, 0.10),
            (0.29, 0.50, 0.11),
            (0.33, 0.45, 0.12),
        ]

        for x_ratio, y_ratio, height_ratio in candles:

            x = rect.width() * x_ratio
            y = rect.height() * y_ratio

            height = (
                rect.height()
                * height_ratio
            )

            painter.setPen(
                QPen(
                    QColor("#16DFFF"),
                    1,
                )
            )

            painter.drawLine(
                QPointF(
                    x,
                    y - height * 0.45,
                ),
                QPointF(
                    x,
                    y + height * 0.45,
                ),
            )

            body_gradient = QLinearGradient(
                x,
                y - height * 0.25,
                x,
                y + height * 0.25,
            )

            body_gradient.setColorAt(
                0,
                QColor("#16DFFF"),
            )

            body_gradient.setColorAt(
                1,
                QColor("#5858FF"),
            )

            painter.setBrush(
                QBrush(body_gradient)
            )

            painter.setPen(Qt.NoPen)

            painter.drawRoundedRect(
                QRectF(
                    x - 5,
                    y - height * 0.25,
                    10,
                    height * 0.5,
                ),
                2,
                2,
            )

        # ==========================================
        # LUMORA LOGO
        # ==========================================

        logo_x = rect.width() * 0.26
        logo_y = rect.height() * 0.38

        radius = min(
            rect.width(),
            rect.height(),
        ) * 0.105

        painter.setPen(
            QPen(
                QColor("#14DFFF"),
                5,
            )
        )

        painter.drawArc(
            QRectF(
                logo_x - radius,
                logo_y - radius,
                radius * 2,
                radius * 2,
            ),
            45 * 16,
            285 * 16,
        )

        painter.setPen(
            QPen(
                QColor("#D63CFF"),
                5,
            )
        )

        painter.drawArc(
            QRectF(
                logo_x - radius,
                logo_y - radius,
                radius * 2,
                radius * 2,
            ),
            205 * 16,
            180 * 16,
        )

        # L mark

        logo_gradient = QLinearGradient(
            logo_x - radius,
            logo_y + radius,
            logo_x + radius,
            logo_y - radius,
        )

        logo_gradient.setColorAt(
            0,
            QColor("#14DFFF"),
        )

        logo_gradient.setColorAt(
            1,
            QColor("#D63CFF"),
        )

        painter.setPen(
            QPen(
                QBrush(logo_gradient),
                9,
            )
        )

        painter.drawLine(
            QPointF(
                logo_x - radius * 0.28,
                logo_y - radius * 0.55,
            ),
            QPointF(
                logo_x - radius * 0.28,
                logo_y + radius * 0.55,
            ),
        )

        painter.drawLine(
            QPointF(
                logo_x - radius * 0.28,
                logo_y + radius * 0.55,
            ),
            QPointF(
                logo_x + radius * 0.45,
                logo_y + radius * 0.55,
            ),
        )

        # ==========================================
        # LUMORA TEXT
        # ==========================================

        text_gradient = QLinearGradient(
            logo_x - 150,
            logo_y + radius + 55,
            logo_x + 150,
            logo_y + radius + 55,
        )

        text_gradient.setColorAt(
            0,
            QColor("#14DFFF"),
        )

        text_gradient.setColorAt(
            0.5,
            QColor("#7474FF"),
        )

        text_gradient.setColorAt(
            1,
            QColor("#E03CFF"),
        )

        painter.setPen(
            QPen(
                QBrush(text_gradient),
                1,
            )
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                30,
                QFont.Bold,
            )
        )

        painter.drawText(
            QRectF(
                logo_x - 145,
                logo_y + radius + 55,
                290,
                55,
            ),
            Qt.AlignCenter,
            "LUMORA",
        )

        # ==========================================
        # TAGLINE
        # ==========================================

        painter.setPen(
            QColor("#D2D2DD"),
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                8,
            )
        )

        painter.drawText(
            QRectF(
                logo_x - 150,
                logo_y + radius + 108,
                300,
                30,
            ),
            Qt.AlignCenter,
            "SEE IT FIRST. TRADE SMARTER.",
        )


class RegisterWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Lumora AI Trading"
        )

        self.resize(
            1100,
            720,
        )

        self.setMinimumSize(
            950,
            620,
        )

        self.init_ui()

        self.load_packages()

    def init_ui(self):

        page = LumoraRegisterBackground()

        main_layout = QHBoxLayout(
            page
        )

        main_layout.setContentsMargins(
            45,
            35,
            45,
            35,
        )

        main_layout.setSpacing(
            35
        )

        page.setMinimumSize(
            950,
            620,
        )

        # ==========================================
        # LEFT SIDE
        # ==========================================

        left_panel = QWidget()

        left_layout = QVBoxLayout(
            left_panel
        )

        left_layout.setAlignment(
            Qt.AlignCenter
        )

        left_layout.addStretch()
        left_layout.addStretch()

        main_layout.addWidget(
            left_panel,
            1,
        )

        # ==========================================
        # REGISTER CARD
        # ==========================================

        card = QWidget()

        card.setObjectName(
            "registerCard"
        )

        card.setFixedWidth(
            490
        )

        card_layout = QVBoxLayout(
            card
        )

        card_layout.setContentsMargins(
            38,
            34,
            38,
            34,
        )

        card_layout.setSpacing(
            13
        )

        # ==========================================
        # TITLE
        # ==========================================

        title = QLabel(
            "Create Your Lumora Account"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setObjectName(
            "title"
        )

        card_layout.addWidget(
            title
        )

        subtitle = QLabel(
            "START TRADING SMARTER"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        subtitle.setObjectName(
            "subtitle"
        )

        card_layout.addWidget(
            subtitle
        )

        card_layout.addSpacing(
            10
        )

        # ==========================================
        # FULL NAME
        # ==========================================

        self.full_name = QLineEdit()

        self.full_name.setPlaceholderText(
            "Full Name"
        )

        self.full_name.setMinimumHeight(
            48
        )

        self.full_name.setObjectName(
            "input"
        )

        card_layout.addWidget(
            self.full_name
        )

        # ==========================================
        # EMAIL
        # ==========================================

        self.email = QLineEdit()

        self.email.setPlaceholderText(
            "Email"
        )

        self.email.setMinimumHeight(
            48
        )

        self.email.setObjectName(
            "input"
        )

        card_layout.addWidget(
            self.email
        )

        # ==========================================
        # PHONE
        # ==========================================

        self.phone = QLineEdit()

        self.phone.setPlaceholderText(
            "Phone Number"
        )

        self.phone.setMinimumHeight(
            48
        )

        self.phone.setObjectName(
            "input"
        )

        card_layout.addWidget(
            self.phone
        )

        # ==========================================
        # PASSWORD
        # ==========================================

        self.password = QLineEdit()

        self.password.setPlaceholderText(
            "Password"
        )

        self.password.setEchoMode(
            QLineEdit.Password
        )

        self.password.setMinimumHeight(
            48
        )

        self.password.setObjectName(
            "input"
        )

        card_layout.addWidget(
            self.password
        )

        # ==========================================
        # CONFIRM PASSWORD
        # ==========================================

        self.confirm_password = QLineEdit()

        self.confirm_password.setPlaceholderText(
            "Confirm Password"
        )

        self.confirm_password.setEchoMode(
            QLineEdit.Password
        )

        self.confirm_password.setMinimumHeight(
            48
        )

        self.confirm_password.setObjectName(
            "input"
        )

        card_layout.addWidget(
            self.confirm_password
        )

        # ==========================================
        # PACKAGE
        # ==========================================

        self.package = QComboBox()

        self.package.setMinimumHeight(
            48
        )

        self.package.setObjectName(
            "combo"
        )

        card_layout.addWidget(
            self.package
        )

        # ==========================================
        # PLAN
        # ==========================================

        self.plan = QComboBox()

        self.plan.setMinimumHeight(
            48
        )

        self.plan.setObjectName(
            "combo"
        )

        card_layout.addWidget(
            self.plan
        )

        # ==========================================
        # SELECTION
        # ==========================================

        self.selection_label = QLabel()

        self.selection_label.setAlignment(
            Qt.AlignCenter
        )

        self.selection_label.setWordWrap(
            True
        )

        self.selection_label.setMinimumHeight(
            65
        )

        self.selection_label.setObjectName(
            "selection"
        )

        self.selection_label.setText(
            "Select a package and plan."
        )

        card_layout.addWidget(
            self.selection_label
        )

        # ==========================================
        # REGISTER
        # ==========================================

        self.register_button = QPushButton(
            "Register"
        )

        self.register_button.setMinimumHeight(
            52
        )

        self.register_button.setObjectName(
            "registerButton"
        )

        self.register_button.clicked.connect(
            self.register
        )

        card_layout.addWidget(
            self.register_button
        )

        # ==========================================
        # SHADOW
        # ==========================================

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(
            45
        )

        shadow.setOffset(
            0,
            0
        )

        shadow.setColor(
            QColor(
                120,
                40,
                255,
                110,
            )
        )

        card.setGraphicsEffect(
            shadow
        )

        main_layout.addWidget(
            card,
            0,
            Qt.AlignCenter,
        )

        # ==========================================
        # FULL PAGE SCROLL
        # ==========================================

        page.setMinimumSize(
            950,
            620,
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
            page
        )

        self.setCentralWidget(
            scroll
        )

        self.apply_style()

        # ==========================================
        # EXISTING SIGNALS
        # ==========================================

        self.package.currentIndexChanged.connect(
            self.load_plans
        )

        self.plan.currentIndexChanged.connect(
            self.update_selection
        )

    def apply_style(self):

        self.setStyleSheet(
            """
            QMainWindow {
                background: #03040A;
            }

            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollArea > QWidget {
                background: transparent;
                border: none;
            }

            QScrollArea > QWidget > QWidget {
                background: transparent;
                border: none;
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
                background: #713D9F;
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

            QWidget#registerCard {
                background: rgba(5, 7, 16, 245);
                border: 1px solid #29273D;
                border-radius: 24px;
            }

            QLabel#title {
                color: #FFFFFF;
                font-size: 27px;
                font-weight: 700;
            }

            QLabel#subtitle {
                color: #9D9DAD;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 2px;
            }

            QLineEdit#input {
                background: #070913;
                color: #FFFFFF;
                border: 1px solid #303044;
                border-radius: 11px;
                padding: 0 16px;
                font-size: 14px;
            }

            QLineEdit#input:focus {
                background: #090B18;
                border: 1px solid #8C4DFF;
            }

            QLineEdit#input::placeholder {
                color: #77778A;
            }

            QComboBox#combo {
                background: #070913;
                color: #FFFFFF;
                border: 1px solid #303044;
                border-radius: 11px;
                padding: 0 14px;
                font-size: 14px;
            }

            QComboBox#combo:hover {
                border: 1px solid #6550D8;
            }

            QComboBox#combo:focus {
                border: 1px solid #8C4DFF;
            }

            QComboBox#combo QAbstractItemView {
                background: #080A14;
                color: #FFFFFF;
                border: 1px solid #393553;
                selection-background-color: #6037B8;
                selection-color: #FFFFFF;
            }

            QLabel#selection {
                color: #B8B8C7;
                background: #070913;
                border: 1px solid #29283B;
                border-radius: 11px;
                padding: 8px;
                font-size: 12px;
            }

            QPushButton#registerButton {
                color: #FFFFFF;
                font-size: 16px;
                font-weight: 700;
                border: none;
                border-radius: 12px;

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

            QPushButton#registerButton:hover {
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

            QPushButton#registerButton:pressed {
                padding-top: 2px;
            }
            """
        )

    def register(self):

        package_id = self.package.currentData()
        plan_data = self.plan.currentData()

        if package_id is None or plan_data is None:

            QMessageBox.warning(
                self,
                "Registration Failed",
                "Please select a package and plan.",
            )

            return

        result = RegisterAPI.register(
            full_name=self.full_name.text().strip(),
            email=self.email.text().strip(),
            phone=self.phone.text().strip(),
            password=self.password.text(),
            confirm_password=self.confirm_password.text(),
            package_id=package_id,
            plan_id=plan_data["id"],
        )

        if result is None:

            QMessageBox.warning(
                self,
                "Registration Failed",
                "Registration failed.",
            )

            return

        token = result.get(
            "access_token"
        )

        if not token:

            QMessageBox.warning(
                self,
                "Registration Failed",
                "Registration succeeded, but authentication failed.",
            )

            return

        package_name = (
            self.package.currentText().strip()
        )

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

        self.payment_window = PaymentWindow(
            token=token,
            package_name=package_name,
            plan_name=plan_name,
            duration=duration,
            final_price=price,
        )

        self.payment_window.show()
        self.payment_window.raise_()
        self.payment_window.activateWindow()

        self.hide()

    def load_packages(self):

        self.package.blockSignals(
            True
        )

        self.package.clear()

        packages = PackageAPI.get_packages()

        if packages is None:

            self.package.blockSignals(
                False
            )

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

        self.package.blockSignals(
            False
        )

        self.load_plans()

    def load_plans(self):

        self.plan.blockSignals(
            True
        )

        self.plan.clear()

        package_id = (
            self.package.currentData()
        )

        if package_id is None:

            self.plan.blockSignals(
                False
            )

            self.update_selection()

            return

        plans = PackageAPI.get_plans(
            package_id
        )

        if plans is None:

            self.plan.blockSignals(
                False
            )

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

        self.plan.blockSignals(
            False
        )

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