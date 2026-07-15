# whatsapp_reader.py
import time
import sys
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

# +--------------------------------------------------------------------+
# |                        KONFIGURATION                               |
# +--------------------------------------------------------------------+
#
# Der Kontaktname wird als Kommandozeilenargument übergeben.
# Beispiel: python whatsapp_reader.py "Max Mustermann"
#

# +--------------------------------------------------------------------+
# |                      ANLEITUNG ZUR BENUTZUNG                         |
# +--------------------------------------------------------------------+
#
# 1. SCHLIESSE ALLE FENSTER VON GOOGLE CHROME.
#    Das ist wichtig, damit der Befehl im nächsten Schritt funktioniert.
#
# 2. ÖFFNE EIN TERMINAL/EINE KONSOLE UND FÜHRE DIESEN BEFEHL AUS:
#
#    Für Linux/macOS:
#    google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-dev-session"
#
#    Für Windows (im Command Prompt):
#    "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%TEMP%\chrome-dev-session"
#
#    -> Ein neues, leeres Chrome-Fenster wird geöffnet.
#
# 3. LOGGE DICH IN DIESEM NEUEN FENSTER BEI WEB.WHATSAPP.COM EIN.
#    Warte, bis deine Chats vollständig geladen sind.
#
# 4. FÜHRE DIESES PYTHON-SKRIPT AUS.
#    Das Skript wird sich mit dem bereits geöffneten Browser verbinden.
#
# +--------------------------------------------------------------------+

def main():
    """Hauptfunktion zum Auslesen des WhatsApp-Chats."""

    if len(sys.argv) < 2:
        print("FEHLER: Bitte gib den Kontaktnamen als Argument an.")
        print("Verwendung: python whatsapp_reader.py \"Kontaktname\"")
        sys.exit(1)

    CONTACT_NAME = sys.argv[1]

    print("Verbinde mit der laufenden Chrome-Instanz...")

    with sync_playwright() as p:
        try:
            # Verbinde mit dem laufenden Chrome über CDP
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")

            # Hole den Default-Context (der existierende Browser-Context)
            contexts = browser.contexts
            if not contexts:
                print("\nFEHLER: Keine aktiven Browser-Kontexte gefunden.")
                print("Stelle sicher, dass Chrome läuft und du bei WhatsApp Web eingeloggt bist.")
                sys.exit(1)

            context = contexts[0]

            # Suche nach einem offenen WhatsApp Web Tab oder öffne einen neuen
            pages = context.pages
            page = None

            for p_page in pages:
                if "web.whatsapp.com" in p_page.url:
                    page = p_page
                    print("Verwende bestehenden WhatsApp Web Tab.")
                    break

            if not page:
                page = context.new_page()
                print("Öffne WhatsApp Web...")
                page.goto("https://web.whatsapp.com")
                print("Warte auf Login... (bitte QR-Code scannen falls nötig)")
                # Warte auf das Suchfeld - zeigt an, dass WhatsApp geladen ist
                page.wait_for_selector('[data-testid="chat-list-search"]', timeout=60000)

            print("Erfolgreich mit Chrome verbunden.")

        except Exception as e:
            print("\nFEHLER BEIM VERBINDEN MIT CHROME:")
            print("Stelle sicher, dass du die Anleitung oben genau befolgt hast.")
            print("1. Sind alle anderen Chrome-Fenster geschlossen?")
            print("2. Hast du Chrome mit dem exakten Befehl aus der Anleitung gestartet?")
            print(f"(Fehlerdetails: {e})")
            sys.exit(1)

        try:
            # --- 1. Kontakt suchen und öffnen ---
            print(f"Suche nach dem Chat: '{CONTACT_NAME}'...")

            # Versuche verschiedene Selektoren für das Suchfeld
            search_box = None
            selectors = [
                '[data-testid="chat-list-search"]',
                'div[contenteditable="true"][data-tab="3"]',
                'div[title*="Suchen"]',
                'div[title*="Search"]',
                'p.selectable-text[contenteditable="true"]'
            ]

            print("Suche Suchfeld...")
            for selector in selectors:
                try:
                    search_box = page.locator(selector).first
                    search_box.click(timeout=5000)
                    print(f"Suchfeld gefunden: {selector}")
                    break
                except:
                    continue

            if not search_box:
                print("\nFEHLER: Suchfeld konnte nicht gefunden werden.")
                print("Stelle sicher, dass WhatsApp Web vollständig geladen ist.")
                sys.exit(1)

            search_box.fill(CONTACT_NAME)
            print(f"Suche nach '{CONTACT_NAME}' eingegeben, warte auf Ergebnisse...")
            time.sleep(2)

            # Finde den Chat in den Suchergebnissen
            # Playwright wartet automatisch auf das Element
            try:
                chat_result = page.locator(f'span[title="{CONTACT_NAME}"]').first
                chat_result.click(timeout=10000)
                print(f"Chat mit '{CONTACT_NAME}' geöffnet.")
            except Exception:
                print(f"\nFEHLER: Chat '{CONTACT_NAME}' konnte nicht gefunden werden.")
                print("Verfügbare Chats im Suchfeld:")
                try:
                    # Zeige verfügbare Chat-Titel
                    titles = page.locator('[data-testid="cell-frame-title"]').all_text_contents()
                    for title in titles[:10]:
                        print(f"  - {title}")
                except:
                    print("  (Konnte keine Chat-Titel auslesen)")
                sys.exit(1)

            time.sleep(2)  # Warte, bis der Chat-Verlauf geladen wird

            # --- 2. Nachrichten auslesen und scrollen ---
            print("Beginne mit dem Auslesen des Verlaufs. Das kann je nach Länge dauern...")

            all_messages = []
            no_new_messages_count = 0
            last_message_count = 0

            while no_new_messages_count < 3:
                # Finde alle Nachrichten-Elemente
                # Versuche verschiedene Selektoren
                message_elements = []
                msg_selectors = [
                    '[data-testid="msg-container"]',
                    'div.message-in, div.message-out',
                    'div[class*="message"]'
                ]

                for selector in msg_selectors:
                    try:
                        message_elements = page.locator(selector).all()
                        if message_elements:
                            if last_message_count == 0:  # Nur beim ersten Mal
                                print(f"Nachrichten gefunden mit: {selector}")
                            break
                    except:
                        continue

                current_count = len(message_elements)
                if current_count > last_message_count:
                    print(f"{current_count} Nachrichten im sichtbaren Bereich...")
                    last_message_count = current_count

                new_messages_found = False

                # Extrahiere Nachrichten von oben nach unten
                for msg_el in message_elements:
                    try:
                        # Hole den kompletten Text der Nachricht
                        message_text = msg_el.inner_text()

                        if message_text and message_text not in all_messages:
                            all_messages.append(message_text)
                            new_messages_found = True
                    except Exception:
                        continue

                if new_messages_found:
                    no_new_messages_count = 0
                else:
                    no_new_messages_count += 1
                    print("Keine neuen Nachrichten gefunden, scrolle weiter nach oben...")

                # Nach oben scrollen um ältere Nachrichten zu laden
                # Fokussiere den Chat und scrolle mit Keyboard
                page.keyboard.press("PageUp")
                page.keyboard.press("PageUp")
                time.sleep(2)

                # Alternative: Scrolle mit JavaScript am ganzen Window
                page.evaluate("window.scrollTo(0, 0)")
                time.sleep(2)

            print(f"\nGesamt: {len(all_messages)} Nachrichten gefunden.")

            print("\n--- VOLLSTÄNDIGER CHAT-VERLAUF ---")
            for msg in all_messages:
                print(msg)
                print("-" * 40)

            # Exportiere in Datei
            if all_messages:
                os.makedirs("exports", exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"exports/{CONTACT_NAME}_{timestamp}.txt"

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"WhatsApp Chat Export: {CONTACT_NAME}\n")
                    f.write(f"Exportiert am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Anzahl Nachrichten: {len(all_messages)}\n")
                    f.write("=" * 80 + "\n\n")
                    for msg in all_messages:
                        f.write(msg + "\n")
                        f.write("-" * 40 + "\n")

                print(f"\nChat wurde exportiert nach: {filename}")
            else:
                print("\nKeine Nachrichten gefunden - kein Export erstellt.")

        except Exception as e:
            print(f"\nEin Fehler ist aufgetreten: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("\nSkript beendet.")


if __name__ == "__main__":
    main()
