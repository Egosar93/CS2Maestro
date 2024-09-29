#!/bin/bash

# Definiert Start- und Endport
startPort=27015
endPort=27020  # Passe diese Werte nach Bedarf an

# Initialisiert einen Zähler für gestoppte Server
countStopped=0

# Schleife zum Überprüfen und Beenden von Servern, die auf den definierten Ports laufen
for (( port=startPort; port<=endPort; port++ ))
do
    # Überprüft, ob auf dem Port ein Prozess läuft und holt die PID
    pid=$(lsof -t -i:$port)

    if [ -n "$pid" ]; then
        echo "Beende CS2-Server auf Port $port (PID: $pid)..."
        
        # Beendet den Prozess
        kill -9 $pid
        
        if [ $? -eq 0 ]; then
            echo "Server auf Port $port erfolgreich beendet."
            ((countStopped++))
        else
            echo "Fehler beim Beenden des Servers auf Port $port."
        fi
    else
        echo "Kein Server auf Port $port gefunden."
    fi
done

# Gibt die Anzahl der erfolgreich gestoppten Server aus
echo "$countStopped Server erfolgreich gestoppt."
