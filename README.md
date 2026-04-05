# CyberGuard

**Surveillance système, analyse réseau et outils de cybersécurité en Python**

CyberGuard est un outil modulaire écrit en Python permettant de surveiller un système, analyser le réseau, détecter des comportements suspects et fournir des informations utiles pour renforcer la sécurité d’un poste ou d’un petit réseau.

Le projet est conçu pour être simple, extensible et pédagogique, tout en offrant des fonctionnalités réellement utiles pour l’analyse et la détection d’activités anormales.

---

## Fonctionnalités

### Analyse réseau
- Récupération d’informations réseau (interfaces, IP, passerelle, DNS)
- Scan basique de ports (optionnel si `nmap` est installé)
- Détection d’activités réseau suspectes (trafic anormal, ports ouverts inattendus)

### Surveillance système
- Utilisation CPU, RAM, disque
- Processus actifs
- Détection de processus suspects (patterns configurables)

### Géolocalisation IP (optionnel)
- Utilise **GeoIP2** pour localiser une adresse IP
- Affiche pays, ville, ASN (si base MaxMind fournie)

### Architecture modulaire
Chaque fonctionnalité est séparée dans un module :