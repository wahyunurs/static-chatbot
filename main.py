# IMPORT
# Mengimport FastAPI, Endpoint Websocket, request HTTP
from fastapi import FastAPI, WebSocket, Request

# Respon mengembalikan HTML
from fastapi.responses import HTMLResponse

# Layanan file statis seperti css, js, dl
from fastapi.staticfiles import StaticFiles

# Template engine HTML Jinja2
from fastapi.templating import Jinja2Templates

# Akses file JSON
import json
# Mengelola path file
from pathlib import Path

# Memuat data Chatbot
# Inisisasi data chatbot dari path data.json
chatbot_data_path = Path("data.json")
# Membuka chatbot data path, with: file akan close otomatis jika sudah selesai, "r": mode read, as: disimpan dalam variabel
with chatbot_data_path.open("r") as file:
    # Menampilkan hasil load file json
    chatbot_data = json.load(file)

# Inisiasi instance dari FastAPI untuk endpoint dan rute
app = FastAPI()
# Menentukan directory dari file statis
app.mount("/static", StaticFiles(directory="static"), name="static")
# Inisiasi Jinja 2 Templates dari directorynya
template = Jinja2Templates(directory="templates")


# GET ENDPOINT HALAMAN INDEX
@app.get("/")
# Mengambil objek request yang akan diteruskan ke template
async def get(request: Request):
    # Mengembalikan hasil render template HTML
    return template.TemplateResponse(
        "index.html", {"request": request, "title": "Static-Chatbot"}
    )


# WEBSOCKETS ENDPOINT
@app.websocket("/ws")
# Method endpoint websocket dengan parameter WebScoket, async: key asinkron untuk memproses yang membutuhkan waktu load
async def websocket_endpoint(websocket: WebSocket):
    # Menunggu untuk menerima koneksi ke websocket
    await websocket.accept()
    # Loop
    while True:
        # Inisiasi data untuk Menunggu menerima chat teks
        data = await websocket.receive_text()
        # Inisiasi respon adalah memanggil method get_chatbot_response dengan parameter data
        response = get_chatbot_response(data)
        # Menunggu untuk websocket mengirim pesan teks respon
        await websocket.send_text(response)

# Method mendapat respon dari chatbot dengan parameter string message, -> str: mengembalikan nilai berupa string
def get_chatbot_response(message: str) -> str:
    # Inisiasi mengubah pesan dari user dikonversi, lower(): ke lowercase atau huruf kecil semua
    message = message.lower()
    # Kondisi jika pesan dari data chatbot
    if message in chatbot_data["greetings"]:
        return chatbot_data["greetings"][message]
    elif message in chatbot_data["farewell"]:
        return chatbot_data["farewell"][message]
    else:
        return "I'm sorry, I don't understand that."
