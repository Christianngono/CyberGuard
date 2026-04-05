#   CyberGuard - Makefile

PYTHON=python3
VENV=venv
ACTIVATE=. $(VENV)/bin/activate

#  Installation & Environnement


all: install

venv:
    $(PYTHON) -m venv $(VENV)

install: venv
    $(ACTIVATE) && pip install --upgrade pip
    $(ACTIVATE) && pip install -r requirements.txt
    @echo "[OK] Installation terminée."

update:
    $(ACTIVATE) && pip install --upgrade -r requirements.txt

freeze:
    $(ACTIVATE) && pip freeze > requirements.txt
    @echo "[OK] requirements.txt mis à jour."

#  Exécution des modules


run:
    $(ACTIVATE) && $(PYTHON) main.py --help

scan:
    $(ACTIVATE) && $(PYTHON) main.py --scan

monitor:
    $(ACTIVATE) && $(PYTHON) main.py --monitor

detect:
    $(ACTIVATE) && $(PYTHON) main.py --detect

geoip:
    $(ACTIVATE) && $(PYTHON) main.py --geoip 8.8.8.8

dashboard:
    $(ACTIVATE) && $(PYTHON) main.py --dashboard

#  Dashboard Web (stable)

web-dashboard:
    $(ACTIVATE) && uvicorn dashboard.web_dashboard:app --ws wsproto --reload

web-prod:
    $(ACTIVATE) && uvicorn dashboard.web_dashboard:app --ws wsproto --host 0.0.0.0 --port 8000

#  Nettoyage

clean:
    rm -rf __pycache__ */__pycache__ .pytest_cache
    rm -rf data/logs/*.log
    @echo "[OK] Nettoyage terminé."

clean-all: clean
    rm -rf $(VENV)
    @echo "[OK] Nettoyage complet (venv supprimé)."
