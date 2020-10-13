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
            "id": self.id,
            "name": self.name,
            "category": self.category
        }

db.connect()
db.create_tables([Recipe], safe=True)
db.close()