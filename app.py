from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/bill', methods=['GET', 'POST'])
def bill():
    if request.method == 'POST':
        name = request.form.get('name')
        depth = int(request.form.get('depth'))
        rate = int(request.form.get('rate'))
        advance = int(request.form.get('advance'))

        total = depth * rate
        balance = total - advance

        return render_template(
            "bill.html",
            name=name,
            depth=depth,
            rate=rate,
            advance=advance,
            total=total,
            balance=balance
        )

    # If someone opens /bill directly
    return "Please submit form first from home page"


if __name__ == "__main__":
    app.run()
    
