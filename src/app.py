from flask import Flask, jsonify, request # similar to a include but getting a particular item exported. Could do import flask, but then flask.Flask instead of just Flask
import time
from db import Recipe

app = Flask(__name__) # Create the server object


@app.route("/")
def hello_world():
    return jsonify({"message": "hello world"})

@app.route("/time")
def get_time():
    return jsonify({"time": int(time.time())})

@app.route("/recipe", methods=["POST"])
def add_recipe():
    json = request.get_json()
    recipe = Recipe(name=json["name"], category=json["category"])
    recipe.save()
    return jsonify({"id": recipe.id})

if __name__ == '__main__':
    app.run(debug=True)