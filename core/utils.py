import platform
import socket
import psutil
from rich.console import Console

console = Console()

def get_system_info():
    """
    Retourne des informations générales sur le système.
    """
    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "cpu_count": psutil.cpu_count(),
        "memory_total": psutil.virtual_memory().total,
    }


def print_section(title: str):
    """
    Affiche une section stylée dans le terminal.
    """
    console.rule(f"[bold cyan]{title}[/bold cyan]")


def bytes_to_human(n: int) -> str:
    """
    Convertit des bytes en format lisible (KB, MB, GB).
    """
    symbols = ("KB", "MB", "GB", "TB")
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10

    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return f"{value:.2f} {s}"

    return f"{n} B"