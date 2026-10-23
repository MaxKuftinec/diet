from sqlalchemy import select
from database import Session
from models import Ingredient

def create_ingredient(ingredient_name: str):
	new_ingredient = Ingredient(name=ingredient_name)

	Session.add(new_ingredient)
	Session.commit()

	return new_ingredient

def list_ingredient():
	return Session.scalars(select(Ingredient).all())
