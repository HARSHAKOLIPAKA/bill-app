from flask import Flask, render_template, request

app = Flask(__name__)

# HOME PAGE (this is what opens on your link)
@app.route("/")
def home():
    return render_template("index.html")

# BILL SUBMIT PAGE
@app.route("/bill", methods=["POST"])
def bill():
    customer = request.form.get("customer")
    amount = request.form.get("amount")
    return f"Bill created for {customer} - ₹{amount}"

# IMPORTANT for Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
