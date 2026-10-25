from sqlalchemy import select
from database import Session
from models import Recipe, Ingredient, RecipeIngredient

def create_ingredient(ingredient_name: str):
	with Session.begin() as db:
		new_ingredient = Ingredient(name=ingredient_name)
		db.add(new_ingredient)

def list_ingredient():
	with Session() as db:
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
	with Session() as db:
		return db.scalars(select(Recipe)).all()

def view_recipe(id: int): # We also need to return it's corresponding ingredients
	with Session() as db:
		recipe = db.get(Recipe, id)
		recipe_ingredients = db.scalars(
			select(RecipeIngredient).where(RecipeIngredient.recipe_id==recipe.id)
		).all()
		# RecipeIngredient is not ingredient, so we have to query ingredients from all RecipeIngredient objects we have received
		#	{"ingredient": (db.get(Ingredient, ingredient.ingredient_id)), "quantity": ingredient.quantity_g}
		#	[{"ingredient": Ingredient object, "quantity": "250"}]
		ingredients = []
		for ingredient in recipe_ingredients:
			ingredients.append(
				{
					"ingredient": (db.get(Ingredient, ingredient.ingredient_id)),
					"quantity": ingredient.quantity_g
				}
			)
		return {"name": recipe.name, "ingredients": ingredients}
