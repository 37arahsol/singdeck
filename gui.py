from PyQt5 import QtWidgets, QtCore
import asyncio
from network import stop_all, start_client  # Добавим импорт start_client

class ModeSelectionWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Выбор режима')
        self.setGeometry(100, 100, 400, 300)

        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel('Выберите режим работы:')
        layout.addWidget(self.label)

        self.server_button = QtWidgets.QPushButton('Запустить сервер')
        layout.addWidget(self.server_button)

        self.client_button = QtWidgets.QPushButton('Подключиться к серверу')
        layout.addWidget(self.client_button)

        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

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
        self.setGeometry(100, 100, 400, 200)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QtWidgets.QVBoxLayout()

        self.status_label = QtWidgets.QLabel('Статус: Ожидание действия...')
        layout.addWidget(self.status_label)

        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        central_widget.setLayout(layout)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.destroyed.connect(self.cleanup)

    def set_status(self, status):
        self.status_label.setText(f'Статус: {status}')

    def closeEvent(self, event):
        self.cleanup()
        event.accept()

    def cleanup(self):
        print("Closing application...")
        stop_all()
        QtWidgets.QApplication.instance().quit()
