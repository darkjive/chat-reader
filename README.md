# WhatsApp Chat Exporter

![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg) ![Lizenz: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Ein Python-Skript zum Exportieren des Chatverlaufs eines bestimmten Kontakts oder einer Gruppe aus WhatsApp Web mithilfe von Playwright.

---

### ⚠️ Haftungsausschluss & Wichtige Warnungen

*   **Nur für Bildungs- und persönlichen Gebrauch:** Dieses Skript ist für den persönlichen Gebrauch gedacht, um deine eigenen Chatdaten zu sichern. Verwende es nicht für andere Zwecke.
*   **Benötigt Debug-Modus:** Dieses Skript funktioniert, indem es deinen Browser fernsteuert. Dies erfordert, dass du Chrome in einem speziellen "Remote Debugging"-Modus startest, der dem Skript erhebliche Kontrolle über deine Browsersitzung gewährt.
*   **Anfällig für Änderungen:** Das Skript basiert auf der internen HTML-Struktur von WhatsApp Web. WhatsApp kann (und wird) seine Website häufig aktualisieren, was das Skript wahrscheinlich unbrauchbar machen wird. Zukünftige Aktualisierungen sind erforderlich, um die Funktionsfähigkeit zu gewährleisten.
*   **Verwende ein temporäres Profil:** Die folgenden Anweisungen verwenden ein temporäres Browserprofil, um eine Beeinträchtigung deiner Hauptbrowserdaten zu vermeiden und die Sicherheit zu erhöhen.

---

### ✨ Funktionen

*   Verbindet sich mit einer bestehenden Chrome-Sitzung.
*   Sucht nach einem angegebenen Kontakt oder einer Gruppe.
*   Scrollt automatisch bis zum Anfang des Chats, um den gesamten Verlauf zu laden.
*   Extrahiert alle Nachrichten und gibt sie auf der Konsole aus.
*   Speichert eine vollständige Kopie des Chats in `exported_chat.txt`.

---

### ⚙️ Voraussetzungen

*   Python 3.7+
*   Google Chrome Browser

---

### 🚀 Installation

1.  **Repository klonen:**
    ```bash
    git clone <deine-repository-url>
    cd chat-reader
    ```

2.  **Virtuelle Python-Umgebung erstellen:**
    ```bash
    python3 -m venv venv
    ```

3.  **Virtuelle Umgebung aktivieren:**
    *   Unter macOS & Linux:
        ```bash
        source venv/bin/activate
        ```
    *   Unter Windows:
        ```bash
        venv\Scripts\activate
        ```

4.  **Erforderliche Abhängigkeiten installieren:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Playwright Browser installieren:**
    ```bash
    playwright install chromium
    ```

---

### 📖 Verwendung

1.  **Chrome im Debug-Modus starten:**
    Schließe alle Chrome-Fenster und führe folgenden Befehl aus:

    Linux/macOS:
    ```bash
    google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-dev-session"
    ```

    Windows (Command Prompt):
    ```cmd
    "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%TEMP%\chrome-dev-session"
    ```

2.  **Bei WhatsApp Web anmelden:**
    Navigiere in dem soeben geöffneten Chrome-Fenster zu `web.whatsapp.com` und melde dich an, indem du den QR-Code mit deinem Telefon scannst. Warte, bis deine Chats vollständig geladen sind.

3.  **Exporter-Skript ausführen:**
    ```bash
    ./run_exporter.sh "Kontaktname"
    ```

    Oder direkt:
    ```bash
    python whatsapp_reader.py "Kontaktname"
    ```

Das Skript findet den Chat, scrollt durch den Verlauf und exportiert alle Nachrichten in eine Datei im `exports/` Verzeichnis (Format: `Kontaktname_TIMESTAMP.txt`).

---

### 🤝 Mitwirken

Beiträge sind willkommen! Wenn du das Skript verbessern möchtest, befolge diese Schritte:

1.  Forke das Repository.
2.  Erstelle einen neuen Branch (`git checkout -b feature/dein-feature-name`).
3.  Nimm deine Änderungen vor.
4.  Commite deine Änderungen (`git commit -m 'Add some feature'`).
5.  Pushe in den Branch (`git push origin feature/dein-feature-name`).
6.  Öffne einen Pull Request.

Einige Ideen zur Verbesserung:
*   XPaths robuster machen.
*   Fehlerbehandlung für mehr Sonderfälle hinzufügen.
*   Export in verschiedene Formate (JSON, CSV).
*   Eine einfache Benutzeroberfläche hinzufügen.

---

### 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Details findest du in der Datei `LICENSE`.