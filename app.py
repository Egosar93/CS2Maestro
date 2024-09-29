from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# Flask-Login 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Einfacher Account
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
@app.route('/logout', methods=['GET', 'POST'])  # Erlaube sowohl GET als auch POST
@login_required
def logout():
    logout_user()
    flash('Erfolgreich abgemeldet', 'success')
    return redirect(url_for('login'))

# Route zum Starten des Servers (erfordert Login)
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

# Route zum Stoppen des Servers (erfordert Login)
@app.route('/stop_servers', methods=['POST'])
@login_required
def stop_servers():
    try:
        result = subprocess.run(['./stop_cs2_servers.sh'], capture_output=True, text=True)
        return jsonify({"status": "success", "message": result.stdout})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
