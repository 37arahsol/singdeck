import asyncio
from network import start_server, start_client, stop_all
from gui import MainWindow, ModeSelectionWindow
from PyQt5 import QtWidgets
import sys
import threading
import signal

class App(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.mode_selection_window = ModeSelectionWindow()
        self.main_window = MainWindow()

        self.mode_selection_window.server_button.clicked.connect(self.start_server_mode)
        self.mode_selection_window.client_button.clicked.connect(self.start_client_mode)

        self.mode_selection_window.show()

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        print("Signal handler called with signal:", signum)
        self.cleanup()
        QtWidgets.QApplication.quit()

    def start_server_mode(self):
        threading.Thread(target=start_server, args=(self.main_window,)).start()
        self.mode_selection_window.hide()
        self.main_window.show()

    def start_client_mode(self):
        threading.Thread(target=asyncio.run, args=(start_client(self.main_window),)).start()
        self.mode_selection_window.hide()
        self.main_window.show()

    def cleanup(self):
        print("Cleaning up before exit...")
        stop_all()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
