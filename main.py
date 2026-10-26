"""Mainly handles CLI (display and input)"""

import models
from catalog import UNITS
from crud import create_ingredient, list_ingredient, create_recipe, list_recipe, update_ingredient, view_ingredient, view_recipe
from database import engine

models.Base.metadata.create_all(bind=engine)

def another_ingredient():
	another_ing = input()
	if another_ing == 'n':
		return 0
	elif another_ing != 'y':
		print("Input either y or n: ", end="")
		return another_ingredient()
	return 42

print(
"""
Diet Planner\n
1. Add ingredient
2. List ingredients
3. Update ingredient
4. Add recipe
5. List recipes
6. View recipes
0. Exit"""
	)

option = 42
while option:
	print("\nSelect option: ", end="")
	try:
		option = int(input())
	except:
		print("Input integer only")
		continue

	if option == 1:
		print("Ingredient name: ", end="")
		ingredient_name = input()
		print("Available Unit of Measurement (UoM)")
		print(f"\n{'ID':^3}|{'Unit':^5}")
		print("-" * 9)
		for index, unit in enumerate(UNITS):
			print(f"{index:^3}|{unit["unit"]:^5}")
		print("\nUoM ID: ", end="")
		uom_id = int(input())
		print("Calorie density per UoM: ", end="")
		calorie_density = int(input())
		print("Protein density per UoM: ", end="")
		protein_density = int(input())
		create_ingredient(ingredient_name, UNITS[uom_id]["unit"], calorie_density, protein_density)
		print("\nIngredient created succesfully!")
	elif option == 2:
		print(f"{'ID':^3}|{'Ingredient':^20}|{'Calorie':^7}|{'Protein':^7}|{'UoM':^5}|")
		print("-" * 47)
		ingredients = list_ingredient()
		for ingredient in ingredients:
			print(f"{ingredient.id:^3}|{ingredient.name:^20}|{ingredient.calorie_density:^7}|{ingredient.protein_density:^7}|{ingredient.uom:^5}|")
	elif option == 3:
		print("\nIngredient ID: ", end="")
		ingredient = view_ingredient(int(input()))
		print(f"\n{ingredient.name}")
		print("-" * 25)
		print(f"Calorie: {ingredient.calorie_density}kcal per 100g")
		print(f"Protein: {ingredient.protein_density}g per 100g")
		print("\nOnly input values for fields you want to change")
		print("Name: ", end="")
		ingredient_name = input()
		print("Calorie: ", end="")
		ingredient_calorie = input()
		try:
			ingredient_calorie = int(ingredient_calorie)
		except:
			ingredient_calorie = ""
		print("Protein: ", end="")
		ingredient_protein = input()
		try:
			ingredient_protein = int(ingredient_protein)
		except:
			ingredient_protein = ""
		update_value = update_ingredient(ingredient.id, ingredient_name, ingredient_calorie, ingredient_protein)
		print("\nIngredient updated succesfully!") if update_value else print("\nNo changes were made")
		ingredient = view_ingredient(ingredient.id)
		print(f"\n{ingredient.name}")
		print("-" * 25)
		print(f"Calorie: {ingredient.calorie_density}kcal per 100g")
		print(f"Protein: {ingredient.protein_density}g per 100g")

	elif option == 4:
		print("Recipe name: ", end="")
		recipe_name = input()
		# Before invoking create_recipe, we gotta ask for all the ingredients, and put it all in a list
		print("Available ingredients:")
		ingredients = list_ingredient()
		for ingredient in ingredients:
			print(f"{ingredient.id}    {ingredient.name}")
		
		ingredients = []
		ano_ing_counter = 42
		while ano_ing_counter:
			print("\nIngredient ID: ", end="")
			ingredient = view_ingredient(int(input()))
			print(f"Quantity ({ingredient.uom}): ", end="") # Make the unit change according to ingredient
			quantity = int(input())
			ingredients.append({"id": ingredient.id, "quantity": quantity})

			print("\nAdd another ingredient?: ", end="")
			ano_ing_counter = another_ingredient() # 0 if no, 42 if yes

		create_recipe(recipe_name=recipe_name, ingredients=ingredients)
		print("\nRecipe created succesfully!")
	elif option == 5:
		print("\nID    Recipe")
		recipes = list_recipe()
		for recipe in recipes:
			print(f"{recipe.id}    {recipe.name}")
	elif option == 6:
		print("\nRecipe ID: ", end="")
		recipe = view_recipe(int(input()))
		print(f"\n{recipe["name"]}")
		print("-" * 29)
		for ingredient in recipe["ingredients"]:
			print(
				f"{ingredient["name"]:<20}"
				f"{ingredient["quantity"]:>3} {ingredient["uom"]}"
			)
		print(f"\nEstimated total calorie: {recipe["total_calorie"]}kcal")
		print(f"Estimated total protein: {recipe["total_protein"]}g")

print("\nGoodbye!")
