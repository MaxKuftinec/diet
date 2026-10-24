from sqlalchemy import select
from main import db
from models import Ingredient

def create_ingredient(ingredient_name: str):
	new_ingredient = Ingredient(name=ingredient_name)

	db.add(new_ingredient)
	db.commit()

	return new_ingredient

def list_ingredient():
	return db.scalars(select(Ingredient)),all()
