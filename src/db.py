from peewee import *

db = SqliteDatabase('recipe.db')

class BaseModel(Model):
    class Meta:
        database = db

class Recipe(BaseModel):
    name = CharField()
    category = CharField()
    def to_dictionary(self):
        return {
            "name": self.name,
            "category": self.category
        }


db.create_table(Recipe, safe=True)
db.connect()