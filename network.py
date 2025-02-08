import asyncio
import websockets
import json
import pyautogui
import pyperclip
import socket
from zeroconf import ServiceInfo, Zeroconf, ServiceBrowser

zeroconf_instance = None
server_instance = None
loop = None

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
def start_server(main_window):
    global zeroconf_instance, server_instance, loop
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
        main_window.set_status("Сервер активирован. Ждем подключение парного устройства...")
        await server_instance.wait_closed()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_server())
    except asyncio.CancelledError:
        print("Event loop stopped")

# Обработчик событий обнаружения сервера
class MyListener:
    def __init__(self):
        self.server_info = None

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info and info.name == "SyncServer._http._tcp.local.":
            self.server_info = info

# Запуск клиента
async def start_client(main_window):
    global zeroconf_instance
    zeroconf_instance = Zeroconf()
    listener = MyListener()
    browser = ServiceBrowser(zeroconf_instance, "_http._tcp.local.", listener)

    # Ожидаем обнаружения сервера
    while listener.server_info is None:
        await asyncio.sleep(1)

    info = listener.server_info
    uri = f"ws://{socket.inet_ntoa(info.addresses[0])}:{info.port}"
    async with websockets.connect(uri) as websocket:
        main_window.set_status("Подключено!")
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
    global zeroconf_instance, server_instance, loop
    if zeroconf_instance:
        zeroconf_instance.close()
        print("Zeroconf instance closed")
    if server_instance:
        server_instance.close()
        print("Server instance closed")
    if loop:
        for task in asyncio.all_tasks(loop):
            task.cancel()
        loop.call_soon_threadsafe(loop.stop)
        print("Event loop stopped")
