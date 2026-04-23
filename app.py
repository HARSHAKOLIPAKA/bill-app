from flask import Flask, render_template, request, redirect, url_for, session, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = "harsha_secret_key_123"  # required for login session


# ---------------- LOGIN PAGE ----------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # SIMPLE LOGIN (you can change later)
        if username == "SURESH" and password == "232003":
            session['user'] = username
            return redirect('/home')
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")


# ---------------- HOME PAGE ----------------
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')
    return render_template("index.html")


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


# ---------------- PDF GENERATOR ----------------
@app.route('/generate', methods=['POST'])
def generate():
    if 'user' not in session:
        return redirect('/')

    name = request.form['name']
    depth = int(request.form['depth'])
    rate = int(request.form['rate'])
    advance = int(request.form['advance'])

    total = depth * rate
    balance = total - advance

    date = datetime.now().strftime("%d-%m-%Y")
    bill_no = f"BW{random.randint(1000,9999)}"

    file_name = f"bill_{bill_no}.pdf"

    c = canvas.Canvas(file_name, pagesize=A4)
    width = 595

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, 800, "HARSHAVARDHAN BOREWELLS")

    c.setFont("Helvetica", 10)
    c.drawString(50, 760, f"Bill No: {bill_no}")
    c.drawString(50, 745, f"Date: {date}")
    c.drawString(50, 730, f"Customer: {name}")

    c.line(50, 710, 550, 710)

    c.drawString(50, 680, f"Depth: {depth} ft")
    c.drawString(50, 660, f"Rate: {rate}")
    c.drawString(50, 640, f"Total: {total}")
    c.drawString(50, 620, f"Advance: {advance}")
    c.drawString(50, 600, f"Balance: {balance}")

    c.save()

    return send_file(file_name, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
