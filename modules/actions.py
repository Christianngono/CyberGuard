from rich.console import Console
from rich.table import Table

from core.logger import logger

console = Console()


def suggest_manual_actions(alerts: list):
    """
    Propose des actions MANUELLES à l'opérateur en fonction des alertes.
    ⚠️ Ne tue pas de processus, ne bloque pas d'IP automatiquement.
    """
    if not alerts:
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Règle")
    table.add_column("Processus")
    table.add_column("PID")
    table.add_column("Suggestion")

    for alert in alerts:
        suggestion = (
            "Vérifier le processus, analyser le binaire, "
            "évaluer la nécessité d'un kill manuel ou d'un blocage firewall."
        )
        table.add_row(
            alert.get("rule_id", "N/A"),
            alert.get("process", "N/A"),
            str(alert.get("pid", "N/A")),
            suggestion,
        )

        logger.info(
            f"Suggestion d'action manuelle pour PID {alert.get('pid')}, "
            f"processus {alert.get('process')}"
        )

    console.print(table)