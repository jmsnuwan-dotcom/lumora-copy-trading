from PySide6.QtWidgets import QApplication

from client.ui.windows.login_window import LoginWindow


def run():

    print("STEP 1")

    app = QApplication([])

    print("STEP 2")

    login_window = LoginWindow()

    print("STEP 3")

    login_window.show()

    print("STEP 4")

    app.exec()

    print("STEP 5")

    return login_window.token