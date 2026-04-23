bill_no = 1
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/bill", methods=["POST"])
def bill():
    customer = request.form.get("customer")
    amount = request.form.get("amount")
    return render_template("bill.html", customer=customer, amount=amount)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
