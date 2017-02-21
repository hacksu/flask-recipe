from flask import Flask # similar to a include but getting a particular item exported. Could do import flask, but then flask.Flask instead of just Flask

app = Flask(__name__) # Create the server object


@app.route("/")
def hello_world():
    return "hello world"


if __name__ == '__main__':
    app.run(debug=True)