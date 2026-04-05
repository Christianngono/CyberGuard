import shutil
import socket
import subprocess
from rich.console import Console
from rich.table import Table

from core.logger import logger
from core.utils import print_section

console = Console()


def _nmap_available() -> bool:
    return shutil.which("nmap") is not None


def _run_nmap_scan(target: str = "localhost", ports: str = "1-1024"):
    """
    Lance un scan nmap si disponible.
    """
    try:
        cmd = ["nmap", "-sV", "-p", ports, target]
        logger.info(f"Lancement du scan nmap : {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        console.print(result.stdout)
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution de nmap : {e}")
        console.print(f"[red]Erreur lors de l'exécution de nmap : {e}[/red]")


def _basic_port_scan(host: str = "127.0.0.1", ports=range(1, 1025)):
    """
    Scan basique de ports via socket (fallback si nmap absent).
    """
    print_section("Scan basique des ports (fallback)")
    table = Table(title=f"Ports ouverts sur {host}")
    table.add_column("Port", style="cyan")
    table.add_column("Statut", style="green")

    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.2)
            try:
                result = s.connect_ex((host, port))
                if result == 0:
                    table.add_row(str(port), "OUVERT")
            except Exception:
                continue

    console.print(table)


def run_network_scan(target: str = "localhost", ports: str = "1-1024"):
    """
    Point d'entrée appelé par main.py pour lancer un scan réseau.
    Utilise nmap si disponible, sinon un scan basique.
    """
    print_section("Scan réseau")
    if _nmap_available():
        console.print("[green]nmap détecté, utilisation de nmap.[/green]")
        _run_nmap_scan(target=target, ports=ports)
    else:
        console.print("[yellow]nmap non disponible, utilisation d'un scan basique.[/yellow]")
        _basic_port_scan(host=target, ports=range(1, 1025))