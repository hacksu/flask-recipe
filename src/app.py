from flask import Flask, jsonify, request, render_template, redirect # similar to a include but getting a particular item exported. Could do import flask, but then flask.Flask instead of just Flask
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
    recipe = Recipe(name=request.form["name"], category=request.form["category"])
    recipe.save()
    return redirect('/recipe')


@app.route("/recipe")
def get_recipes():
    recipes = []
    for recipe in Recipe.select():
        recipes.append(recipe.to_dictionary())
    return render_template('recipes.html', recipes=recipes)

@app.route("/recipe/delete/<int:id>")
def delete_recipes(id):
    jsonify({"n": Recipe.delete().where(Recipe.id==id).execute()})
    return redirect('/recipe')

if __name__ == '__main__':
    app.run(debug=True)