#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CyberGuard - Main Entry Point
Orchestration du scanner, du monitoring, de la détection et des dashboards.
"""

import argparse
import sys
from rich.console import Console
from rich.panel import Panel

# Import des modules internes
from modules.scanner import run_network_scan
from modules.monitor import run_system_monitor
from modules.detection import run_detection_engine
from modules.geoip import lookup_ip
from dashboard.terminal_dashboard import start_terminal_dashboard

console = Console()


def banner():
    console.print(Panel.fit(
        "[bold cyan]🛡️ CYBERGUARD — Security Monitoring Framework[/bold cyan]\n"
        "[green]Surveillance système • Analyse réseau • Détection d’anomalies[/green]",
        border_style="cyan"
    ))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="CyberGuard — Outil de surveillance et d’analyse de sécurité."
    )

    parser.add_argument("--scan", action="store_true",
                        help="Effectuer un scan réseau (ports, services).")

    parser.add_argument("--monitor", action="store_true",
                        help="Surveiller le système (CPU, RAM, processus).")

    parser.add_argument("--detect", action="store_true",
                        help="Lancer le moteur de détection d’anomalies.")

    parser.add_argument("--geoip", type=str,
                        help="Géolocaliser une adresse IP.")

    parser.add_argument("--dashboard", action="store_true",
                        help="Afficher le dashboard terminal en temps réel.")

    return parser.parse_args()


def main():
    banner()
    args = parse_arguments()

    # Aucun argument → afficher aide
    if len(sys.argv) == 1:
        console.print("[yellow]Aucun argument fourni. Utilisez --help pour voir les options.[/yellow]")
        return

    # Scan réseau
    if args.scan:
        console.print("[bold cyan]🔍 Scan réseau en cours...[/bold cyan]")
        run_network_scan()

    # Monitoring système
    if args.monitor:
        console.print("[bold cyan]🖥️ Surveillance système...[/bold cyan]")
        run_system_monitor()

    # Détection d’anomalies
    if args.detect:
        console.print("[bold cyan]⚠️ Moteur de détection activé...[/bold cyan]")
        run_detection_engine()

    # Géolocalisation IP
    if args.geoip:
        console.print(f"[bold cyan]🌍 Recherche GeoIP pour {args.geoip}...[/bold cyan]")
        lookup_ip(args.geoip)

    # Dashboard terminal
    if args.dashboard:
        console.print("[bold cyan]📊 Dashboard en temps réel...[/bold cyan]")
        start_terminal_dashboard()


if __name__ == "__main__":
    main()