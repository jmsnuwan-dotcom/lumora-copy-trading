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
    QComboBox,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
)

from client.api.package_api import PackageAPI
from client.api.subscription_api import SubscriptionAPI
from client.ui.windows.payment_window import PaymentWindow


class LumoraPackageBackground(QWidget):

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()

        # =====================================================
        # BACKGROUND
        # =====================================================

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
            0.55,
            QColor("#070817"),
        )

        gradient.setColorAt(
            1.0,
            QColor("#12051B"),
        )

        painter.fillRect(
            rect,
            gradient,
        )

        # =====================================================
        # SUBTLE GRID
        # =====================================================

        painter.setPen(
            QPen(
                QColor(
                    90,
                    80,
                    170,
                    18,
                ),
                1,
            )
        )

        grid_size = 45

        for x in range(
            0,
            rect.width(),
            grid_size,
        ):
            painter.drawLine(
                x,
                0,
                x,
                rect.height(),
            )

        for y in range(
            0,
            rect.height(),
            grid_size,
        ):
            painter.drawLine(
                0,
                y,
                rect.width(),
                y,
            )

        # =====================================================
        # TRADING CURVE
        # =====================================================

        path = QPainterPath()

        path.moveTo(
            -20,
            rect.height() * 0.76,
        )

        path.cubicTo(
            rect.width() * 0.16,
            rect.height() * 0.60,
            rect.width() * 0.30,
            rect.height() * 0.90,
            rect.width() * 0.48,
            rect.height() * 0.70,
        )

        path.cubicTo(
            rect.width() * 0.67,
            rect.height() * 0.50,
            rect.width() * 0.82,
            rect.height() * 0.78,
            rect.width() + 20,
            rect.height() * 0.57,
        )

        painter.setPen(
            QPen(
                QColor(
                    150,
                    60,
                    255,
                    65,
                ),
                2,
            )
        )

        painter.drawPath(path)

        # =====================================================
        # CANDLESTICKS
        # =====================================================

        candles = [
            (0.08, 0.72, 0.07),
            (0.12, 0.68, 0.08),
            (0.16, 0.63, 0.09),
            (0.20, 0.58, 0.10),
            (0.24, 0.52, 0.11),
            (0.28, 0.46, 0.12),
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

        # =====================================================
        # LUMORA LOGO
        # =====================================================

        logo_x = rect.width() * 0.20
        logo_y = rect.height() * 0.42

        radius = min(
            rect.width(),
            rect.height(),
        ) * 0.085

        painter.setPen(
            QPen(
                QColor("#15DFFF"),
                4,
            )
        )

        painter.drawArc(
            QRectF(
                logo_x - radius,
                logo_y - radius,
                radius * 2,
                radius * 2,
            ),
            50 * 16,
            285 * 16,
        )

        painter.setPen(
            QPen(
                QColor("#D83DFF"),
                4,
            )
        )

        painter.drawArc(
            QRectF(
                logo_x - radius,
                logo_y - radius,
                radius * 2,
                radius * 2,
            ),
            210 * 16,
            170 * 16,
        )

        # =====================================================
        # L
        # =====================================================

        logo_gradient = QLinearGradient(
            logo_x - radius,
            logo_y + radius,
            logo_x + radius,
            logo_y - radius,
        )

        logo_gradient.setColorAt(
            0,
            QColor("#15DFFF"),
        )

        logo_gradient.setColorAt(
            1,
            QColor("#D83DFF"),
        )

        painter.setPen(
            QPen(
                QBrush(logo_gradient),
                8,
            )
        )

        painter.drawLine(
            QPointF(
                logo_x - radius * 0.30,
                logo_y - radius * 0.55,
            ),
            QPointF(
                logo_x - radius * 0.30,
                logo_y + radius * 0.55,
            ),
        )

        painter.drawLine(
            QPointF(
                logo_x - radius * 0.30,
                logo_y + radius * 0.55,
            ),
            QPointF(
                logo_x + radius * 0.48,
                logo_y + radius * 0.55,
            ),
        )

        # =====================================================
        # LUMORA TEXT
        # =====================================================

        text_gradient = QLinearGradient(
            logo_x - 130,
            logo_y + radius + 45,
            logo_x + 130,
            logo_y + radius + 45,
        )

        text_gradient.setColorAt(
            0,
            QColor("#15DFFF"),
        )

        text_gradient.setColorAt(
            0.55,
            QColor("#6B6DFF"),
        )

        text_gradient.setColorAt(
            1,
            QColor("#E23CFF"),
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
                27,
                QFont.Bold,
            )
        )

        painter.drawText(
            QRectF(
                logo_x - 140,
                logo_y + radius + 30,
                280,
                50,
            ),
            Qt.AlignCenter,
            "LUMORA",
        )

        # =====================================================
        # TAGLINE
        # =====================================================

        painter.setPen(
            QColor("#A9A9B8"),
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                7,
            )
        )

        painter.drawText(
            QRectF(
                logo_x - 150,
                logo_y + radius + 78,
                300,
                30,
            ),
            Qt.AlignCenter,
            "SEE IT FIRST. TRADE SMARTER.",
        )


class PackageSelectionWindow(QMainWindow):

    def __init__(self, token: str):
        super().__init__()

        self.token = token

        self.setWindowTitle(
            "Lumora AI Trading - Select Package"
        )

        self.resize(
            950,
            620,
        )

        self.setMinimumSize(
            850,
            560,
        )

        self.init_ui()

        self.load_packages()

    # ==========================================================
    # UI
    # ==========================================================

    def init_ui(self):

        page = LumoraPackageBackground()

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
            30,
        )

        # ======================================================
        # LEFT SIDE
        # ======================================================

        left = QWidget()

        left_layout = QVBoxLayout(
            left
        )

        left_layout.setAlignment(
            Qt.AlignCenter
        )

        left_layout.addStretch()

        left_layout.addStretch()

        main_layout.addWidget(
            left,
            1,
        )

        # ======================================================
        # PACKAGE CARD
        # ======================================================

        card = QWidget()

        card.setObjectName(
            "packageCard"
        )

        card.setFixedWidth(
            450,
        )

        card_layout = QVBoxLayout(
            card
        )

        card_layout.setContentsMargins(
            38,
            38,
            38,
            38,
        )

        card_layout.setSpacing(
            16,
        )

        # ======================================================
        # TITLE
        # ======================================================

        title = QLabel(
            "Select Your Package"
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
            "CHOOSE YOUR AI TRADING PLAN"
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
            12,
        )

        # ======================================================
        # PACKAGE
        # ======================================================

        self.package = QComboBox()

        self.package.setMinimumHeight(
            52,
        )

        self.package.setObjectName(
            "combo"
        )

        card_layout.addWidget(
            self.package
        )

        # ======================================================
        # PLAN
        # ======================================================

        self.plan = QComboBox()

        self.plan.setMinimumHeight(
            52,
        )

        self.plan.setObjectName(
            "combo"
        )

        card_layout.addWidget(
            self.plan
        )

        # ======================================================
        # SELECTION DETAILS
        # ======================================================

        self.selection_label = QLabel(
            "Select a package and plan."
        )

        self.selection_label.setAlignment(
            Qt.AlignCenter
        )

        self.selection_label.setWordWrap(
            True
        )

        self.selection_label.setMinimumHeight(
            115,
        )

        self.selection_label.setObjectName(
            "selection"
        )

        card_layout.addWidget(
            self.selection_label
        )

        # ======================================================
        # CONTINUE
        # ======================================================

        self.continue_button = QPushButton(
            "Continue to Payment"
        )

        self.continue_button.setMinimumHeight(
            54,
        )

        self.continue_button.setObjectName(
            "continueButton"
        )

        card_layout.addWidget(
            self.continue_button
        )

        # ======================================================
        # CARD SHADOW
        # ======================================================

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(
            45,
        )

        shadow.setOffset(
            0,
            0,
        )

        shadow.setColor(
            QColor(
                120,
                40,
                255,
                105,
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

        self.setCentralWidget(
            page
        )

        self.apply_style()

        # ======================================================
        # EXISTING SIGNALS
        # ======================================================

        self.package.currentIndexChanged.connect(
            self.load_plans
        )

        self.plan.currentIndexChanged.connect(
            self.update_selection
        )

        self.continue_button.clicked.connect(
            self.create_subscription
        )

    # ==========================================================
    # STYLE
    # ==========================================================

    def apply_style(self):

        self.setStyleSheet(
            """
            QMainWindow {
                background: #03040A;
            }

            QWidget#packageCard {
                background: #050710;
                border: 1px solid #29273D;
                border-radius: 24px;
            }

            QLabel#title {
                color: #FFFFFF;
                font-size: 28px;
                font-weight: 700;
            }

            QLabel#subtitle {
                color: #9D9DAD;
                font-size: 10px;
                font-weight: 600;
            }

            QComboBox#combo {
                background: #070913;
                color: #FFFFFF;
                border: 1px solid #303044;
                border-radius: 12px;
                padding: 0 16px;
                font-size: 15px;
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
                color: #C2C2D0;
                background: #070913;
                border: 1px solid #29283B;
                border-radius: 13px;
                padding: 12px;
                font-size: 13px;
            }

            QPushButton#continueButton {
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

            QPushButton#continueButton:hover {
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

            QPushButton#continueButton:pressed {
                padding-top: 2px;
            }
            """
        )

    # ==========================================================
    # LOAD PACKAGES
    # ==========================================================

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

    # ==========================================================
    # LOAD PLANS
    # ==========================================================

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

    # ==========================================================
    # UPDATE SELECTION
    # ==========================================================

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

    # ==========================================================
    # CREATE SUBSCRIPTION
    # ==========================================================

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