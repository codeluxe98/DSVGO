# DSGVO-Datenlöschtool

Dieses Projekt enthält ein erweitertes Beispiel einer FastAPI-Anwendung. Nutzende können sich registrieren, anmelden und eine DSGVO-Datenlöschanfrage stellen. Alle Broker aus der Datenbank werden benachrichtigt und es wird ein PDF erzeugt, das heruntergeladen werden kann. Aktionen werden protokolliert und ein Admin-Bereich ermöglicht die Verwaltung der Nutzenden.

## ✅ Funktionen
- Registrierung und Login
- Formular für Datenlöschanfragen
- Händler werden aus einer Datenbank geladen
- PDF mit benachrichtigten Händlern
- Admin-Panel zur Benutzerverwaltung

## 🚀 Schnellstart
```bash
docker compose up --build
```
Die Anwendung ist danach unter [http://localhost:8000](http://localhost:8000) erreichbar. Mit `DATABASE_URL` kann auch eine MySQL-Datenbank genutzt werden (siehe `docker-compose.yml`).
