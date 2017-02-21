from peewee import *

db = SqliteDatabase('recipe.db')

class BaseModel(Model):
    class Meta:
        database = db

class Recipe(BaseModel):
    name = CharField()
    category = CharField()
    

db.connect()