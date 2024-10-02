from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, emit
import subprocess
import socket
from rcon.source import Client  # Aktualisierter Import für den RCON-Client

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app, async_mode=None)

# Flask-Login einrichten
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Einfache Benutzerverwaltung (für echte Anwendungen eine Datenbank verwenden)
users = {'admin': {'password': 'password123'}}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

# Route für die Hauptseite
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Login-Seite
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            flash('Login erfolgreich!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Ungültige Anmeldedaten', 'danger')
    return render_template('login.html')

# Logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Erfolgreich abgemeldet', 'success')
    return redirect(url_for('login'))

# Route zum Starten des Servers
@app.route('/start_server', methods=['POST'])
@login_required
def start_server():
    base_name = request.form['base_name']
    server_count = request.form['server_count']
    map_name = request.form['map_name']
    game_mode = request.form['game_mode']
    
    try:
        result = subprocess.run(
            ['./start_cs2_servers.sh', base_name, server_count, map_name, game_mode],
            capture_output=True, text=True
        )
        return jsonify({"status": "success", "message": result.stdout})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Route zum Stoppen des Servers
@app.route('/stop_servers', methods=['POST'])
@login_required
def stop_servers():
    try:
        result = subprocess.run(['./stop_cs2_servers.sh'], capture_output=True, text=True)
        return jsonify({"status": "success", "message": result.stdout})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Route zum Stoppen eines einzelnen Servers
@app.route('/stop_server/<port>', methods=['POST'])
@login_required
def stop_server(port):
    try:
        result = subprocess.run([f'lsof -t -i:{port} | xargs kill -9'], shell=True, capture_output=True, text=True)
        return jsonify({"status": "success", "message": f"Server auf Port {port} wurde gestoppt."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Route zum Überprüfen der aktiven Server
@app.route('/list_servers', methods=['GET'])
@login_required
def list_servers():
    active_servers = []
    ports = range(27015, 27020)  # Beispielhafter Portbereich

    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            if result == 0:
                active_servers.append(f'{port}')

    return jsonify({"servers": active_servers})

# Route für das RCON-Terminal (HTML-Seite)
@app.route('/rcon_terminal')
@login_required
def rcon_terminal():
    return render_template('rcon_terminal.html')

# WebSocket-Event für RCON-Befehle
@socketio.on('send_rcon_command')
@login_required
def handle_rcon_command(data):
    ip = data.get('ip')
    port = data.get('port')
    command = data.get('command')

    try:
        # Aktualisierte Verwendung von rcon.source.Client
        with Client(ip, port, passwd='test123') as client:
            response = client.run(command)
            emit('rcon_output', {'output': response})
    except Exception as e:
        emit('rcon_output', {'output': f"Fehler: {str(e)}"})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
