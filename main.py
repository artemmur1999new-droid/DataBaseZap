import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from random import randint

accounts = {}

app = Flask(__name__)
CORS(app)

# Проверка сервера
@app.route("/")
def home():
    return "Server is running"


# 🔹 Регистрация
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    name = data.get("name")
    password = data.get("password")

    if not name or not password:
        return jsonify({"status": "error", "message": "no_data"})

    if name in accounts:
        return jsonify({"status": "error", "message": "exists"})

    while True:
        ids = str(randint(999, 999999999999999999999999))
        if ids not in accounts:
            break

    accounts[name] = {
        "password": password,
        "id": ids,
        "data": {}
    }

    accounts[ids] = name

    return jsonify({"status": "ok", "id": ids})


# 🔹 Логин
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    name = data.get("name")
    password = data.get("password")

    user = accounts.get(name)

    if user and user.get("password") == password:
        return jsonify({"status": "ok", "id": user["id"]})

    return jsonify({"status": "error", "message": "invalid"})


# 🔹 Добавить сервис
@app.route("/addservice", methods=["POST"])
def add_service():
    data = request.json

    id = data.get("id")
    service = data.get("service")

    username = accounts.get(id)

    if not username:
        return jsonify({"status": "error", "message": "invalid_id"})

    accounts[username]["data"][service] = {}

    return jsonify({"status": "ok"})


# 🔹 Получить данные
@app.route("/getdata", methods=["POST"])
def get_data():
    data = request.json

    id = data.get("id")
    service = data.get("service")

    username = accounts.get(id)

    if not username:
        return jsonify({"status": "error", "message": "invalid_id"})

    return jsonify(accounts[username]["data"].get(service, {}))


# 🔹 Установить данные
@app.route("/setdata", methods=["POST"])
def set_data():
    data = request.json

    id = data.get("id")
    service = data.get("service")
    value = data.get("data")

    username = accounts.get(id)

    if not username:
        return jsonify({"status": "error", "message": "invalid_id"})

    accounts[username]["data"][service] = value

    return jsonify({"status": "ok"})


# 🔹 Запуск (Render / локально)
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
