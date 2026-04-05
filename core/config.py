import os
from dotenv import load_dotenv

# Charger automatiquement les variables du fichier .env
load_dotenv()

class Config:
    """
    Configuration centrale de CyberGuard.
    Toutes les variables importantes sont centralisées ici.
    """

    # Chemin vers la base GeoIP
    GEOIP_DB_PATH = os.getenv("GEOIP_DB_PATH", "data/geoip/GeoLite2-City.mmdb")

    # Chemin vers le fichier de logs
    LOG_PATH = os.getenv("LOG_PATH", "data/logs/cyberguard.log")

    # Niveau de logs
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Chemin vers les règles IDS
    RULES_PATH = "data/rules/detection_rules.json"

    @staticmethod
    def ensure_directories():
        """
        Crée automatiquement les dossiers nécessaires si absents.
        """
        os.makedirs("data/logs", exist_ok=True)
        os.makedirs("data/geoip", exist_ok=True)
        os.makedirs("data/rules", exist_ok=True)