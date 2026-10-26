from sqlalchemy import select
from database import Session
from models import Recipe, Ingredient, RecipeIngredient

def create_ingredient(ingredient_name: str, calorie_density: int, protein_density: int):
	with Session.begin() as db:
		new_ingredient = Ingredient(name=ingredient_name, calorie_density=calorie_density, protein_density=protein_density)
		db.add(new_ingredient)

def list_ingredient():
	with Session() as db:
		return db.scalars(select(Ingredient)).all()

def view_ingredient(ingredient_id: int):
	with Session() as db:
		return db.get(Ingredient, ingredient_id)

def update_ingredient(ingredient_id: int, ingredient_name: str, ingredient_calorie: int, ingredient_protein: int):
	with Session.begin() as db:
		ingredient = db.get(Ingredient, ingredient_id)
		update_value = 0
		if ingredient_name:
			ingredient.name = ingredient_name
			update_value = 42
		if ingredient_calorie:
			ingredient.calorie_density = ingredient_calorie
			update_value = 42
		if ingredient_protein:
			ingredient.protein_density = ingredient_protein
			update_value = 42
		return update_value

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
		recipe = db.get(Recipe, id) # This still hasn't handle nonexisten id, so it may return None
		recipe_ingredients = db.scalars(
			select(RecipeIngredient).where(RecipeIngredient.recipe_id==recipe.id)
		).all()
		# RecipeIngredient is not ingredient, so we have to query ingredients from all RecipeIngredient objects we have received
		#	{"ingredient": (db.get(Ingredient, ingredient.ingredient_id)), "quantity": ingredient.quantity_g}
		#	[{"ingredient": Ingredient object, "quantity": "250"}]
		ingredients = []
		total_calorie = 0
		total_protein = 0
		for ingredient in recipe_ingredients:
			ing = db.get(Ingredient, ingredient.ingredient_id)
			calorie = ing.calorie_density * ingredient.quantity_g / 100
			protein = ing.protein_density * ingredient.quantity_g / 100
			ingredients.append(
				{
					"name": ing.name,
					"quantity": ingredient.quantity_g,
					"calorie": calorie,
					"protein": protein
				}
			)
			total_calorie += calorie
			total_protein += protein
		return {"name": recipe.name, "ingredients": ingredients, "total_calorie": total_calorie, "total_protein": total_protein}
