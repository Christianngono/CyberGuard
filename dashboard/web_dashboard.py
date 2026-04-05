import psutil
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocket
from fastapi.staticfiles import StaticFiles

from core.utils import bytes_to_human
from core.logger import logger

app = FastAPI(title="CyberGuard Web Dashboard")

# Servir les fichiers statiques
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("dashboard/templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client WebSocket connecté.")

    try:
        while True:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            data = {
                "cpu": cpu,
                "ram_percent": mem.percent,
                "ram_used": bytes_to_human(mem.used),
                "ram_total": bytes_to_human(mem.total),
                "disk_percent": disk.percent,
                "disk_used": bytes_to_human(disk.used),
                "disk_total": bytes_to_human(disk.total),
            }

            await websocket.send_json(data)
    except Exception:
        logger.info("Client WebSocket déconnecté.")