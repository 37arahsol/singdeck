from PyQt5 import QtWidgets, QtCore
import asyncio
import sys
from network import start_client, stop_all

class ModeSelectionWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Выбор режима')
        self.setGeometry(100, 100, 400, 300)

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-size: 16px;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: #ffffff;
                border-radius: 10px;
                padding: 10px;
                border: 1px solid #5c5c5c;
                transition: all 0.3s;
            }
            QPushButton:hover {
                background-color: #4c4c4c;
            }
            QPushButton:pressed {
                background-color: #2b2b2b;
                border: 1px solid #4c4c4c;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border-radius: 5px;
                padding: 5px;
                border: 1px solid #5c5c5c;
            }
            QLabel {
                font-weight: bold;
            }
        """)

        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel('Выберите режим работы:')
        layout.addWidget(self.label)

        self.server_button = QtWidgets.QPushButton('Запустить сервер')
        layout.addWidget(self.server_button)

        self.client_button = QtWidgets.QPushButton('Подключиться к серверу')
        layout.addWidget(self.client_button)

        layout.setSpacing(20)  # Пространство между элементами
        layout.setContentsMargins(20, 20, 20, 20)  # Внешние отступы

        self.setLayout(layout)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.destroyed.connect(self.cleanup)

    def closeEvent(self, event):
        self.cleanup()
        event.accept()

    def cleanup(self):
        print("Closing application...")
        stop_all()
        QtWidgets.QApplication.instance().quit()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dual Monitor Sync')
        self.setGeometry(100, 100, 400, 300)

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-size: 16px;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: #ffffff;
                border-radius: 10px;
                padding: 10px;
                border: 1px solid #5c5c5c;
                transition: all 0.3s;
            }
            QPushButton:hover {
                background-color: #4c4c4c;
            }
            QPushButton:pressed {
                background-color: #2b2b2b;
                border: 1px solid #4c4c4c;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border-radius: 5px;
                padding: 5px;
                border: 1px solid #5c5c5c;
            }
            QLabel {
                font-weight: bold;
            }
        """)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QtWidgets.QVBoxLayout()

        host_layout = QtWidgets.QHBoxLayout()
        self.host_label = QtWidgets.QLabel('IP-адрес партнера:')
        self.host_input = QtWidgets.QLineEdit()
        host_layout.addWidget(self.host_label)
        host_layout.addWidget(self.host_input)
        layout.addLayout(host_layout)

        port_layout = QtWidgets.QHBoxLayout()
        self.port_label = QtWidgets.QLabel('Порт:')
        self.port_input = QtWidgets.QLineEdit()
        self.port_input.setText('8765')
        port_layout.addWidget(self.port_label)
        port_layout.addWidget(self.port_input)
        layout.addLayout(port_layout)

        self.start_button = QtWidgets.QPushButton('Подключиться')
        self.start_button.clicked.connect(self.start_connection)
        layout.addWidget(self.start_button)

        self.status_label = QtWidgets.QLabel('')
        layout.addWidget(self.status_label)

        layout.setSpacing(20)  # Пространство между элементами
        layout.setContentsMargins(20, 20, 20, 20)  # Внешние отступы

        central_widget.setLayout(layout)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.destroyed.connect(self.cleanup)

    def start_connection(self):
        host = self.host_input.text()
        port = int(self.port_input.text())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_client(host, port))
        self.set_status("Подключено!")

    def set_status(self, status):
        self.status_label.setText(status)

    def closeEvent(self, event):
        self.cleanup()
        event.accept()

    def cleanup(self):
        print("Closing application...")
        stop_all()
        QtWidgets.QApplication.instance().quit()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mode_selection_window = ModeSelectionWindow()
    main_window = MainWindow()

    mode_selection_window.server_button.clicked.connect(main_window.show)
    mode_selection_window.client_button.clicked.connect(main_window.show)

    mode_selection_window.show()
    sys.exit(app.exec_())
