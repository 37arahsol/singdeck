import asyncio
import websockets
import json
import pyautogui
import pyperclip
import socket

zeroconf_instance = None
server_instance = None

# Обработчик входящих сообщений
async def process_message(data, websocket):
    if data["type"] == "cursor":
        x = data["x"]
        y = data["y"]
        pyautogui.moveTo(x, y)
        # Отправляем текущую позицию курсора обратно клиенту
        x_local, y_local = pyautogui.position()
        message = {"type": "cursor", "x": x_local, "y": y_local}
        await websocket.send(json.dumps(message))
    elif data["type"] == "clipboard":
        clipboard_data = data["content"]
        pyperclip.copy(clipboard_data)
        # Отправляем содержимое буфера обмена обратно клиенту
        message = {"type": "clipboard", "content": pyperclip.paste()}
        await websocket.send(json.dumps(message))
    # Добавьте другие типы сообщений по мере необходимости

# Функция обработки соединений
async def handler(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        await process_message(data, websocket)

# Запуск сервера
async def start_server(app):
    global zeroconf_instance, server_instance
    host = '0.0.0.0'
    port = 8765

    # Если не используем mDNS, эти строки можно убрать
    # desc = {'path': '/'}
    # info = ServiceInfo(
    #     "_http._tcp.local.",
    #     "SyncServer._http._tcp.local.",
    #     addresses=[socket.inet_aton(socket.gethostbyname(socket.gethostname()))],
    #     port=port,
    #     properties=desc,
    #     server="SyncServer.local."
    # )
    # zeroconf_instance = Zeroconf()
    # zeroconf_instance.register_service(info)

    async def run_server():
        global server_instance
        server_instance = await websockets.serve(handler, host, port)
        print(f"Server started on {host}:{port}")
        app.set_status("Сервер активирован. Ждем подключение парного устройства...")
        await server_instance.wait_closed()

    await run_server()

# Запуск клиента
async def start_client(app, host='localhost', port=8765):
    uri = f"ws://{host}:{port}"
    try:
        async with websockets.connect(uri) as websocket:
            app.set_status("Подключено!")
            while True:
                # Отправляем текущую позицию курсора
                x, y = pyautogui.position()
                message = {"type": "cursor", "x": x, "y": y}
                await websocket.send(json.dumps(message))
                # Получаем данные от сервера
                response = await websocket.recv()
                data = json.loads(response)
                if data["type"] == "cursor":
                    pyautogui.moveTo(data["x"], data["y"])
                elif data["type"] == "clipboard":
                    pyperclip.copy(data["content"])
    except Exception as e:
        print(f"Не удалось подключиться к серверу: {e}")
        app.set_status("Ошибка подключения.")

def stop_all():
    global zeroconf_instance, server_instance
    if zeroconf_instance:
        zeroconf_instance.close()
        print("Zeroconf instance closed")
    if server_instance:
        server_instance.close()
        print("Server instance closed")
