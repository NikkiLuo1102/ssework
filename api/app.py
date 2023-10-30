from flask import Flask, render_template, request
import re
import math
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


def is_prime(i):
    if i <= 1 or i % 2 == 0 or i % 3 == 0:
        return False
    elif i <= 3:
        return True
    else:
        k = 5
        while k * k <= i:
            if i % k == 0 or i % (k + 2) == 0:
                return False
            k += 6
        return True


def process_query(query_parameter):
    pattern_multiplied = r'What is \d+ multiplied by \d+\?$'
    pattern_largest = r'Which of the following numbers is the largest\
        : \d+(, \d+)+\?$'
    pattern_plus = r'What is \d+ plus \d+\?$'
    pattern_square_cubes = r'Which of the following numbers is both \
        a square and a cube: \d+(, \d+)+\?$'
    pattern_prime = r'Which of the following numbers are primes\
        : \d+(, \d+)+\?$'
    pattern_minus = r'What is \d+ minus \d+\?$'
    pattern_num = r'\d+'

    if re.match(pattern_multiplied, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        res = 1
        for i in matches:
            res = res * int(i)
        return str(res)

    elif re.match(pattern_largest, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        int_ls = [int(i) for i in matches]
        return str(max(int_ls))

    elif re.match(pattern_plus, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        res = 0
        for i in matches:
            res = res + int(i)
        return str(res)

    elif re.match(pattern_square_cubes, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        res = ""
        for i in matches:
            square_root = math.sqrt(i)
            cube_root = i ** (1/3)
            if square_root.is_integer() and cube_root.is_integer():
                res = res + str(i) + ", "
        return res[0:-2]

    elif re.match(pattern_minus, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        res = 0
        for i in matches:
            res = res - int(i)
        return str(res)

    elif re.match(pattern_prime, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        res = ""
        for i in matches:
            i = int(i)
            if is_prime(i):
                res = res + str(i) + ", "
        return res[0:-2]

    elif query_parameter == "What is your name?":
        return "KFC V50"

    elif query_parameter == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"

    else:
        return "Unknown"
