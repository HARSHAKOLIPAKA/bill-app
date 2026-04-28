from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# ================= DATABASE =================

def get_db():
    conn = sqlite3.connect('chat.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    # Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE
        )
    ''')

    # Messages table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            receiver TEXT,
            message TEXT,
            time TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ================= ROUTES =================

# 🔐 Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')

        if not username:
            return "Username required", 400

        session['user'] = username

        conn = get_db()
        try:
            conn.execute("INSERT INTO users (username) VALUES (?)", (username,))
            conn.commit()
        except:
            pass  # user already exists
        conn.close()

        return redirect('/home')

    return render_template('index.html')


# 🏠 Home (User List)
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')

    conn = get_db()

    users = conn.execute(
        "SELECT username FROM users WHERE username != ?",
        (session['user'],)
    ).fetchall()

    conn.close()

    return render_template('home.html', users=users)


# 💬 Chat Page
@app.route('/chat/<user>')
def chat(user):
    if 'user' not in session:
        return redirect('/')

    return render_template('chat.html', other=user)


# 📥 Get Messages (API)
@app.route('/get_messages/<user>')
def get_messages(user):
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()

    messages = conn.execute('''
        SELECT * FROM messages
        WHERE (sender=? AND receiver=?)
        OR (sender=? AND receiver=?)
        ORDER BY id
    ''', (session['user'], user, user, session['user'])).fetchall()

    conn.close()

    return jsonify([dict(m) for m in messages])


# 📤 Send Message (API)
@app.route('/send_message/<user>', methods=['POST'])
def send_message(user):
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({"error": "Invalid data"}), 400

    msg = data['message'].strip()

    if msg == "":
        return jsonify({"error": "Empty message"}), 400

    time = datetime.now().strftime("%H:%M")

    conn = get_db()
    conn.execute('''
        INSERT INTO messages (sender, receiver, message, time)
        VALUES (?, ?, ?, ?)
    ''', (session['user'], user, msg, time))
    conn.commit()
    conn.close()

    return jsonify({"status": "sent"})


# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)
