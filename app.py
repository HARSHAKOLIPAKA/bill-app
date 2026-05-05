from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
app.secret_key = "chat_secret"

socketio = SocketIO(app, cors_allowed_origins="*")

# ---------------- DATABASE INIT ----------------
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

# ---------------- HOME ----------------
@app.route('/')
def home():
    return redirect('/login')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        conn = sqlite3.connect("chat.db")
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
            conn.commit()
        except:
            return "User already exists"

        conn.close()
        return redirect('/login')

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        conn = sqlite3.connect("chat.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
        user = c.fetchone()

        conn.close()

        if user:
            session['user'] = u
            return redirect('/chat')

        return "Invalid login"

    return render_template("login.html")

# ---------------- CHAT PAGE ----------------
@app.route('/chat')
def chat():
    if 'user' not in session:
        return redirect('/login')

    return render_template("chat.html", user=session['user'])

# ---------------- SOCKET MESSAGE ----------------
@socketio.on('message')
def handle_message(msg):
    user = session.get('user')

    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    c.execute("INSERT INTO messages (sender, message) VALUES (?, ?)", (user, msg))
    conn.commit()
    conn.close()

    emit("message", {
        "user": user,
        "message": msg
    }, broadcast=True)

# ---------------- LOAD OLD MESSAGES ----------------
@app.route('/messages')
def messages():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    c.execute("SELECT sender, message FROM messages")
    data = c.fetchall()

    conn.close()

    return {"data": data}

# ---------------- RUN ----------------
if __name__ == "__main__":
    init_db()
    socketio.run(app, host="0.0.0.0", port=10000)
