# whatsapp_reader.py
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# +--------------------------------------------------------------------+
# |                        KONFIGURATION                               |
# +--------------------------------------------------------------------+
#
#  ÄNDERE DEN NAMEN HIER:
#  Gib den exakten Namen des Kontakts oder der Gruppe ein, wie er
#  in deiner WhatsApp-Kontaktliste erscheint.
#
CONTACT_NAME = "Name des Kontakts hier eingeben"

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
    
    if CONTACT_NAME == "Name des Kontakts hier eingeben":
        print("FEHLER: Bitte bearbeite das Skript und gib einen Kontaktnamen in der Variable 'CONTACT_NAME' an.")
        sys.exit(1)

    print("Verbinde mit der laufenden Chrome-Instanz...")
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print("\nFEHLER BEIM VERBINDEN MIT CHROME:")
        print("Stelle sicher, dass du die Anleitung oben genau befolgt hast.")
        print("1. Sind alle anderen Chrome-Fenster geschlossen?")
        print("2. Hast du Chrome mit dem exakten Befehl aus der Anleitung gestartet?")
        print(f"(Fehlerdetails: {e})")
        sys.exit(1)

    print("Erfolgreich mit Chrome verbunden. Stelle sicher, dass web.whatsapp.com geöffnet ist.")

    try:
        # --- 1. Kontakt suchen und öffnen ---
        print(f"Suche nach dem Chat: '{CONTACT_NAME}'...")

        # XPath für das Suchfeld in WhatsApp Web (Titel-Attribut ist sprachabhängig)
        search_box_xpath = "//div[@title='Suchen oder neuen Chat starten']"
        
        # Warte, bis die Hauptseite von WhatsApp geladen ist (max. 30 Sekunden)
        search_box = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, search_box_xpath))
        )
        
        # Klicke, leere das Feld und gib den Namen ein
        search_box.click()
        search_box.clear()
        search_box.send_keys(CONTACT_NAME)
        time.sleep(1) # Kurze Pause, damit die Suchergebnisse laden können

        # XPath, um den Chat in der Ergebnisliste zu finden
        chat_xpath = f"//span[contains(@title, '{CONTACT_NAME}')]"
        chat_element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, chat_xpath))
        )
        chat_element.click()
        print(f"Chat mit '{CONTACT_NAME}' geöffnet.")
        time.sleep(2) # Warte, bis der Chat-Verlauf geladen wird

        # --- 2. Nachrichten auslesen und scrollen ---
        # XPath für das Panel, das die Nachrichten enthält.
        # Die Klasse kann sich ändern, dies ist ein Versuch.
        chat_pane_xpath = "//div[contains(@class, '_aigv')]"
        chat_pane = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, chat_pane_xpath))
        )

        print("Beginne mit dem Auslesen des Verlaufs. Das kann je nach Länge dauern...")
        
        all_messages = []
        last_height = 0
        no_new_messages_count = 0

        while no_new_messages_count < 3: # Stoppe, wenn 3x Scrollen keine neuen Nachrichten bringt
            # XPath für einzelne Nachrichten-Container
            message_elements_xpath = ".//div[contains(@class, 'copyable-text')]"
            
            current_messages = chat_pane.find_elements(By.XPATH, message_elements_xpath)
            
            new_messages_found = False
            for msg_el in reversed(current_messages): # Von unten nach oben durchgehen
                # Metadaten (Zeit, Status) und Nachrichtentext sind getrennt
                try:
                    meta_text = msg_el.get_attribute('data-pre-plain-text') # Enthält [Uhrzeit] Name:
                    message_text = msg_el.find_element(By.XPATH, ".//span[contains(@class, 'selectable-text')]" ).text
                    
                    full_message = f"{meta_text} {message_text}"
                    
                    if full_message not in all_messages:
                        all_messages.insert(0, full_message) # Vorne einfügen, um Reihenfolge beizubehalten
                        new_messages_found = True
                except NoSuchElementException:
                    # Manchmal sind Elemente leer oder haben eine andere Struktur
                    continue

            if new_messages_found:
                print(f"{len(all_messages)} Nachrichten gefunden...")
                no_new_messages_count = 0
            else:
                print("Keine *neuen* Nachrichten im sichtbaren Bereich gefunden.")
                no_new_messages_count += 1

            # Nach oben scrollen
            driver.execute_script("arguments[0].scrollTop = 0", chat_pane)
            print("Scrolle nach oben...")
            time.sleep(4) # WICHTIG: Wartezeit, damit alte Nachrichten nachgeladen werden können.
                          # Bei langsamer Verbindung ggf. erhöhen.

        print("\n--- VOLLSTÄNDIGER CHAT-VERLAUF ---")
        for msg in all_messages:
            print(msg)

    except TimeoutException:
        print("\nFEHLER: Ein Element wurde nicht rechtzeitig gefunden.")
        print(f"Mögliche Gründe:")
        print(f"1. Der Kontakt '{CONTACT_NAME}' wurde nicht in der Chat-Liste gefunden.")
        print("2. Die Internetverbindung ist zu langsam.")
        print("3. WhatsApp hat sein Design geändert und die XPaths im Skript sind veraltet.")
    except Exception as e:
        print(f"\nEin unerwarteter Fehler ist aufgetreten: {e}")
    finally:
        print("\nSkript beendet.")


if __name__ == "__main__":
    main()
