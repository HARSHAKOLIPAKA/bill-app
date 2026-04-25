from flask import Flask, render_template, request, redirect, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "chat_secret"

# Temporary storage (later we use database)
messages = []

@app.route('/')
def home():
    return render_template("chat.html", messages=messages)

@app.route('/send', methods=['POST'])
def send():
    username = request.form['username']
    text = request.form['message']

    messages.append({
        "user": username,
        "text": text,
        "time": datetime.now().strftime("%H:%M")
    })

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
