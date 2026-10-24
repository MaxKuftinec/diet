from sqlalchemy import select
from database import Session
from models import Recipe, Ingredient, RecipeIngredient

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

def create_recipe(recipe_name: str, ingredients: list):
	recipe = Recipe(name=recipe_name)

	db.add(recipe)
	db.flush() # Flush allows creation of id without comitting the object in db
	for ingredient in ingredients:
		new_recipe_ingredient = RecipeIngredient(recipe_id=recipe.id, ingredient_id=ingredient["id"], quantity_g=ingredient["quantity"])
		db.add(new_recipe_ingredient)

	# Before exiting method, commit and close session
	db.commit()
	db.close()
