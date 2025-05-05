# DSGVO-Datenlöschtool

Ein selbstgehostetes Tool zum Versenden von DSGVO-Datenlöschanfragen an Datenhändler per E-Mail.

![Screenshot](preview.png)

## ✅ Funktionen
- DSGVO-konformes Anfrageformular über Web-Oberfläche (FastAPI + TailwindCSS)
- Automatischer E-Mail-Versand mit Gmail (über App-Passwort)
- PDF-Generierung der Anfragen mit direktem Download
- Logging aller versendeten Anfragen
- Datenhändler frei definierbar über `data_brokers.json`
- Automatisierte tägliche Backups als ZIP-Dateien

---

## 🚀 Schnellstart

### Voraussetzungen
- Docker & Docker Compose installiert
- Gmail-Konto mit aktivierter 2-Faktor-Authentifizierung
- App-Passwort über [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

### Installation
```bash
git clone https://github.com/dein-benutzername/dsgvo-tool.git
cd dsgvo-tool
chmod +x setup.sh
./setup.sh
```

Die Anwendung läuft anschließend unter: [http://localhost:8000](http://localhost:8000)

---

## 🔧 Konfiguration
Die Datei `docker-compose.yml` enthält folgende Umgebungsvariablen:
```yaml
SMTP_SERVER: smtp.gmail.com
SMTP_PORT: 587
SMTP_USERNAME: dein@gmail.com
SMTP_PASSWORD: <App-Passwort>
EMAIL_FROM: dein@gmail.com
EMAIL_SUBJECT: "DSGVO-Datenlöschanfrage"
```

Die Liste der Datenhändler wird in `data_brokers.json` gepflegt:
```json
[
  { "name": "Acxiom", "email": "privacy@acxiom.com" },
  { "name": "Oracle", "email": "privacy_emea@oracle.com" }
]
```

---

## 📦 Backup & Logging
- Tägliches Backup um 2:00 Uhr via `cron` in ZIP-Dateien
- Logs der versendeten Anfragen: `logs/sent_requests.log`
- PDF-Ausgaben in `pdf/`

---

## 🧪 Technologien
- Python 3.11
- FastAPI
- Jinja2 + TailwindCSS
- WeasyPrint (für PDF)
- Docker & Docker Compose

---

## 🤝 Mitwirken
Pull Requests und Feedback sind willkommen! Stelle sicher, dass du alle Änderungen getestet hast.

---

## 📜 Lizenz
MIT License – frei zur privaten und gewerblichen Nutzung.

---

> Erstellt von [Dein Name oder GitHub-Handle]
