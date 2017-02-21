from flask import Flask, jsonify # similar to a include but getting a particular item exported. Could do import flask, but then flask.Flask instead of just Flask
import time

app = Flask(__name__) # Create the server object


@app.route("/")
def hello_world():
    return jsonify({"message": "hello world"})

@app.route("/time")
def get_time():
    return jsonify({"time": int(time.time())})

if __name__ == '__main__':
    app.run(debug=True)