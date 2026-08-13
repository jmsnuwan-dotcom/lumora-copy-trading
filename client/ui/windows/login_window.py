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
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMainWindow,
    QMessageBox,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
)

from client.api.auth_api import AuthAPI
from client.api.subscription_api import SubscriptionAPI

from client.ui.windows.register_window import RegisterWindow
from client.ui.windows.dashboard_window import DashboardWindow
from client.ui.windows.admin_dashboard_window import (
    AdminDashboardWindow,
)
from client.ui.windows.package_selection_window import (
    PackageSelectionWindow,
)
from client.ui.windows.payment_window import PaymentWindow


class LumoraBackground(QWidget):

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()

        # ==========================================
        # BACKGROUND
        # ==========================================

        gradient = QLinearGradient(
            0,
            0,
            rect.width(),
            rect.height(),
        )

        gradient.setColorAt(
            0.0,
            QColor("#03040a"),
        )

        gradient.setColorAt(
            0.5,
            QColor("#070817"),
        )

        gradient.setColorAt(
            1.0,
            QColor("#12051b"),
        )

        painter.fillRect(
            rect,
            gradient,
        )

        # ==========================================
        # SUBTLE NETWORK DOTS
        # ==========================================

        painter.setPen(
            QPen(
                QColor(80, 70, 180, 45),
                1,
            )
        )

        points = [
            (35, 75),
            (130, 125),
            (85, 215),
            (190, 180),
            (rect.width() - 80, 90),
            (rect.width() - 150, 160),
            (rect.width() - 50, 240),
        ]

        for x, y in points:

            if x < rect.width() and y < rect.height():

                painter.drawEllipse(
                    QPointF(x, y),
                    3,
                    3,
                )

        # ==========================================
        # PURPLE CURVE
        # ==========================================

        path = QPainterPath()

        path.moveTo(
            0,
            rect.height() * 0.72,
        )

        path.cubicTo(
            rect.width() * 0.18,
            rect.height() * 0.58,
            rect.width() * 0.32,
            rect.height() * 0.88,
            rect.width() * 0.52,
            rect.height() * 0.72,
        )

        path.cubicTo(
            rect.width() * 0.70,
            rect.height() * 0.55,
            rect.width() * 0.82,
            rect.height() * 0.82,
            rect.width(),
            rect.height() * 0.62,
        )

        painter.setPen(
            QPen(
                QColor(150, 60, 255, 75),
                2,
            )
        )

        painter.drawPath(path)

        # ==========================================
        # CANDLESTICKS
        # ==========================================

        candle_data = [
            (0.12, 0.67, 0.06),
            (0.16, 0.63, 0.07),
            (0.20, 0.59, 0.08),
            (0.24, 0.55, 0.09),
            (0.28, 0.51, 0.10),
            (0.32, 0.47, 0.11),
        ]

        for index, (
            x_ratio,
            y_ratio,
            height_ratio,
        ) in enumerate(candle_data):

            x = rect.width() * x_ratio
            y = rect.height() * y_ratio

            candle_height = (
                rect.height() * height_ratio
            )

            # Wick
            painter.setPen(
                QPen(
                    QColor("#16d9ff"),
                    2,
                )
            )

            painter.drawLine(
                QPointF(
                    x,
                    y - candle_height * 0.35,
                ),
                QPointF(
                    x,
                    y + candle_height * 0.35,
                ),
            )

            # Body
            body_gradient = QLinearGradient(
                x,
                y - candle_height * 0.25,
                x,
                y + candle_height * 0.25,
            )

            body_gradient.setColorAt(
                0,
                QColor("#15e1ff"),
            )

            body_gradient.setColorAt(
                1,
                QColor("#4166ff"),
            )

            painter.setBrush(
                QBrush(body_gradient)
            )

            painter.setPen(Qt.NoPen)

            painter.drawRoundedRect(
                QRectF(
                    x - 7,
                    y - candle_height * 0.25,
                    14,
                    candle_height * 0.5,
                ),
                3,
                3,
            )

        # ==========================================
        # LUMORA LOGO MARK
        # ==========================================

        logo_x = rect.width() * 0.23
        logo_y = rect.height() * 0.42

        radius = min(
            rect.width(),
            rect.height(),
        ) * 0.115

        # Glow
        painter.setPen(
            QPen(
                QColor(40, 210, 255, 180),
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
            50 * 16,
            285 * 16,
        )

        painter.setPen(
            QPen(
                QColor(220, 55, 255, 190),
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
            210 * 16,
            170 * 16,
        )

        # L shape
        logo_gradient = QLinearGradient(
            logo_x - radius,
            logo_y + radius,
            logo_x + radius,
            logo_y - radius,
        )

        logo_gradient.setColorAt(
            0,
            QColor("#18dfff"),
        )

        logo_gradient.setColorAt(
            1,
            QColor("#d83dff"),
        )

        painter.setPen(
            QPen(
                QBrush(logo_gradient),
                10,
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

        # ==========================================
        # LUMORA TEXT
        # ==========================================

        text_gradient = QLinearGradient(
            logo_x - 130,
            logo_y + radius + 55,
            logo_x + 150,
            logo_y + radius + 55,
        )

        text_gradient.setColorAt(
            0,
            QColor("#15dfff"),
        )

        text_gradient.setColorAt(
            0.55,
            QColor("#6b6dff"),
        )

        text_gradient.setColorAt(
            1,
            QColor("#e23cff"),
        )

        painter.setPen(
            QPen(
                QBrush(text_gradient),
                1,
            )
        )

        font = QFont(
            "Segoe UI",
            32,
            QFont.Bold,
        )

        painter.setFont(font)

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

        # Tagline

        painter.setPen(
            QColor("#d5d5df"),
        )

        tagline_font = QFont(
            "Segoe UI",
            8,
        )

        tagline_font.setLetterSpacing(
            QFont.AbsoluteSpacing,
            3,
        )

        painter.setFont(
            tagline_font
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


class LoginWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.token = None

        self.admin_dashboard_window = None
        self.dashboard = None
        self.package_selection_window = None
        self.payment_window = None
        self.register_window = None

        self.setWindowTitle(
            "Lumora AI Trading"
        )

        self.resize(
            1050,
            650,
        )

        self.setMinimumSize(
            900,
            580,
        )

        self.init_ui()

    def init_ui(self):

        page = LumoraBackground()

        main_layout = QHBoxLayout(
            page
        )

        main_layout.setContentsMargins(
            45,
            35,
            45,
            35,
        )

        main_layout.setSpacing(30)

        # ==========================================
        # LEFT SIDE
        # ==========================================

        left = QWidget()

        left_layout = QVBoxLayout(
            left
        )

        left_layout.setAlignment(
            Qt.AlignCenter
        )

        left_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        left_layout.addStretch()

        left_layout.addStretch()

        main_layout.addWidget(
            left,
            1,
        )

        # ==========================================
        # LOGIN CARD
        # ==========================================

        card = QWidget()

        card.setObjectName(
            "loginCard"
        )

        card.setFixedWidth(
            440
        )

        card_layout = QVBoxLayout(
            card
        )

        card_layout.setContentsMargins(
            40,
            42,
            40,
            42,
        )

        card_layout.setSpacing(
            18
        )

        # Title

        title = QLabel(
            "Lumora AI Trading"
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

        # Subtitle

        subtitle = QLabel(
            "SEE IT FIRST. TRADE SMARTER."
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
            20
        )

        # ==========================================
        # EMAIL
        # ==========================================

        self.email = QLineEdit()

        self.email.setPlaceholderText(
            "Email"
        )

        self.email.setMinimumHeight(
            54
        )

        self.email.setObjectName(
            "input"
        )

        card_layout.addWidget(
            self.email
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
            54
        )

        self.password.setObjectName(
            "input"
        )

        card_layout.addWidget(
            self.password
        )

        card_layout.addSpacing(
            10
        )

        # ==========================================
        # LOGIN BUTTON
        # ==========================================

        self.login_button = QPushButton(
            "Login"
        )

        self.login_button.setMinimumHeight(
            54
        )

        self.login_button.setObjectName(
            "loginButton"
        )

        self.login_button.clicked.connect(
            self.login
        )

        card_layout.addWidget(
            self.login_button
        )

        # ==========================================
        # REGISTER BUTTON
        # ==========================================

        self.register_button = QPushButton(
            "Create Account"
        )

        self.register_button.setMinimumHeight(
            54
        )

        self.register_button.setObjectName(
            "registerButton"
        )

        self.register_button.clicked.connect(
            self.open_register
        )

        card_layout.addWidget(
            self.register_button
        )

        card_layout.addStretch()

        # ==========================================
        # CARD SHADOW
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
                100,
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

    def apply_style(self):

        self.setStyleSheet(
            """
            QMainWindow {
                background: #03040a;
            }

            QWidget#loginCard {
                background: rgba(5, 7, 16, 245);
                border: 1px solid #29273d;
                border-radius: 24px;
            }

            QLabel#title {
                color: #ffffff;
                font-size: 29px;
                font-weight: 700;
            }

            QLabel#subtitle {
                color: #a7a7b7;
                font-size: 11px;
                letter-spacing: 2px;
            }

            QLineEdit#input {
                background: #070913;
                color: #ffffff;
                border: 1px solid #303044;
                border-radius: 12px;
                padding: 0 18px;
                font-size: 15px;
            }

            QLineEdit#input:focus {
                border: 1px solid #8c4dff;
                background: #090b18;
            }

            QLineEdit#input::placeholder {
                color: #77778a;
            }

            QPushButton#loginButton {
                color: #ffffff;
                font-size: 16px;
                font-weight: 600;
                border: none;
                border-radius: 12px;
                background: qlineargradient(
                    x1: 0,
                    y1: 0,
                    x2: 1,
                    y2: 0,
                    stop: 0 #079df5,
                    stop: 0.5 #5858ff,
                    stop: 1 #d42cff
                );
            }

            QPushButton#loginButton:hover {
                background: qlineargradient(
                    x1: 0,
                    y1: 0,
                    x2: 1,
                    y2: 0,
                    stop: 0 #16b5ff,
                    stop: 0.5 #7474ff,
                    stop: 1 #e348ff
                );
            }

            QPushButton#loginButton:pressed {
                padding-top: 2px;
            }

            QPushButton#registerButton {
                color: #ffffff;
                font-size: 15px;
                font-weight: 600;
                background: transparent;
                border: 1px solid #1adfff;
                border-radius: 12px;
            }

            QPushButton#registerButton:hover {
                background: rgba(20, 220, 255, 25);
                border: 1px solid #d23cff;
            }
            """
        )

    def login(self):

        email = self.email.text().strip()
        password = self.password.text()

        if not email or not password:

            QMessageBox.warning(
                self,
                "Login Required",
                "Please enter your email and password.",
            )

            return

        result = AuthAPI.login_request(
            email,
            password,
        )

        if not result["success"]:

            QMessageBox.warning(
                self,
                "Login Failed",
                result["message"],
            )

            return

        data = result["data"]

        self.token = data[
            "access_token"
        ]

        user = data["user"]

        # ==========================================
        # ADMIN
        # ==========================================

        if user["role"] == "admin":

            self.admin_dashboard_window = (
                AdminDashboardWindow(
                    self.token
                )
            )

            self.admin_dashboard_window.show()

            self.hide()

            return

        # ==========================================
        # CLIENT
        # ==========================================

        subscription = (
            SubscriptionAPI.get_my_subscription(
                self.token
            )
        )

        # ------------------------------------------
        # NO SUBSCRIPTION
        # ------------------------------------------

        if subscription is None:

            self.open_package_selection()

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

        # ==========================================
        # PAYMENT WAITING
        # ==========================================

        if (
            status in {
                "PENDING",
                "SUBMITTED",
            }
            or payment_status in {
                "PENDING",
                "SUBMITTED",
            }
        ):

            self.open_pending_payment(
                subscription
            )

            return

        # ==========================================
        # APPROVED / ACTIVE
        # ==========================================

        if status in {
            "APPROVED",
            "ACTIVE",
        }:

            self.open_dashboard()

            return

        # ==========================================
        # UNKNOWN / EXPIRED / OTHER
        # ==========================================

        self.open_package_selection()

    def open_package_selection(self):

        self.package_selection_window = (
            PackageSelectionWindow(
                token=self.token,
            )
        )

        self.package_selection_window.show()
        self.package_selection_window.raise_()
        self.package_selection_window.activateWindow()

        self.hide()

    def open_pending_payment(
        self,
        subscription: dict,
    ):

        package = subscription.get(
            "package"
        ) or {}

        plan = subscription.get(
            "plan"
        ) or {}

        package_name = package.get(
            "name",
            "Unknown",
        )

        plan_name = plan.get(
            "name",
            "Unknown",
        )

        duration_days = plan.get(
            "duration_days"
        )

        price = plan.get(
            "price",
            0,
        )

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

    def open_dashboard(self):

        self.dashboard = DashboardWindow(
            self.token
        )

        self.dashboard.show()
        self.dashboard.raise_()
        self.dashboard.activateWindow()

        self.hide()

    def open_register(self):

        self.register_window = RegisterWindow()

        self.register_window.show()
        self.register_window.raise_()
        self.register_window.activateWindow()