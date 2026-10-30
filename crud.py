from datetime import date
from decimal import Decimal
from sqlalchemy import select
from database import Session
from models import InventoryLot, Recipe, Ingredient, RecipeIngredient

def create_ingredient(ingredient_name: str, uom: str, calorie_density: int, protein_density: int):
	with Session.begin() as db:
		new_ingredient = Ingredient(name=ingredient_name, uom=uom, calorie_density=calorie_density, protein_density=protein_density)
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
			new_recipe_ingredient = RecipeIngredient(recipe_id=recipe.id, ingredient_id=ingredient["id"], quantity=ingredient["quantity"])
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
		#	{"ingredient": (db.get(Ingredient, ingredient.ingredient_id)), "quantity": ingredient.quantity}
		#	[{"ingredient": Ingredient object, "quantity": "250"}]
		ingredients = []
		total_calorie = 0
		total_protein = 0
		for ingredient in recipe_ingredients:
			ing = db.get(Ingredient, ingredient.ingredient_id)
			calorie = ing.calorie_density * ingredient.quantity
			protein = ing.protein_density * ingredient.quantity
			ingredients.append(
				{
					"name": ing.name,
					"quantity": ingredient.quantity,
					"uom": ing.uom,
					"calorie": calorie,
					"protein": protein
				}
			)
			total_calorie += calorie
			total_protein += protein
		return {"name": recipe.name, "ingredients": ingredients, "total_calorie": total_calorie, "total_protein": total_protein}

def create_inventory(ingredient_id: int, quantity_purchased: Decimal, total_price: Decimal, purchased_at: date, expires_at: date):
	db = Session()
	inventory = InventoryLot(
		ingredient_id=ingredient_id,
		quantity_purchased=quantity_purchased,
		quantity_remaining=quantity_purchased,
		total_price=total_price,
		purchased_at=purchased_at if purchased_at else date.today(),
		expires_at=expires_at
	)
	db.add(inventory)
	db.commit()
	id = inventory.id
	db.close()
	return view_inventory_lot(id)

def view_inventory_lot(id: int):
	with Session() as db:
		lot = db.get(InventoryLot, id)
		return {
			"name": db.get(Ingredient, lot.ingredient_id).name,
			"quantity_purchased": lot.quantity_purchased,
			"quantity_remaining": lot.quantity_remaining,
			"price": lot.total_price,
			"purchased_at": lot.purchased_at,
			"expire": lot.expires_at,
			"opened": lot.opened_at,
			"consume_after_open": lot.consume_after_open
		}

def list_inventory():
	with Session() as db:
		return db.scalars(select(InventoryLot)).all()
