# ✨ StarDust

**KI-Assistent für schnelle Antworten direkt unter Windows**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

StarDust läuft lokal auf Ihrem Rechner und liefert per Hotkey blitzschnell Antworten über die OpenAI-API.

## Inhalt

- [Features](#features)
- [Installation](#installation)
- [Verwendung](#verwendung)
- [Entwicklung](#entwicklung)
- [Mitwirken](#mitwirken)
- [Sicherheit](#sicherheit)

## Features

- 🚀 **Schnelle Antworten** durch OpenAI GPT-3.5
- ⌨️ **Einfacher Start** via `Ctrl+Alt+Y`
- 📝 **Texterkennung** aus der Zwischenablage
- 💻 **System-Tray-Icon** für schnellen Zugriff
- 🔒 **Lokale API-Key-Speicherung**
- 📊 **Umfangreiches Logging**

## Installation

1. Neueste Version im [Release-Bereich](https://github.com/yourusername/StarDust/releases) herunterladen
2. `StarDust.exe` starten
3. Beim ersten Start nach dem OpenAI-API-Key fragen lassen

## Verwendung

1. `Ctrl+Alt+Y` – Aufnahmemodus starten
2. Frage eingeben
3. `Ctrl+Alt+X` – Aufnahme beenden
4. Antwort landet in der Zwischenablage
5. Zwei Arten der Ausgabe:
   - **`Ctrl+V`** fügt alles direkt ein
   - **`Ctrl+Alt+V`** tippt die Antwort Zeichen für Zeichen

### Hotkeys

- `Ctrl+Alt+Y` – Start Aufnahme
- `Ctrl+Alt+X` – Ende Aufnahme
- `Ctrl+Alt+V` – Antwort einfügen
- `Win+Esc` – aktuellen Modus abbrechen

## Entwicklung

### Voraussetzungen

- Python ≥ 3.12
- OpenAI API-Key

### Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### EXE-Datei erstellen

```bash
pyinstaller StarDust.spec
```

## Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).

## Mitwirken

Pull Requests und Issues sind jederzeit willkommen!

## Sicherheit

- API-Key wird nur lokal gespeichert
- Keine Datenweitergabe an Dritte
- Kommunikation ausschließlich mit der OpenAI-API
