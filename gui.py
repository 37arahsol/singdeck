from PyQt5 import QtWidgets, QtCore
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dual Monitor Sync')
        self.setGeometry(100, 100, 300, 200)

        # Элементы интерфейса
        self.host_label = QtWidgets.QLabel('IP-адрес партнера:', self)
        self.host_label.move(20, 20)

        self.host_input = QtWidgets.QLineEdit(self)
        self.host_input.move(20, 50)
        self.host_input.resize(250, 20)

        self.port_label = QtWidgets.QLabel('Порт:', self)
        self.port_label.move(20, 80)

        self.port_input = QtWidgets.QLineEdit(self)
        self.port_input.move(20, 110)
        self.port_input.resize(250, 20)
        self.port_input.setText('8765')

        self.start_button = QtWidgets.QPushButton('Подключиться', self)
        self.start_button.move(20, 150)
        self.start_button.clicked.connect(self.start_connection)

    def start_connection(self):
        host = self.host_input.text()
        port = int(self.port_input.text())
        # Инициализация сетевого соединения
        # network.start_client(host, port)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
