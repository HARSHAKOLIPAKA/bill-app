import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_key"

socketio = SocketIO(app, cors_allowed_origins="*")

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

# ---------------- ONLINE USERS ----------------
online_users = set()

# ---------------- ROUTES ----------------
@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        conn = sqlite3.connect("chat.db")
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users (username,password) VALUES (?,?)", (u,p))
            conn.commit()
        except:
            return "User already exists"

        return redirect('/login')

    return render_template("register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        conn = sqlite3.connect("chat.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
        user = c.fetchone()

        if user:
            session['user'] = u
            return redirect('/chat')

        return "Invalid login"

    return render_template("login.html")

@app.route('/chat')
def chat():
    if 'user' not in session:
        return redirect('/login')

    return render_template("chat.html", user=session['user'])

@app.route('/logout')
def logout():
    user = session.get('user')
    if user in online_users:
        online_users.remove(user)

    session.clear()
    return redirect('/login')

# ---------------- SOCKET CONNECT ----------------
@socketio.on('connect')
def connect():
    user = session.get('user')
    if user:
        online_users.add(user)
        emit("users", list(online_users), broadcast=True)

# ---------------- SOCKET DISCONNECT ----------------
@socketio.on('disconnect')
def disconnect():
    user = session.get('user')
    if user in online_users:
        online_users.remove(user)
        emit("users", list(online_users), broadcast=True)

# ---------------- CHAT MESSAGE ----------------
@socketio.on('message')
def handle_message(msg):
    user = session.get('user')

    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (sender,message) VALUES (?,?)", (user,msg))
    conn.commit()
    conn.close()

    emit("message", {"user": user, "message": msg}, broadcast=True)

# ---------------- START ----------------
if __name__ == "__main__":
    init_db()
    socketio.run(app, host="0.0.0.0", port=10000)
