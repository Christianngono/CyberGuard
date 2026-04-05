import time
import psutil
from rich.live import Live
from rich.table import Table
from rich.panel import Panel

from core.utils import bytes_to_human
from core.logger import logger


def _build_dashboard():
    table = Table(title="CyberGuard - Dashboard Temps Réel", expand=True)

    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    table.add_column("Ressource", style="cyan", justify="left")
    table.add_column("Valeur", style="green", justify="right")

    table.add_row("CPU", f"{cpu} %")
    table.add_row("RAM", f"{mem.percent} % ({bytes_to_human(mem.used)} / {bytes_to_human(mem.total)})")
    table.add_row("Disque", f"{disk.percent} % ({bytes_to_human(disk.used)} / {bytes_to_human(disk.total)})")

    return Panel(table, border_style="cyan")


def start_terminal_dashboard(refresh_rate: float = 1.0):
    """
    Dashboard terminal en temps réel.
    """
    logger.info("Démarrage du dashboard terminal.")

    with Live(refresh_per_second=4) as live:
        while True:
            live.update(_build_dashboard())
            time.sleep(refresh_rate)