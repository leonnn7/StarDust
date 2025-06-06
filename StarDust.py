"""StarDust Hauptprogramm.

Dieser kleine Helfer lauscht auf Hotkeys, sendet eingegebene Fragen an die
OpenAI‑API und kopiert die Antwort direkt in die Zwischenablage. Die Datei
enthält das komplette Tray‑ und Hotkey‑Handling.
"""

import keyboard
import pyperclip
import openai
import logging
import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv, dotenv_values
import win32gui
import win32con
import win32api
import ctypes
import tkinter as tk
from tkinter import simpledialog
import pystray
from pystray import MenuItem as item
from PIL import Image

# AppData-Ordner für StarDust
APPDATA_DIR = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'StarDust')
os.makedirs(APPDATA_DIR, exist_ok=True)
ENV_PATH = os.path.join(APPDATA_DIR, '.env')
LOG_PATH = os.path.join(APPDATA_DIR, 'stardust.log')

# Logging in AppData
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.NullHandler()
    ]
)

# Lade Umgebungsvariablen aus AppData
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
else:
    # Falls keine .env, lade keine
    pass

# Überprüfe API Key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    try:
        root = tk.Tk()
        root.withdraw()
        api_key = simpledialog.askstring("API-Key erforderlich", "Bitte gib deinen OpenAI API-Key ein:")
        root.destroy()
    except Exception:
        print("Kein API-Key gefunden und keine GUI-Eingabe möglich. Bitte .env Datei manuell anlegen.")
        sys.exit(1)
    if not api_key:
        print("Kein API-Key eingegeben. Das Programm wird beendet.")
        sys.exit(1)
    with open(ENV_PATH, 'w') as f:
        f.write(f'OPENAI_API_KEY={api_key}')
    print("API-Key wurde gespeichert. Programm wird gestartet...")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    load_dotenv(ENV_PATH)

# Konfiguriere OpenAI API
openai.api_key = api_key

# Globale Variablen
is_listening = False
is_writing = False
current_text = ""
original_cursor = None
last_response = ""
current_write_index = 0

def get_ai_response(prompt, context=None, use_context=False):
    """Sende die Eingabe an die OpenAI-API und liefere die Antwort zurück.

    Args:
        prompt: Die Benutzerfrage.
        context: Optionaler Kontext aus der Zwischenablage.
        use_context: Wenn True wird der Kontext dem Prompt hinzugefügt.

    Returns:
        String mit der Antwort der KI oder einer Fehlermeldung.
    """
    try:
        # Prüfe ob es eine mathematische Berechnung ist
        if any(op in prompt for op in ['+', '-', '*', '/']):
            try:
                parts = prompt.split()
                if len(parts) >= 3:
                    num1 = float(parts[0])
                    operator = parts[1]
                    num2 = float(parts[2])
                    if operator == '+':
                        result = num1 + num2
                    elif operator == '-':
                        result = num1 - num2
                    elif operator == '*':
                        result = num1 * num2
                    elif operator == '/':
                        result = num1 / num2
                    else:
                        raise ValueError("Ungültiger Operator")
                    return str(int(result) if result.is_integer() else result)
            except:
                pass
        messages = [
            {"role": "system", "content": """Du bist ein hilfreicher KI-Assistent. 
            - Wenn du nach Code gefragt wirst, gib einen vollständigen, ausführbaren Code zurück, der das Problem löst.
            - Der Code muss funktionieren und alle notwendigen Imports und Funktionen enthalten.
            - Verwende Markdown-Formatierung für Code-Blöcke.
            - Bei Programmieranfragen, die mit 'code' oder 'programmiere' beginnen, MUSS du funktionierenden Code zurückgeben.
            - Wenn du nach einer Erklärung gefragt wirst, gib eine kurze, präzise Antwort.
            - Wenn du nach einer Berechnung gefragt wirst, gib nur das Ergebnis zurück."""}
        ]
        if use_context and context:
            messages.append({"role": "user", "content": f"Kontext: {context}\n\nFrage: {prompt}"})
        else:
            messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Fehler bei der API-Anfrage: {str(e)}")
        return "Fehler bei der API-Anfrage"

def set_cursor_style(style):
    """Ändert das Aussehen des Mauszeigers je nach Programmzustand."""
    try:
        if style == "recording":
            # Roter Cursor
            cursor_info = win32gui.GetCursorInfo()
            if cursor_info[1] > 0:  # Wenn ein Cursor existiert
                hcursor = win32gui.LoadCursor(0, win32con.IDC_CROSS)
                win32gui.SetCursor(hcursor)
        else:
            # Normaler Cursor
            hcursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
            win32gui.SetCursor(hcursor)
    except Exception as e:
        logging.error(f"Fehler beim Ändern des Cursors: {str(e)}")

def on_key_event(event):
    """Verarbeitet Tastatureingaben während des Programms."""
    global is_listening, is_writing, current_text, current_write_index, last_response
    if event.event_type == keyboard.KEY_DOWN:
        if is_writing:
            if current_write_index < len(last_response):
                keyboard.send('backspace')
                time.sleep(0.01)
                keyboard.write(last_response[current_write_index])
                time.sleep(0.01)
                current_write_index += 1
                if current_write_index >= len(last_response):
                    is_writing = False
                    set_cursor_style("normal")
                    logging.info("=== Write Mode beendet ===")
            return
        # Robuste Strg+V-Erkennung
        if is_listening and event.name == 'v' and keyboard.is_pressed('ctrl'):
            pasted = pyperclip.paste()
            current_text += pasted
            logging.info(f"Text aktualisiert (Paste): {current_text}")
            return  # NICHT das 'v' anhängen!
        elif event.name == 'backspace' and is_listening:
            current_text = current_text[:-1]
            logging.info(f"Text aktualisiert (Backspace): {current_text}")
        elif len(event.name) == 1 and is_listening:
            current_text += event.name
            logging.info(f"Text aktualisiert: {current_text}")

def start_listening():
    """Startet den Aufnahmemodus für Benutzereingaben."""
    global is_listening, current_text
    is_listening = True
    current_text = ""
    set_cursor_style("recording")
    logging.info("=== Aufnahmemodus gestartet ===")

def stop_listening():
    """Beendet den Aufnahmemodus und schickt die Anfrage an die KI."""
    global is_listening, last_response
    if is_listening:
        is_listening = False
        set_cursor_style("normal")
        logging.info("=== Aufnahmemodus beendet ===")
        if current_text:
            use_context = False
            context = None
            prompt = current_text
            if current_text.startswith('.'):
                use_context = True
                prompt = current_text[1:].strip()
                context = pyperclip.paste()
            response = get_ai_response(prompt, context, use_context)
            last_response = response
            pyperclip.copy(response)
            logging.info(f"Anfrage: {current_text[:50]}...")
            logging.info(f"Antwort: {response[:50]}...")

def toggle_write_mode():
    """Schaltet den Schreibmodus zum automatischen Tippen um."""
    global is_writing, current_write_index
    if not is_writing and last_response:
        is_writing = True
        current_write_index = 0
        set_cursor_style("recording")
        logging.info("=== Write Mode gestartet ===")
    else:
        is_writing = False
        set_cursor_style("normal")
        logging.info("=== Write Mode beendet ===")

def cancel_listening():
    """Bricht Aufnahme- oder Schreibmodus sofort ab."""
    global is_listening, is_writing
    if is_listening or is_writing:
        is_listening = False
        is_writing = False
        set_cursor_style("normal")
        logging.info("=== Modus abgebrochen ===")

def create_tray_icon():
    """Erzeugt das System-Tray-Icon mit Beenden-Menü."""
    def on_exit(icon, item):
        icon.stop()
        os._exit(0)

    # Icon laden (stardust.ico)
    try:
        image = Image.open("stardust.ico")
    except Exception:
        image = None
    menu = (item('Beenden / Exit', on_exit),)
    icon = pystray.Icon("StarDust", image, "StarDust", menu)
    icon.run_detached()

def main():
    """Initialisiert Hotkeys und startet die Ereignisschleife."""
    create_tray_icon()
    try:
        # Registriere die Hotkeys
        keyboard.add_hotkey('ctrl+alt+y', start_listening)
        keyboard.add_hotkey('ctrl+alt+x', stop_listening)
        keyboard.add_hotkey('ctrl+alt+v', toggle_write_mode)
        keyboard.add_hotkey('win+esc', cancel_listening)
        # Registriere Tastatureingaben
        keyboard.hook(on_key_event)
        logging.info("Programm gestartet - Warte auf Hotkey (Ctrl+Alt+Y)")
        keyboard.wait()
    except Exception as e:
        logging.error(f"Fehler im Hauptprogramm: {str(e)}")
    finally:
        keyboard.unhook_all()
        set_cursor_style("normal")

if __name__ == "__main__":
    main()
