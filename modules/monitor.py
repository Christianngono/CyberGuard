import psutil
from rich.console import Console
from rich.table import Table

from core.logger import logger
from core.utils import print_section, bytes_to_human

console = Console()


def _get_cpu_info():
    return {
        "percent": psutil.cpu_percent(interval=1),
        "cores": psutil.cpu_count(logical=True),
    }


def _get_memory_info():
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "used": mem.used,
        "percent": mem.percent,
    }


def _get_disk_info():
    disk = psutil.disk_usage("/")
    return {
        "total": disk.total,
        "used": disk.used,
        "percent": disk.percent,
    }


def _display_system_overview():
    cpu = _get_cpu_info()
    mem = _get_memory_info()
    disk = _get_disk_info()

    print_section("Vue d'ensemble du système")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Ressource")
    table.add_column("Utilisation")

    table.add_row("CPU", f"{cpu['percent']} % ({cpu['cores']} cœurs)")
    table.add_row("Mémoire", f"{mem['percent']} % ({bytes_to_human(mem['used'])} / {bytes_to_human(mem['total'])})")
    table.add_row("Disque", f"{disk['percent']} % ({bytes_to_human(disk['used'])} / {bytes_to_human(disk['total'])})")

    console.print(table)


def _display_top_processes(limit: int = 10):
    print_section(f"Top {limit} processus par utilisation CPU")
    processes = []
    for p in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            processes.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes.sort(key=lambda x: x["cpu_percent"], reverse=True)
    processes = processes[:limit]

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("PID", style="cyan")
    table.add_column("Nom")
    table.add_column("CPU %", justify="right")
    table.add_column("RAM %", justify="right")

    for proc in processes:
        table.add_row(
            str(proc["pid"]),
            proc["name"] or "N/A",
            f"{proc['cpu_percent']:.1f}",
            f"{proc['memory_percent']:.1f}",
        )

    console.print(table)


def run_system_monitor():
    """
    Point d'entrée appelé par main.py pour afficher un snapshot
    de l'état du système.
    """
    logger.info("Lancement du monitoring système (snapshot).")
    _display_system_overview()
    _display_top_processes()