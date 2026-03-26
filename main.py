from flask import Flask
from flask_cors import CORS
from random import randint
from json import loads
import os

accounts = {}

app = Flask(__name__)
CORS(app)

@app.route("/<name>/<password>")
def crus(name, password):
    while True:
        ids = str(randint(999, 999999999999999999999999))
        if not ids in accounts:
            break
    accounts[name] = {"password": password, "id": ids, "data": {}}
    accounts[ids] = name
    return ids

@app.route("/login/<name>/<password>")
def lg(name, password):
    return accounts.get(name).get("id") if accounts.get("name").get("password") == password else "err"

@app.route("/addservice/<id>/<name>")
def adds(id, name):
    ids = accounts[id]
    usr = accounts[ids][data]
    usr[name] = {}
    return ids

@app.route("/getdata/<id>/<name>")
def gtd(id, name):
    ids = accounts[id]
    usr = accounts[ids][data][name]
    return usr

@app.route("/setdata/<id>/<name>/<path:path>")
def std(id, name, path):
    ids = accounts[id]
    usr = accounts[ids][data]
    usr[name] = loads(path)
    return f"{usr[name]}"

app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=False)
