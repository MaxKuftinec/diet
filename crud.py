from sqlalchemy import select
from database import Session
from models import Ingredient

db = Session()

def create_ingredient(ingredient_name: str):
	new_ingredient = Ingredient(name=ingredient_name)

	db.add(new_ingredient)
	db.commit()
	db.close()

	return new_ingredient

def list_ingredient():
	list = db.scalars(select(Ingredient)).all()
	db.close()
	return list
