from sqlalchemy import select
from database import Session
from models import Recipe, Ingredient, RecipeIngredient

def create_ingredient(ingredient_name: str):
	with Session.begin() as db:
		new_ingredient = Ingredient(name=ingredient_name)
		db.add(new_ingredient)
		return new_ingredient

def list_ingredient():
	with Session.begin() as db:
		return db.scalars(select(Ingredient)).all()

def create_recipe(recipe_name: str, ingredients: list):
	with Session.begin() as db:
		recipe = Recipe(name=recipe_name)

		db.add(recipe)
		db.flush() # Flush allows creation of id without comitting the object in db
		for ingredient in ingredients:
			new_recipe_ingredient = RecipeIngredient(recipe_id=recipe.id, ingredient_id=ingredient["id"], quantity_g=ingredient["quantity"])
			db.add(new_recipe_ingredient)

def list_recipe():
	with Session.begin() as db:
		return db.scalars(select(Recipe)).all()

def view_recipe(recipe_id: int): # We also need to return it's corresponding ingredients
	with Session.begin() as db:
		return Recipe(id=recipe_id)
