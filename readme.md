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
* Create a folder for this project
* Open command prompt, Powershell, similar.
* Navigate to the folder you created and run: `mkdir src`
* Run: `pip install flask flask_cors peewee`
* Inside the src folder, create a file named `app.py`
* Paste:

                from flask import Flask, jsonify, request, render_template, redirect
                import time
                from db import Recipe

                app = Flask(__name__) # Create the server object


                @app.route("/")
                def hello_world():
                    return jsonify({"message": "hello world"})
                
                if __name__ == '__main__':
                    app.run(debug=True)

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

* We need to tell Peewee to create a table for this class: `db.create_tables([Recipe], safe=True)`

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
* To exit we can press `exit()`

### Post it

Let's actually save something given us by the user. We'll talk about a lot so get ready

* Open the app.py file back upchan
* Again we're going to copy an existing route and modify it
* Set the route to `/recipe` and we also need to set the method to POST: `@app.route("/recipe", methods=["POST"])`
* Change the function to be named something like `add_recipe`: `def add_recipe():`
* At the top of the file import `Recipe`: `from db import Recipe`
* Also import `request` from `flask` so we can get info about the current request like the JSON they send: `from flask import Flask, jsonify, request, render_template, redirect`
* Before we go any farther try loading `http://localhost:5000/recipe`. You should get an error. Something like this method not allowed
this is because browsers always make `GET` requests and we're only listening for `POST`
* Make a new recipe: `recipe = Recipe(name=json["name"], category=json["category"])`
* Save that: `recipe.save()`
* Now every time we post something to it we save a new recipe.

### Show the recipes we've saved

We need to actually show the recipes. I've found the easiest way to do this is to add a method to our Recipe class.

* Open up `db.py`
* Add the first line of our method: `def to_dictionary(self):`
* The `self` will be a reference to the class
* After that add an indent and return

        return {
            "id": self.id,
            "name": self.name,
            "category": self.category
        }
* This is the way to define a Dictionary in python. It might look like JSON and infact it is very close but it isn't.
* Now back in `app.py` lets copy the `add_recipe` route, but remove the methods field and change the name

        @app.route("/recipe")
        def get_recipes():
            recipes = []
            for recipe in Recipe.select():
                recipes.append(recipe.to_dictionary())
            recipe.save()
            return render_template('recipes.html', recipes=recipes)

* Obviously we need to change the actual contents too. Remember how we played around earlier. We can do the same thing here except we need to
store the dictionaries for each recipe instead of printing their names
* First create an list to store it in (python's expandable array): `recipes = []`
* Next add the loop to find all the recipes: `for recipe in Recipe.select()`. We don't need a `where` here because we aren't filtering by anything
* Inside the loop call the append method on `recipes` to add each recipe's 
dictionary representation: `recipes.append(recipe.to_dictionary())`
* Finaly last but not least jsonify the whole thing and return it: `return jsonify({"recipes": recipes})`

### Delete the bad

There's one more thing we can't do right now. Delete old recipes

      @app.route("/recipe/delete/<int:id>")
      def delete_recipes(id):
          jsonify({"n": Recipe.delete().where(Recipe.id==id).execute()})
          return redirect('/recipe')

