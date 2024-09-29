#!/bin/bash

# Überprüft, ob mindestens vier Argumente übergeben wurden
if [ "$#" -lt 4 ]; then
    echo "Fehler: Zu wenige Argumente. Benutzung: $0 <Basisname> <Anzahl der Server> <Mapname> <Gamemode>"
    exit 1
fi

# Nimmt den Basisnamen, die Anzahl der Server, den Mapnamen und den Gamemode von den Befehlszeilenargumenten
baseServerName=$1
serverCount=$2
mapName=$3
gameMode=$4

# Definiert Start- und Endport
startPort=27015
endPort=27020  # Stellen Sie sicher, dass dieser Wert den Startport und die mögliche Anzahl von Servern berücksichtigt

# Pfad zur ausführbaren LinuxGSM-Datei für CS2
gameExecutable="$HOME/serverfiles/game/bin/linuxsteamrt64/cs2"

# Erfasst die erste gefundene IP-Adresse des Hosts
hostIP=$(hostname -I | awk '{print $1}')

# Maximal zulässige Anzahl von Servern, basierend auf den Ports
maxServers=$((endPort - startPort + 1))

# Überprüft, ob die angeforderte Serveranzahl das Maximum überschreitet
if (( serverCount > maxServers )); then
    echo "Fehler: Die Anzahl der zu startenden Server ($serverCount) überschreitet das Maximum von $maxServers."
    exit 1
fi

# Initialisiert einen Zähler für erfolgreich gestartete Server
countStarted=0

# Schleife zum Überprüfen und Starten der geforderten Anzahl von Spielservern
for (( i=1; i<=serverCount; i++ ))
do
    port=$((startPort + i - 1))
    
    # Überprüft, ob der Port bereits verwendet wird
    if ss -tupln | grep ":$port" > /dev/null; then
        echo "Fehler: Port $port wird bereits verwendet. Überspringe Server '$baseServerName_$i'."
        continue
    else
        # Generiert den Servernamen basierend auf dem eingegebenen Basisnamen und fügt die Nummer hinzu
        serverName="${baseServerName}_$i"
        echo "Versuche, Server '$serverName' auf Port $port zu starten..."
        
        # Führt den Befehl zum Starten des Servers aus, inklusive Map und Gamemode
        $gameExecutable -dedicated -ip 0.0.0.0 -port $port +map $mapName +game_mode $gameMode +maxplayers 16 +exec cs2server.cfg +hostname "$serverName" &
        
        echo "Warte auf den Serverstart..."
        sleep 10  # Wartet 10 Sekunden, bevor der nächste Server gestartet wird
        echo "Server '$serverName' erfolgreich auf Port $port gestartet."
        ((countStarted++))
    fi
done

# Gibt die Anzahl der erfolgreich gestarteten Server aus
echo "$countStarted von $serverCount Server(n) erfolgreich gestartet."
