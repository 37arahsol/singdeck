import asyncio
from network import start_server, start_client
from gui import MainWindow
from PyQt5 import QtWidgets
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Запуск сетевого взаимодействия в отдельном потоке
    loop = asyncio.get_event_loop()
    # Здесь можно выбрать, запускать сервер или клиент, в зависимости от настроек
    # Например, loop.run_until_complete(start_server('0.0.0.0', 8765))

    sys.exit(app.exec_())
