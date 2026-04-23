from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/bill', methods=['GET', 'POST'])
def bill():
    data = None

    if request.method == 'POST':
        name = request.form.get('name')
        depth = int(request.form.get('depth'))
        rate = int(request.form.get('rate'))
        advance = int(request.form.get('advance'))

        total = depth * rate
        balance = total - advance

        data = {
            "name": name,
            "depth": depth,
            "rate": rate,
            "advance": advance,
            "total": total,
            "balance": balance
        }

    return render_template("bill.html", data=data)


if __name__ == "__main__":
    app.run()
