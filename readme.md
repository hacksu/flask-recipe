# Recipe 

This will be a recipe in two parts. First a simple server to store and list recipes. Second also a recipe for a basic Flask server.

## Flask

Flask is a minimalistic library to programtically respond to HTTP requests in Python.
It isn't the only option for this. If you prefer JavaScript, Node.js has a popular library called Express. 
If you need a more complete, though more complicated, solution in Python Django does everything Flask does along with managing a database
with features like an auto generated admin interface.

## HTTP

HTTP is how a lot of the web comunicates. Each request consistes of a url (domain name, and path) a, method used to identify the rquest,
often a body containing exra information, and a list of headers (a list of string fields with values)

## HTTP Methods

* [OPTIONS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS): Information about the requested route
* [GET](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET): Getting the selected information
* HEAD: Same as get accept only returning the header, no body sent. Can be used for meta information like file size
* PATCH: Meant to change an existing 
* [POST](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST): Data sent to the server. The type of request usually made when forms are submitted
* PUT: Similar to post, but intend to be particular to saving data at a particular url
* DELETE: Just what it sounds like. Requests that the server delete the resource
* TRACE: Web server should just echo the request
* CONNECT: Reserved for use by proxies

The biggest practical difference between POST and GET is that POST allows for much more data to be sent in the body. In fact, JavaScript will only allow you
to send data in the body as part of POST request or similar

## Setup

* Install Python: https://www.python.org/
* Download starter project: https://github.com/hacksu/flask-recipe
* Open command prompt, Powershell, similar.
* Run: `pip install flask flask_cors`
* CD into into the directory you downloaded
 * example: `cd Downloads/flask-recipe`
* Run the server: `python src/app.py`
* Open `http://localhost:5000/`
* You should see hello world

## Project

### jsonify

Right now we're returning a string. This is fine for many cases. We could return an entire HTML website, but what is being done
a lot now is building the entire frontend in JS and HTML and just sending the data to it as needed. It can make it easier to 
implement mobile apps and similar. Flask will let us return JSON, which is a lot easier for other programs to use. We just need to make
a few changes. 

* Import `jsonify` so we can convert python dictionaries to JSON: `from flask import Flask, jsonify`
* Return JSON from our hello world route. `return jsonify({"message": "hello world"})`
* We don't need to restart the server (probably), because we started flask in debug mode it will reload when we change the file
* Reload the URL and we should see JSON


### Another route

Obviously a web server isn't very interesting if it can only return one thing. Lets add a route to tell us the time

* To start just copy and paste the entire hello world route
* We have to change the name of the function as we can't have two with the same name: `def get_time():`
* We also should change where the route is mapped to: `@app.route("/time")`
* Now lets change what it returns 