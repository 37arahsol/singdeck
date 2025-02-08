import asyncio
import websockets
import json
import pyautogui
import pyperclip
import socket
from zeroconf import ServiceInfo, Zeroconf, ServiceBrowser

zeroconf_instance = None
server_instance = None

# Обработчик входящих сообщений
async def process_message(data):
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
        await process_message(data)

# Запуск сервера
async def start_server(app):
    global zeroconf_instance, server_instance
    host = '0.0.0.0'
    port = 8765

    # Регистрируем mDNS сервис
    desc = {'path': '/'}
    info = ServiceInfo(
        "_http._tcp.local.",
        "SyncServer._http._tcp.local.",
        addresses=[socket.inet_aton(socket.gethostbyname(socket.gethostname()))],
        port=port,
        properties=desc,
        server="SyncServer.local."
    )
    zeroconf_instance = Zeroconf()
    zeroconf_instance.register_service(info)

    async def run_server():
        global server_instance
        server_instance = await websockets.serve(handler, host, port)
        print(f"Server started on {host}:{port}")
        app.status_label.config(text="Сервер активирован. Ждем подключение парного устройства...")
        await server_instance.wait_closed()

    loop = asyncio.get_event_loop()
    await loop.create_task(run_server())

# Обработчик событий обнаружения сервера
class MyListener:
    def __init__(self):
        self.server_info = None

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info and info.name == "SyncServer._http._tcp.local.":
            self.server_info = info

# Запуск клиента
async def start_client(app):
    zeroconf_instance = Zeroconf()
    listener = MyListener()
    browser = ServiceBrowser(zeroconf_instance, "_http._tcp.local.", listener)

    # Ожидаем обнаружения сервера
    while listener.server_info is None:
        await asyncio.sleep(1)

    info = listener.server_info
    uri = f"ws://{socket.inet_ntoa(info.addresses[0])}:{info.port}"
    async with websockets.connect(uri) as websocket:
        app.status_label.config(text="Подключено!")
        while True:
            x, y = pyautogui.position()
            message = {"type": "cursor", "x": x, "y": y}
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            data = json.loads(response)
            if data["type"] == "cursor":
                pyautogui.moveTo(data["x"], data["y"])
            elif data["type"] == "clipboard":
                pyperclip.copy(data["content"])

def stop_all():
    global zeroconf_instance, server_instance
    if zeroconf_instance:
        zeroconf_instance.close()
        print("Zeroconf instance closed")
    if server_instance:
        server_instance.close()
        print("Server instance closed")
