from flask import Flask, render_template, request

app = Flask(__name__)

bill_no = 1

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/bill", methods=["POST"])
def bill():
    global bill_no

    customer = request.form.get("customer")
    amount = request.form.get("amount")

    current_bill = bill_no
    bill_no += 1

    return render_template(
        "bill.html",
        customer=customer,
        amount=amount,
        bill_no=current_bill
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
