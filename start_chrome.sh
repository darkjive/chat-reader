#!/bin/bash

# Dieses Skript automatisiert den Start von Google Chrome im Debug-Modus.

echo "Versuche, alle laufenden Chromium-Prozesse zu beenden..."
# 'pkill' beendet Prozesse, die auf das Muster passen.
# '|| true' verhindert, dass das Skript fehlschlägt, wenn keine Prozesse gefunden werden.
pkill -f "chromium" || true

echo "Warte 2 Sekunden, um sicherzustellen, dass die Prozesse beendet wurden..."
sleep 2

echo "Entferne das alte temporäre Profilverzeichnis..."
rm -rf "/tmp/chrome-dev-session"

echo "Starte Chromium im Debug-Modus..."
# Das '&'-Zeichen am Ende startet den Prozess im Hintergrund,
# sodass das Terminal für andere Befehle frei bleibt.
chromium --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-dev-session" &

echo "Chrome wurde gestartet. Es kann einen Moment dauern, bis das Fenster erscheint."
echo "Du kannst dieses Terminal nun für andere Befehle verwenden oder es geöffnet lassen."
