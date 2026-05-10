from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# ================= DATABASE =================

def get_db():
    conn = sqlite3.connect('chat.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create tables
conn = get_db()

conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    message TEXT,
    time TEXT
)
''')

conn.commit()
conn.close()

# ================= HOME =================

@app.route('/')
def home():
    if 'username' in session:
        return redirect('/chat')
    return redirect('/login')

# ================= REGISTER =================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_db()

        try:
            conn.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, password)
            )

            conn.commit()

            return redirect('/login')

        except:
            return "Username already exists"

    return render_template('register.html')

# ================= LOGIN =================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_db()

        user = conn.execute(
            'SELECT * FROM users WHERE username=? AND password=?',
            (username, password)
        ).fetchone()

        if user:
            session['username'] = username
            return redirect('/chat')

        return "Invalid username or password"

    return render_template('login.html')

# ================= CHAT =================

@app.route('/chat', methods=['GET', 'POST'])
def chat():

    if 'username' not in session:
        return redirect('/login')

    username = session['username']

    conn = get_db()

    if request.method == 'POST':

        message = request.form['message']
        time = datetime.now().strftime('%H:%M')

        conn.execute(
            'INSERT INTO messages (username, message, time) VALUES (?, ?, ?)',
            (username, message, time)
        )

        conn.commit()

    messages = conn.execute(
        'SELECT * FROM messages'
    ).fetchall()

    return render_template(
        'chat.html',
        messages=messages,
        username=username
    )

# ================= LOGOUT =================

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ================= RUN =================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
