import crud # Why from crud import ... doesn't work?
import models
from database import engine, Session

models.Base.metadata.create_all(bind=engine)

db = Session()

print("\nDiet Planner\n\n1. Add ingredient\n2. List ingredients\n0. Exit")

option = 42
while option:
	print("\n\nSelect option: ", end="")
	option = int(input())

	if option == 1:
		print("Ingredient name: ", end="")
		ingredient_name = input()
		crud.create_ingredient(ingredient_name=ingredient_name)
		print("\n\nIngredient created succesfully!")
	elif option == 2:
		print("ID    Ingredient")
		print(crud.list_ingredient)

print("\n\nGoodbye!")
db.close()