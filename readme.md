# Recipe 

This will be a recipe in two parts. First a simple server to store and list recipes. Second also a recipe for a basic Flask server.

## Flask

Flask is a minimalistic library to programmatically respond to HTTP requests in Python.
It isn't the only option for this. If you prefer JavaScript, Node.js has a popular library called Express. 
If you need a more complete, though more complicated, solution in Python Django does everything Flask does along with managing a database
with features like an auto generated admin interface.

## HTTP

HTTP is how a lot of the web communicates. Each request consists of a url (domain name, and path) a, method used to identify the rquest,
often a body containing extra information, and a list of headers (a list of string fields with values)

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
* Now lets change what it returns: `return jsonify({"time": 0})`
* Load `http://localhost:5000/time` and we should see the result.
* Of couse we can still load `http://localhost:5000/` to see the old route

### Return useful things

Right now we aren't returning the actual time. Let's do that. Here time is unix time

* First we need to immport `time`: `import time`
* `time.time()` gives us a double corresponding to the [unix time](https://en.wikipedia.org/wiki/Unix_time)
* We can just replace `0` in the JSON with it: `return jsonify({"time": time.time()})`
* We can also round down to an int by using `int()` to convert `return jsonify({"time": int(time.time())})`

### Recipes

What we have now is well and good, but it would be nice to be able to save data. Doing that will expose all sorts of different options.
To actually store the data I'll be using a library called `Peewee`. There are a lot of other options including raw `SQL`, `MongoDB`, `Redix` 
and many more. Each has benefits and problems.

* First we need to install `Peewee`: `pip install peewee`
* Next lets add a new file to the `src` folder. Name it `db.py`
* First we are going to import `Peewee` We're lazy so we're just importing everything in it: `from peewee import *`
* Now we need to reference a `SQL` db. More choices here, but we're going to make the lazy one again: `db = SqliteDatabase('recipe.db')`
* We're going to create an entire class to be the base for everything else

        class BaseModel(Model):
            class Meta:
                database = db

* Finally lets add a class to represent our data

        class Recipe(BaseModel):
            name = CharField()
            category = CharField()

* We need to tell Peewee to create a table for this class: `db.create_table(Recipe, safe=True)`

### Test it

Python is a scripting language and like many we don't actually need to make a file to test it. Lets quickly check that our DB model is working

* Open your command prompt and cd into the src folder: `cd src`
* Launch python: `python`
* Import the file we made: `import db`
* Create an instance of a recipe: `cookies = db.Recipe(name="Chocolate", category="Cookies")`
* Save the cookie: `cookies.save()`
* You might notice that it prints one. This means everything went well and is because python when run in this mode
prints the value of every expression
* If you want to add a few more feel free.
* We can list these by typing `db.Recipe.select().where(db.Recipe.name=="Cookies")`, but we'll get something weird
* Instead to actually list features of each we have to use a loop: `for cookie in db.Recipe.select().where(db.Recipe.name=="Chocolate"):`
* Press enter and we'll see a some funny dots. Press tab to indent a line and type `print(cookie.name)` then enter twice
* Deleting items works similarly only we use delete instead of select and we must call execute on the result like: 
`db.Recipe.delete().where(db.Recipe.name=="Chocolate").execute()`
* To exit we can press `control-d` or type `exit()`

### Use it

Lets actually save something given us by the user. We'll talk about a lot so get ready

* Open the app.py file back up
* Again we're going to copy an existing route and modify it
* Set the route to `/recipe` and we also need to set the method to POST: `@app.route("/recipe", methods=["POST"])`
* Change the function to be named something like `add_recipe`: `def add_recipe():`
* At the top of the file import `Recipe`: `from db import Recipe`
* Also import `request` from `flask` so we can get info about the current request like the JSON they send: `from flask import Flask, jsonify, request`
* 

