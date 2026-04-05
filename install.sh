#!/usr/bin/env bash
set -e

echo "[*] Création du venv..."
python3 -m venv venv

echo "[*] Activation du venv..."
# Pour bash/zsh
source venv/bin/activate

echo "[*] Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[*] Création des dossiers data/..."
mkdir -p data/logs data/geoip data/rules

echo "[*] Copie du .env.example vers .env (si absent)..."
if [ ! -f ".env" ]; then
  cp .env.example .env
fi

echo "[*] Fichier de règles par défaut..."
if [ ! -f "data/rules/detection_rules.json" ]; then
  cat > data/rules/detection_rules.json << 'EOF'
[
  {
    "id": "RULE_001",
    "type": "process_name",
    "pattern": "ncat",
    "severity": "high",
    "description": "Outil de tunneling détecté"
  }
]
EOF
fi

echo "[*] Installation terminée."
echo "Active le venv avec : source venv/bin/activate"
echo "Puis lance : python main.py --help"