from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    return render_template("index.html")

@app.route("/congrt")
def congrt():
    return "congratulation"
