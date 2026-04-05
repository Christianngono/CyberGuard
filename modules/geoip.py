from rich.console import Console

from core.config import Config
from core.logger import logger

try:
    import geoip2.database
except ImportError:
    geoip2 = None

console = Console()


def lookup_ip(ip: str):
    """
    Géolocalise une IP via GeoIP2 si la base est disponible.
    """
    if geoip2 is None:
        console.print("[red]Le module geoip2 n'est pas installé.[/red]")
        logger.error("geoip2 non disponible.")
        return

    try:
        reader = geoip2.database.Reader(Config.GEOIP_DB_PATH)
    except FileNotFoundError:
        console.print(f"[red]Base GeoIP introuvable : {Config.GEOIP_DB_PATH}[/red]")
        logger.error(f"Base GeoIP introuvable : {Config.GEOIP_DB_PATH}")
        return
    except Exception as e:
        console.print(f"[red]Erreur lors de l'ouverture de la base GeoIP : {e}[/red]")
        logger.error(f"Erreur GeoIP : {e}")
        return

    try:
        response = reader.city(ip)
        console.print(f"[bold cyan]Résultats GeoIP pour {ip}[/bold cyan]")
        console.print(f"Pays : {response.country.name} ({response.country.iso_code})")
        console.print(f"Région : {response.subdivisions.most_specific.name}")
        console.print(f"Ville : {response.city.name}")
        console.print(f"Latitude : {response.location.latitude}")
        console.print(f"Longitude : {response.location.longitude}")
        logger.info(f"GeoIP {ip} : {response.country.name} / {response.city.name}")
    except Exception as e:
        console.print(f"[red]Impossible de géolocaliser {ip} : {e}[/red]")
        logger.error(f"Erreur GeoIP pour {ip} : {e}")
    finally:
        reader.close()