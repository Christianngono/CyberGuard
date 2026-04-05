from rich.console import Console
from rich.panel import Panel

from core.logger import logger

console = Console()


def alert_info(message: str):
    """
    Alerte d'information (non critique).
    """
    console.print(Panel.fit(f"[cyan]{message}[/cyan]", title="INFO", border_style="cyan"))
    logger.info(message)


def alert_warning(message: str):
    """
    Alerte de niveau avertissement.
    """
    console.print(Panel.fit(f"[yellow]{message}[/yellow]", title="AVERTISSEMENT", border_style="yellow"))
    logger.warning(message)


def alert_critical(message: str):
    """
    Alerte critique (à traiter manuellement).
    """
    console.print(Panel.fit(f"[red]{message}[/red]", title="CRITIQUE", border_style="red"))
    logger.error(message)