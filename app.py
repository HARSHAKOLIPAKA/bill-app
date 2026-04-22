from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    name = request.form["name"]
    amount = request.form["amount"]
    service = request.form["service"]

    return f"""
    <h2>Bill Generated</h2>
    <p>Customer: {name}</p>
    <p>Service: {service}</p>
    <p>Amount: ₹{amount}</p>
    <a href="/">Go Back</a>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
