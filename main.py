import sys
from PyQt5 import QtWidgets
from gui import MainWindow, ModeSelectionWindow
from network import start_server, start_client, stop_all
import asyncio
from asyncqt import QEventLoop  # Нужно установить библиотеку asyncqt

class App(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.loop = QEventLoop(self)
        asyncio.set_event_loop(self.loop)

        self.mode_selection_window = ModeSelectionWindow()
        self.main_window = MainWindow()

        self.mode_selection_window.server_button.clicked.connect(self.start_server_mode)
        self.mode_selection_window.client_button.clicked.connect(self.start_client_mode)

        self.mode_selection_window.show()

        self.aboutToQuit.connect(self.cleanup)

    def start_server_mode(self):
        self.mode_selection_window.hide()
        self.main_window.show()
        asyncio.ensure_future(start_server(self.main_window))

    def start_client_mode(self):
        self.mode_selection_window.hide()
        self.main_window.show()
        asyncio.ensure_future(start_client(self.main_window))

    def cleanup(self):
        print("Cleaning up before exit...")
        stop_all()

if __name__ == '__main__':
    app = App(sys.argv)
    with app.loop:
        sys.exit(app.exec_())
