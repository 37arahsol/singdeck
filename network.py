import asyncio
import websockets
import json
import pyautogui
import pyperclip
from zeroconf import ServiceInfo, Zeroconf, ServiceBrowser, ServiceListener
import socket

zeroconf = Zeroconf()
service_name = "_syncservice._tcp.local."
service_type = "_syncservice._tcp.local."
service_port = 8765

# Обработчик входящих сообщений
async def process_message(data, websocket):
    if data["type"] == "cursor":
        x = data["x"]
        y = data["y"]
        pyautogui.moveTo(x, y)
    elif data["type"] == "clipboard":
        clipboard_data = data["content"]
        pyperclip.copy(clipboard_data)
    # Добавьте другие типы сообщений по мере необходимости

# Функция обработки соединений
async def handler(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        await process_message(data, websocket)

# Запуск сервера
async def start_server(app):
    global zeroconf
    # Получаем IP-адрес хоста
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)

    desc = {'name': 'SyncServer'}
    info = ServiceInfo(
        service_type,
        f"SyncServer.{service_type}",
        addresses=[socket.inet_aton(host_ip)],
        port=service_port,
        properties=desc,
        server=f"{hostname}.local."
    )

    zeroconf.register_service(info)
    print("Сервис mDNS зарегистрирован")

    async def run_server():
        print(f"Сервер запущен на {host_ip}:{service_port}")
        app.set_status("Сервер активирован. Ожидаем подключение...")
        async with websockets.serve(handler, host_ip, service_port):
            await asyncio.Future()  # Блокируем функцию, чтобы сервер работал

    await run_server()

# Обработчик для обнаружения сервера
class ServerListener(ServiceListener):
    def __init__(self):
        self.server_info = None

    def remove_service(self, zeroconf, type, name):
        pass

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            self.server_info = info

    def update_service(self, zeroconf, type, name):
        pass

# Запуск клиента
async def start_client(app):
    global zeroconf
    listener = ServerListener()
    browser = ServiceBrowser(zeroconf, service_type, listener)

    app.set_status("Поиск сервера...")

    # Ожидание обнаружения сервера
    while listener.server_info is None:
        await asyncio.sleep(1)  # Изменяем на целое число

    info = listener.server_info
    addresses = info.addresses
    host_ip = socket.inet_ntoa(addresses[0])
    port = info.port

    uri = f"ws://{host_ip}:{port}"
    try:
        async with websockets.connect(uri) as websocket:
            app.set_status("Подключено к серверу!")
            while True:
                # Отправляем текущую позицию курсора
                x, y = pyautogui.position()
                message = {"type": "cursor", "x": x, "y": y}
                await websocket.send(json.dumps(message))
                await asyncio.sleep(0.1)  # Оставляем небольшую задержку
    except Exception as e:
        print(f"Не удалось подключиться к серверу: {e}")
        app.set_status("Ошибка подключения.")

def stop_all():
    global zeroconf
    zeroconf.close()
    print("Zeroconf instance closed")
