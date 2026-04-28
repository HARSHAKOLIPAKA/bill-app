from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    conn = sqlite3.connect('chat.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['username']
        return redirect('/chat')
    return render_template('index.html')

@app.route('/chat')
def chat():
    if 'user' not in session:
        return redirect('/')
    return render_template('chat.html')

# 👉 NEW: get messages (API)
@app.route('/get_messages')
def get_messages():
    conn = get_db()
    messages = conn.execute("SELECT * FROM messages").fetchall()
    conn.close()

    return jsonify([dict(msg) for msg in messages])

# 👉 NEW: send message (API)
@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user' not in session:
        return "Unauthorized", 401

    data = request.json
    msg = data['message']

    conn = get_db()
    conn.execute("INSERT INTO messages (user, message) VALUES (?, ?)", (session['user'], msg))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
    
