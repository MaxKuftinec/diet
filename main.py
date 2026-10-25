import models
from crud import create_ingredient, list_ingredient, create_recipe, list_recipe, view_recipe
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
3. Add recipe
4. List recipes
5. View recipes
0. Exit
	"""
	)

option = 42
while option:
	print("Select option: ", end="")
	try:
		option = int(input())
	except:
		print("Input integer only")
		continue

	if option == 1:
		print("Ingredient name: ", end="")
		ingredient_name = input()
		create_ingredient(ingredient_name=ingredient_name)
		print("\nIngredient created succesfully!")
	elif option == 2:
		print("ID    Ingredient")
		ingredients = list_ingredient()
		for ingredient in ingredients:
			print(f"{ingredient.id}    {ingredient.name}")
	elif option == 3:
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
			ingredient_id = int(input()) # PostgreSQL can accept integer as string, but let's convert it beforehand
			print("Quantity (g): ", end="")
			quantity = int(input())
			ingredients.append({"id": ingredient_id, "quantity": quantity})

			print("\nAdd another ingredient?: ", end="")
			ano_ing_counter = another_ingredient() # 0 if no, 42 if yes

		create_recipe(recipe_name=recipe_name, ingredients=ingredients)
		print("\nRecipe created succesfully!")
	elif option == 4:
		print("\nID    Recipe")
		recipes = list_recipe()
		for recipe in recipes:
			print(f"{recipe.id}    {recipe.name}")
	elif option == 5:
		print("\nRecipe ID: ", end="")
		recipe_id = int(input())
		recipe = view_recipe()
		print(
			f"""\n{recipe.name}
			\n------------------------
			\n"""
		)


print("\nGoodbye!")
