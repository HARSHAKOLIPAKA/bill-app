from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = "chat_secret"

socketio = SocketIO(app)

online_users = {}

# ---------------- HOME ----------------
@app.route('/')
def home():
    return redirect('/login')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session['user'] = request.form['username']
        return redirect('/chat')
    return render_template('register.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['username']
        return redirect('/chat')
    return render_template('login.html')

# ---------------- CHAT ----------------
@app.route('/chat')
def chat():
    if 'user' not in session:
        return redirect('/login')
    return render_template('chat.html', user=session['user'])

# ---------------- SOCKET CONNECT ----------------
@socketio.on('connect')
def connect():
    user = session.get('user')
    if user:
        online_users[user] = True
        emit('users', list(online_users.keys()), broadcast=True)

# ---------------- SOCKET DISCONNECT ----------------
@socketio.on('disconnect')
def disconnect():
    user = session.get('user')
    if user in online_users:
        del online_users[user]
        emit('users', list(online_users.keys()), broadcast=True)

# ---------------- MESSAGE ----------------
@socketio.on('message')
def handle_message(msg):
    user = session.get('user')
    emit('message', {
        'user': user,
        'message': msg
    }, broadcast=True)

# ---------------- RUN ----------------
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
