from datetime import datetime, timedelta, timezone

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from client.api.admin_api import AdminAPI


class AdminOnlineWindow(QMainWindow):

    def __init__(self, token: str):
        super().__init__()

        self.token = token

        self.setWindowTitle(
            "Lumora AI Trading - Online Users"
        )

        self.resize(
            1150,
            760,
        )

        # ======================================================
        # MAIN WINDOW PALETTE
        # ======================================================

        palette = self.palette()

        palette.setColor(
            QPalette.Window,
            "#05050d",
        )

        palette.setColor(
            QPalette.Base,
            "#05050d",
        )

        palette.setColor(
            QPalette.AlternateBase,
            "#05050d",
        )

        palette.setColor(
            QPalette.WindowText,
            "#f5f5f7",
        )

        self.setPalette(
            palette
        )

        # ======================================================
        # GLOBAL STYLE
        # ======================================================

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #05050d;
            }

            QWidget {
                background-color: #05050d;
                color: #f5f5f7;
                font-family: "Segoe UI";
                font-size: 13px;
            }

            QLabel {
                background-color: transparent;
                color: #f5f5f7;
            }

            QFrame {
                background-color: transparent;
            }

            QScrollArea {
                background-color: #05050d;
                border: none;
            }

            QScrollArea QWidget {
                background-color: #05050d;
            }

            QScrollBar:vertical {
                background: #070711;
                width: 10px;
                margin: 0px;
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
                border: none;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: #05050d;
            }

            QScrollBar:horizontal {
                background: #05050d;
                height: 0px;
                border: none;
            }
            """
        )

        self.init_ui()

        self.load_online_users()

        # ======================================================
        # AUTO REFRESH
        # ======================================================

        self.refresh_timer = QTimer(
            self
        )

        self.refresh_timer.timeout.connect(
            self.load_online_users
        )

        self.refresh_timer.start(
            15000
        )

    # ==========================================================
    # UI
    # ==========================================================

    def init_ui(self):

        page = QWidget()

        page.setAutoFillBackground(
            True
        )

        page_palette = page.palette()

        page_palette.setColor(
            QPalette.Window,
            "#05050d",
        )

        page_palette.setColor(
            QPalette.Base,
            "#05050d",
        )

        page.setPalette(
            page_palette
        )

        page.setStyleSheet(
            """
            QWidget {
                background-color: #05050d;
                color: #f5f5f7;
            }
            """
        )

        layout = QVBoxLayout(
            page
        )

        layout.setContentsMargins(
            28,
            24,
            28,
            24,
        )

        layout.setSpacing(
            18
        )

        # ======================================================
        # HEADER
        # ======================================================

        header_layout = QHBoxLayout()

        header_layout.setSpacing(
            20
        )

        title_box = QVBoxLayout()

        title_box.setSpacing(
            5
        )

        title = QLabel(
            "Online Users"
        )

        title.setStyleSheet(
            """
            QLabel {
                background: transparent;
                color: #ffffff;
                font-size: 28px;
                font-weight: 800;
            }
            """
        )

        subtitle = QLabel(
            "Clients currently online through heartbeat."
        )

        subtitle.setStyleSheet(
            """
            QLabel {
                background: transparent;
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

        # ======================================================
        # ONLINE COUNT
        # ======================================================

        self.online_count = QLabel(
            "● 0 ONLINE"
        )

        self.online_count.setAlignment(
            Qt.AlignCenter
        )

        self.online_count.setMinimumWidth(
            180
        )

        self.online_count.setMinimumHeight(
            58
        )

        self.online_count.setStyleSheet(
            """
            QLabel {
                background-color: #061711;
                border: 1px solid #087a55;
                border-radius: 10px;
                color: #00e69a;
                font-weight: 700;
                padding: 6px 14px;
            }
            """
        )

        header_layout.addWidget(
            self.online_count
        )

        layout.addLayout(
            header_layout
        )

        # ======================================================
        # ONLINE PANEL
        # ======================================================

        online_panel = QFrame()

        online_panel.setObjectName(
            "onlinePanel"
        )

        online_panel.setStyleSheet(
            """
            QFrame#onlinePanel {
                background-color: #080811;
                border: 1px solid #28283f;
                border-radius: 14px;
            }
            """
        )

        online_panel_layout = QVBoxLayout(
            online_panel
        )

        online_panel_layout.setContentsMargins(
            18,
            18,
            18,
            18,
        )

        online_panel_layout.setSpacing(
            12
        )

        # ======================================================
        # PANEL TITLE
        # ======================================================

        online_title = QLabel(
            "CURRENTLY ONLINE"
        )

        online_title.setStyleSheet(
            """
            QLabel {
                background: transparent;
                color: #00e69a;
                font-size: 12px;
                font-weight: 800;
                letter-spacing: 2px;
            }
            """
        )

        online_panel_layout.addWidget(
            online_title
        )

        # ======================================================
        # ONLINE LIST
        # ======================================================

        self.online_list = QWidget()

        self.online_list.setStyleSheet(
            """
            QWidget {
                background-color: transparent;
            }
            """
        )

        self.online_layout = QVBoxLayout(
            self.online_list
        )

        self.online_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.online_layout.setSpacing(
            10
        )

        online_panel_layout.addWidget(
            self.online_list
        )

        layout.addWidget(
            online_panel
        )

        layout.addStretch()

        # ======================================================
        # SCROLL AREA
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

        scroll.setAutoFillBackground(
            True
        )

        # ------------------------------------------------------
        # Force viewport dark
        # ------------------------------------------------------

        scroll_palette = scroll.palette()

        scroll_palette.setColor(
            QPalette.Window,
            "#05050d",
        )

        scroll_palette.setColor(
            QPalette.Base,
            "#05050d",
        )

        scroll_palette.setColor(
            QPalette.AlternateBase,
            "#05050d",
        )

        scroll.setPalette(
            scroll_palette
        )

        scroll.viewport().setAutoFillBackground(
            True
        )

        viewport_palette = (
            scroll.viewport().palette()
        )

        viewport_palette.setColor(
            QPalette.Window,
            "#05050d",
        )

        viewport_palette.setColor(
            QPalette.Base,
            "#05050d",
        )

        scroll.viewport().setPalette(
            viewport_palette
        )

        scroll.setStyleSheet(
            """
            QScrollArea {
                background-color: #05050d;
                border: none;
            }

            QScrollArea > QWidget {
                background-color: #05050d;
            }

            QScrollArea > QWidget > QWidget {
                background-color: #05050d;
            }

            QScrollBar:vertical {
                background-color: #070711;
                width: 10px;
                margin: 0px;
                border: none;
            }

            QScrollBar::handle:vertical {
                background-color: #292943;
                border-radius: 5px;
                min-height: 40px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #713d9f;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                background: transparent;
                border: none;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background-color: #05050d;
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
    # LOAD ONLINE USERS
    # ==========================================================

    def load_online_users(self):

        clients = AdminAPI.get_clients(
            self.token
        )

        if clients is None:

            self.online_count.setText(
                "● CONNECTION ERROR"
            )

            self.online_count.setStyleSheet(
                """
                QLabel {
                    background-color: #210912;
                    border: 1px solid #9b2447;
                    border-radius: 10px;
                    color: #ff5578;
                    font-weight: 700;
                    padding: 6px 14px;
                }
                """
            )

            self.clear_online_list()

            self.show_empty(
                "Unable to load online users."
            )

            return

        # ======================================================
        # ONLY ONLINE CLIENTS
        # ======================================================

        online_clients = []

        for client in clients:

            if bool(
                client.get(
                    "is_online",
                    False,
                )
            ):

                online_clients.append(
                    client
                )

        # ======================================================
        # COUNT
        # ======================================================

        count = len(
            online_clients
        )

        self.online_count.setText(
            f"● {count} ONLINE"
        )

        self.online_count.setStyleSheet(
            """
            QLabel {
                background-color: #061711;
                border: 1px solid #087a55;
                border-radius: 10px;
                color: #00e69a;
                font-weight: 700;
                padding: 6px 14px;
            }
            """
        )

        # ======================================================
        # CLEAR
        # ======================================================

        self.clear_online_list()

        # ======================================================
        # EMPTY
        # ======================================================

        if not online_clients:

            self.show_empty(
                "No clients are currently online."
            )

            return

        # ======================================================
        # ADD ROWS
        # ======================================================

        for client in online_clients:

            self.add_online_row(
                client
            )

        self.online_layout.addStretch()

    # ==========================================================
    # CLEAR
    # ==========================================================

    def clear_online_list(self):

        while self.online_layout.count():

            item = self.online_layout.takeAt(
                0
            )

            widget = item.widget()

            if widget:

                widget.deleteLater()

    # ==========================================================
    # EMPTY
    # ==========================================================

    def show_empty(
        self,
        message: str,
    ):

        empty = QLabel(
            message
        )

        empty.setAlignment(
            Qt.AlignCenter
        )

        empty.setMinimumHeight(
            180
        )

        empty.setStyleSheet(
            """
            QLabel {
                background: transparent;
                color: #777790;
                border: none;
                font-size: 13px;
            }
            """
        )

        self.online_layout.addWidget(
            empty
        )

    # ==========================================================
    # ONLINE ROW
    # ==========================================================

    def add_online_row(
        self,
        client: dict,
    ):

        row = QFrame()

        row.setObjectName(
            "onlineRow"
        )

        row.setMinimumHeight(
            90
        )

        row.setStyleSheet(
            """
            QFrame#onlineRow {
                background-color: #0a0a14;
                border: 1px solid #00a978;
                border-radius: 11px;
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
            14
        )

        # ======================================================
        # CLIENT INFO
        # ======================================================

        info_box = QVBoxLayout()

        info_box.setSpacing(
            5
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

        name_label = QLabel(
            str(name)
        )

        name_label.setStyleSheet(
            """
            QLabel {
                background: transparent;
                color: #ffffff;
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
                background: transparent;
                color: #777790;
                font-size: 11px;
                border: none;
            }
            """
        )

        info_box.addWidget(
            name_label
        )

        info_box.addWidget(
            email_label
        )

        row_layout.addLayout(
            info_box,
            1,
        )

        # ======================================================
        # ONLINE STATUS
        # ======================================================

        status_label = QLabel(
            "● ONLINE"
        )

        status_label.setAlignment(
            Qt.AlignCenter
        )

        status_label.setMinimumWidth(
            100
        )

        status_label.setMinimumHeight(
            42
        )

        status_label.setStyleSheet(
            """
            QLabel {
                background-color: #063d28;
                border: 1px solid #008f61;
                border-radius: 7px;
                color: #00e69a;
                font-size: 10px;
                font-weight: 800;
                padding: 5px 10px;
            }
            """
        )

        row_layout.addWidget(
            status_label
        )

        # ======================================================
        # MT5 LOGIN
        # ======================================================

        mt5_login = client.get(
            "mt5_login"
        )

        self.add_data_column(
            row_layout,
            "MT5 LOGIN",
            (
                str(mt5_login)
                if mt5_login not in (
                    None,
                    "",
                )
                else "-"
            ),
        )

        # ======================================================
        # SERVER / BROKER
        # ======================================================

        mt5_server = client.get(
            "mt5_server"
        )

        broker = client.get(
            "broker"
        )

        server_value = (
            mt5_server
            or broker
            or "-"
        )

        self.add_data_column(
            row_layout,
            "SERVER",
            str(server_value),
        )

        # ======================================================
        # BALANCE
        # ======================================================

        balance = client.get(
            "balance"
        )

        self.add_data_column(
            row_layout,
            "BALANCE",
            self.format_money(
                balance
            ),
            value_color="#00e69a",
        )

        # ======================================================
        # EQUITY
        # ======================================================

        equity = client.get(
            "equity"
        )

        self.add_data_column(
            row_layout,
            "EQUITY",
            self.format_money(
                equity
            ),
            value_color="#67a1ff",
        )

        # ======================================================
        # LAST SEEN
        # ======================================================

        last_seen = client.get(
            "last_seen"
        )

        self.add_data_column(
            row_layout,
            "LAST SEEN",
            self.format_last_seen(
                last_seen
            ),
            value_font_size=9,
        )

        self.online_layout.addWidget(
            row
        )

    # ==========================================================
    # DATA COLUMN
    # ==========================================================

    @staticmethod
    def add_data_column(
        parent_layout,
        title: str,
        value: str,
        value_color: str = "#f5f5f7",
        value_font_size: int = 11,
    ):

        box = QVBoxLayout()

        box.setSpacing(
            5
        )

        title_label = QLabel(
            title
        )

        title_label.setStyleSheet(
            """
            QLabel {
                background: transparent;
                color: #777790;
                font-size: 9px;
                font-weight: 700;
                border: none;
            }
            """
        )

        value_label = QLabel(
            value
        )

        value_label.setStyleSheet(
            f"""
            QLabel {{
                background: transparent;
                color: {value_color};
                font-size: {value_font_size}px;
                font-weight: 700;
                border: none;
            }}
            """
        )

        value_label.setAlignment(
            Qt.AlignLeft
            | Qt.AlignVCenter
        )

        box.addWidget(
            title_label
        )

        box.addWidget(
            value_label
        )

        parent_layout.addLayout(
            box
        )

    # ==========================================================
    # MONEY
    # ==========================================================

    @staticmethod
    def format_money(
        value,
    ):

        if value is None:
            return "-"

        try:

            return (
                f"${float(value):,.2f}"
            )

        except (
            TypeError,
            ValueError,
        ):

            return str(
                value
            )

    # ==========================================================
    # LAST SEEN
    # ==========================================================

    @staticmethod
    def format_last_seen(
        value,
    ):

        if not value:
            return "-"

        try:

            # --------------------------------------------------
            # datetime object
            # --------------------------------------------------

            if isinstance(
                value,
                datetime,
            ):

                dt = value

            # --------------------------------------------------
            # string
            # --------------------------------------------------

            else:

                raw = str(
                    value
                ).strip()

                if raw.endswith(
                    "Z"
                ):

                    raw = (
                        raw[:-1]
                        + "+00:00"
                    )

                dt = datetime.fromisoformat(
                    raw
                )

            # --------------------------------------------------
            # Missing timezone = UTC
            # --------------------------------------------------

            if dt.tzinfo is None:

                dt = dt.replace(
                    tzinfo=timezone.utc
                )

            # --------------------------------------------------
            # UTC → Sri Lanka
            # --------------------------------------------------

            sri_lanka = timezone(
                timedelta(
                    hours=5,
                    minutes=30,
                )
            )

            dt = dt.astimezone(
                sri_lanka
            )

            return dt.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        except (
            TypeError,
            ValueError,
            OverflowError,
        ):

            return str(
                value
            )

    # ==========================================================
    # CLOSE
    # ==========================================================

    def closeEvent(
        self,
        event,
    ):

        if hasattr(
            self,
            "refresh_timer",
        ):

            self.refresh_timer.stop()

        event.accept()