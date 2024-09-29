# CS2 Server Control

Dieses Projekt ermöglicht die Steuerung von CS2-Servern über eine Weboberfläche. Es verwendet Flask, Flask-Login und Shell-Skripte, um Server zu starten, zu stoppen und zu verwalten.

## Installation

1. Klone das Repository:
   ```bash
   git clone https://github.com/Egosar93/web_cs2server_manager.git
   ```
2. Navigiere in das Projektverzeichnis:
   ```bash
   cd web_cs2server_manager
   ```
3. Installiere die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

4. Starte die Flask-App:
   ```bash
   python app.py
   ```

5. Besuche die Weboberfläche unter `http://127.0.0.1:5000`.

## Funktionen

- Login-geschützte Serversteuerung
- Starten und Stoppen von CS2-Servern
- Auswahl von Spielmodus und Karte
- Mehrere Server verwalten

## Konfiguration

- Benutzername: `admin`
- Passwort: `password123`

## Abhängigkeiten

- Flask
- Flask-Login
