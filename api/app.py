from flask import Flask, jsonify, render_template, request
import math
import re
import requests
from datetime import datetime


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    return render_template("hello.html", name=input_name, age=input_age)


@app.route('/submit2', methods=["POST"])
def submit2():
    user = request.form.get("github_name")
    # 使用函数参数 username 构建 GitHub API 的 URL
    url = f"https://api.github.com/users/{user}/repos"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            repos = response.json()  # 数据是 GitHub 仓库的列表
            for repo in repos:
                if repo.get("updated_at"):
                    t1 = '%Y-%m-%dT%H:%M:%SZ'
                    t2 = "%Y-%m-%d %H:%M:%S"
                    tp = datetime.strptime(repo["updated_at"], t1).strftime(t2)
                    repo["formatted_updated_at"] = tp
            return render_template('submit2.html', username=user, repos=repos)
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


@app.route('/search', methods=['POST'])
def search():
    # 从请求中获取搜索关键词
    query = request.form.get('search_value')
    # 使用GitHub API进行存储库搜索
    url = f'https://api.github.com/search/repositories?q={query}'
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # 提取有关存储库的信息
            repos = data['items']
            return render_template('search.html', query=query, repos=repos)
        else:
            # 返回一个错误消息
            return jsonify(error='Error: Unable to fetch data from GitHub API')
    except requests.exceptions.RequestException as e:
        # 返回一个错误消息
        return jsonify(error=f'Error: {str(e)}')


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
    large = r'Which of the following numbers is the largest: (\d+)(, \d+)*\?$'
    pattern_plus = r'What is \d+ plus \d+\?$'
    cubes = r'[A-Za-z\s]+ is both a square and a cube: (\d+)(, \d+)*\?$'
    prime = r'Which of the following numbers are primes: (\d+)(, \d+)*\?$'
    pattern_minus = r'What is \d+ minus \d+\?$'
    pattern_num = r'\d+'

    if re.match(pattern_multiplied, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        res = 1
        for i in matches:
            res = res * int(i)
        return str(res)

    elif re.match(large, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        int_ls = [int(i) for i in matches]
        return str(max(int_ls))

    elif re.match(pattern_plus, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        res = 0
        for i in matches:
            res = res + int(i)
        return str(res)

    elif re.match(cubes, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        res = ""
        for i in matches:
            i = int(i)
            square_root = round(math.sqrt(i), 5)
            cube_root = round(i ** (1/3), 5)
            if square_root.is_integer() and cube_root.is_integer():
                res = res + str(i) + ", "
        return res[0:-2]

    elif re.match(pattern_minus, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        return str(int(matches[0])-int(matches[1]))

    elif re.match(prime, query_parameter):
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
