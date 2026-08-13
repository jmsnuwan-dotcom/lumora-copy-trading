from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QWidget


class ScrollPage(QScrollArea):

    def __init__(
        self,
        page: QWidget,
        parent=None,
    ):
        super().__init__(parent)

        self.setWidgetResizable(True)

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        self.setWidget(page)