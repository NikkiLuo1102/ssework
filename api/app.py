from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    return render_template("hello.html", name=input_name, age=input_age)


@app.route("/query", methods=["GET"])
def get_query_parameter():
    query_parameter = request.args.get("q")
    return process_query(query_parameter)


def process_query(query_parameter):
    if query_parameter == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    elif query_parameter == "What is your name?":
        return "KFC V50"
    else:
        return "Unknown"
