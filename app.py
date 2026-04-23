from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
import random
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/generate', methods=['POST'])
def generate_bill():
    name = request.form['name']
    depth = int(request.form['depth'])
    rate = int(request.form['rate'])
    advance = int(request.form['advance'])

    # CALCULATION
    total = depth * rate
    balance = total - advance

    # AUTO INFO
    date = datetime.now().strftime("%d-%m-%Y")
    bill_no = f"BW{random.randint(1000,9999)}"

    # FILE NAME
    file_name = f"bill_{bill_no}.pdf"

    # BUSINESS INFO
    business_name = "HARSHAVARDHAN BOREWELLS"
    phone = "Phone: 9618532962, 7013973292"
    address = "Address: JULURPADU, MAIN ROAD, BHADRADRI KOTHAGUDEM"

    # CREATE PDF
    c = canvas.Canvas(file_name, pagesize=A4)
    page_width = 595

    # HEADER
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(page_width/2, 800, business_name)

    c.setFont("Helvetica", 10)
    c.drawCentredString(page_width/2, 780, phone)
    c.drawCentredString(page_width/2, 765, address)

    # BILL INFO
    c.drawString(400, 740, f"Bill No: {bill_no}")
    c.drawString(400, 725, f"Date: {date}")

    # CUSTOMER
    c.drawString(50, 740, f"Customer: {name}")

    # LINE
    c.line(50, 710, 550, 710)

    # TABLE
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 690, "Description")
    c.drawString(300, 690, "Details")
    c.drawString(450, 690, "Amount")

    c.setFont("Helvetica", 11)
    c.drawString(50, 660, "Borewell Drilling")
    c.drawString(300, 660, f"{depth} ft x ₹{rate}")
    c.drawString(450, 660, f"₹{total}")

    # LINE
    c.line(50, 640, 550, 640)

    # TOTALS
    c.drawString(350, 610, f"Total: ₹{total}")
    c.drawString(350, 590, f"Advance: ₹{advance}")
    c.drawString(350, 570, f"Balance: ₹{balance}")

    # FOOTER
    c.drawString(50, 520, "Payment Mode: Cash / UPI")
    c.drawString(50, 500, "Thank You! 🙏")
    c.drawString(400, 500, "Signature")

    c.save()

    return send_file(file_name, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
