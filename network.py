import asyncio
import websockets
import json
import pyautogui
import pyperclip

# Функции для сервера и клиента

async def handler(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        await process_message(data, websocket)

async def client(uri):
    async with websockets.connect(uri) as websocket:
        # Отправка и получение сообщений
        while True:
            # Пример отправки данных курсора
            x, y = pyautogui.position()
            message = {"type": "cursor", "x": x, "y": y}
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            await process_message(json.loads(response), websocket)

# Запуск сервера
def start_server(host, port):
    return websockets.serve(handler, host, port)

# Запуск клиента
def start_client(host, port):
    uri = f"ws://{host}:{port}"
    asyncio.get_event_loop().run_until_complete(client(uri))

async def process_message(data, websocket):
    if data["type"] == "cursor":
        x = data["x"]
        y = data["y"]
        pyautogui.moveTo(x, y)
    elif data["type"] == "clipboard":
        clipboard_data = data["content"]
        pyperclip.copy(clipboard_data)
    # Добавьте другие типы сообщений по мере необходимости

