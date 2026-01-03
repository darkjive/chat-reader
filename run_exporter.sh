#!/bin/bash

# Dieses Skript führt das Python-Export-Skript mit dem korrekten
# Python-Interpreter aus dem virtuellen Environment ('venv') aus.

# Prüfen, ob das venv-Verzeichnis existiert
if [ ! -d "venv" ]; then
    echo "Fehler: Das virtuelle Environment 'venv' wurde nicht gefunden."
    echo "Bitte führe zuerst die Schritte im Abschnitt 'Installation' der README aus."
    exit 1
fi

# Prüfen, ob das Python-Skript existiert
if [ ! -f "whatsapp_reader.py" ]; then
    echo "Fehler: Die Datei 'whatsapp_reader.py' wurde nicht gefunden."
    exit 1
fi

echo "Starte den WhatsApp Exporter mit dem Python-Interpreter aus 'venv'..."
echo "---"

# Führe das Skript direkt mit dem Python aus dem venv aus
# Alle Argumente werden durchgereicht
./venv/bin/python whatsapp_reader.py "$@"

echo "---"
echo "Exporter-Skript beendet."
