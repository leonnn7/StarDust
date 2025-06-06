# StarDust - KI-Assistent für schnelle Antworten

StarDust ist ein leistungsstarker KI-Assistent, der direkt in Ihrem System läuft und Ihnen hilft, schnell Antworten auf Ihre Fragen zu bekommen. Mit einem einfachen Hotkey können Sie den Assistenten aktivieren und Ihre Fragen stellen.

## Features

- 🚀 Schnelle Antworten durch OpenAI GPT-3.5
- ⌨️ Einfache Aktivierung mit Hotkey (Ctrl+Alt+Y)
- 📝 Automatische Texterkennung
- 💻 System-Tray-Integration
- 🔒 Lokale API-Key-Speicherung
- 📊 Detailliertes Logging

## Installation

1. Laden Sie die neueste Version von StarDust aus dem [Releases](https://github.com/yourusername/StarDust/releases) Bereich herunter
2. Führen Sie die `StarDust.exe` aus
3. Bei der ersten Ausführung werden Sie nach Ihrem OpenAI API-Key gefragt

## Verwendung

1. Drücken Sie `Ctrl+Alt+Y` um den Aufnahmemodus zu starten
2. Geben Sie Ihre Frage ein
3. Drücken Sie `Ctrl+Alt+X` um die Aufnahme zu beenden
4. Die Antwort wird automatisch in die Zwischenablage kopiert
5. Sie haben zwei Möglichkeiten, die Antwort einzufügen:
   - **Mit `Ctrl+V`**: Die komplette Antwort wird sofort eingefügt (Paste)
   - **Mit `Ctrl+Alt+V`**: Die Antwort wird Zeichen für Zeichen wie getippt eingefügt (z.B. für Programme, die kein direktes Einfügen erlauben)

### Hotkeys

- `Ctrl+Alt+Y`: Aufnahmemodus starten
- `Ctrl+Alt+X`: Aufnahmemodus beenden
- `Ctrl+Alt+V`: Antwort einfügen
- `Win+Esc`: Aktuellen Modus abbrechen

## Entwicklung

### Voraussetzungen

- Python 3.12 oder höher
- OpenAI API-Key

### Installation der Abhängigkeiten

```bash
pip install -r requirements.txt
```

### Erstellen der EXE-Datei

```bash
pyinstaller StarDust.spec
```

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.

## Mitwirken

Beiträge sind willkommen! Bitte erstellen Sie einen Pull Request oder öffnen Sie ein Issue für Verbesserungsvorschläge.

## Sicherheit

- Der API-Key wird lokal in der AppData gespeichert
- Keine Daten werden an Dritte gesendet
- Alle Kommunikation erfolgt direkt mit der OpenAI API 