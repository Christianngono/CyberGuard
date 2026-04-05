import json
import psutil
from rich.console import Console
from rich.table import Table

from core.config import Config
from core.logger import logger
from core.utils import print_section

console = Console()


def _load_rules():
    """
    Charge les règles de détection depuis le fichier JSON.
    Format attendu :
    [
      {
        "id": "RULE_1",
        "type": "process_name",
        "pattern": "ncat",
        "severity": "high",
        "description": "Outil de tunneling détecté"
      }
    ]
    """
    try:
        with open(Config.RULES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Fichier de règles introuvable : {Config.RULES_PATH}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Erreur JSON dans {Config.RULES_PATH} : {e}")
        return []


def _check_process_rules(rules):
    alerts = []
    processes = []
    for p in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
        try:
            processes.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    for rule in rules:
        if rule.get("type") != "process_name":
            continue
        pattern = rule.get("pattern", "").lower()
        for proc in processes:
            name = (proc["name"] or "").lower()
            if pattern and pattern in name:
                alerts.append({
                    "rule_id": rule.get("id"),
                    "severity": rule.get("severity", "low"),
                    "description": rule.get("description", ""),
                    "pid": proc["pid"],
                    "process": proc["name"],
                })

    return alerts


def _display_alerts(alerts):
    if not alerts:
        console.print("[green]Aucune alerte détectée selon les règles actuelles.[/green]")
        return

    print_section("Alertes de détection")
    table = Table(show_header=True, header_style="bold red")
    table.add_column("Règle")
    table.add_column("Sévérité")
    table.add_column("Processus")
    table.add_column("PID")
    table.add_column("Description")

    for alert in alerts:
        table.add_row(
            alert["rule_id"] or "N/A",
            alert["severity"],
            alert["process"] or "N/A",
            str(alert["pid"]),
            alert["description"],
        )

    console.print(table)


def run_detection_engine():
    """
    Point d'entrée appelé par main.py pour lancer le moteur de détection.
    Analyse les processus selon les règles définies.
    """
    logger.info("Lancement du moteur de détection.")
    rules = _load_rules()
    if not rules:
        console.print("[yellow]Aucune règle de détection chargée.[/yellow]")
        return

    alerts = _check_process_rules(rules)
    for alert in alerts:
        logger.warning(
            f"Alerte : règle={alert['rule_id']} "
            f"sev={alert['severity']} proc={alert['process']} pid={alert['pid']}"
        )

    _display_alerts(alerts)