from flask import Flask, render_template, request

app = Flask(__name__)

# 🏠 HOME PAGE
@app.route('/')
def home():
    return render_template("index.html")


# 🧾 BILL PAGE
@app.route('/bill', methods=['GET', 'POST'])
def bill():
    total = None
    if request.method == 'POST':
        name = request.form.get('name')
        depth = int(request.form.get('depth'))
        rate = int(request.form.get('rate'))
        advance = int(request.form.get('advance'))

        total_amount = depth * rate
        balance = total_amount - advance

        total = {
            "name": name,
            "depth": depth,
            "rate": rate,
            "advance": advance,
            "total_amount": total_amount,
            "balance": balance
        }

    return render_template("bill.html", data=total)


# 🚀 RUN APP
if __name__ == "__main__":
    app.run(debug=True)
