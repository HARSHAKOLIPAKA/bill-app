from flask import Flask, render_template, request, redirect, session, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = "harsha_secret_key_123"


# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "SURESH" and password == "232003":
            session['user'] = username
            return redirect('/home')
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")


# ---------------- HOME ----------------
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


# ---------------- PDF GENERATE ----------------
@app.route('/generate', methods=['POST'])
def generate():

    if 'user' not in session:
        return redirect('/')

    # FORM DATA
    name = request.form['name']
    depth = int(request.form['depth'])
    rate = int(request.form['rate'])
    advance = int(request.form['advance'])

    total = depth * rate
    balance = total - advance

    # BILL INFO
    bill_no = f"BW{random.randint(1000,9999)}"
    file_name = f"bill_{bill_no}.pdf"

    # PDF START
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4

    # BORDER
    c.rect(20, 20, width-40, height-40)

    # PHONE (RIGHT TOP)
    c.setFont("Helvetica", 10)
    c.drawRightString(width-30, height-50, "Cell: 9618532962")
    c.drawRightString(width-30, height-65, "7013973292")

    # TITLE
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width/2, height-120, "HARSHAVARDHAN BOREWELLS")

    # ADDRESS
    c.setFont("Helvetica", 12)
    c.drawCentredString(
        width/2,
        height-150,
        "Julurupadu, mainroad, Bhadradri kothagudem district - 507166"
    )

    # LINE
    c.line(40, height-200, width-40, height-200)

    # CUSTOMER INFO
    c.setFont("Helvetica", 12)
    c.drawString(50, height-220, f"Customer: {name}")
    c.drawString(400, height-220, f"Bill No: {bill_no}")
    c.drawString(400, height-240, f"Date: {datetime.now().strftime('%d-%m-%Y')}")

    # ITEMS
    y = height - 300
    c.setFont("Helvetica", 14)

    c.drawString(80, y, "5 Inch 140MM Sudhakar 6CG PVC pipes")
    c.drawString(width-250, y, f": {depth} X {rate}")
    c.drawRightString(width-60, y, f"= {total}")

    y -= 35

    c.drawString(80, y, "Transport and Labour charges")
    c.drawString(width-250, y, ":")
    c.drawRightString(width-60, y, f"+ {advance}")

    y -= 50

    # TOTAL
    c.setFont("Helvetica-Bold", 16)
    c.drawString(80, y, "Grand Total")
    c.drawString(width-250, y, ":")
    c.drawRightString(width-60, y, f"= {balance}")

    # FOOTER
    c.setFont("Helvetica", 10)
    c.drawString(50, 80, "Thank You! Visit Again 🙏")
    c.drawString(width-150, 80, "Signature")

    c.save()

    return send_file(file_name, as_attachment=True)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
