from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String

class Recipe(Base):
	__tablename__ = "recipe"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)

class Ingredient(Base):
	__tablename__ = "ingredient"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)

class RecipeIngredient(Base):
	"""Joint table"""
	__tablename__ = "recipe_ingredient"

	# id = Column(Integer, primary_key=True, index=True)
	recipe_id = Column(Integer, ForeignKey("recipe.id"), primary_key=True)
	ingredient_id = Column(Integer, ForeignKey("ingredient.id"), primary_key=True)
	quantity_g = Column(Integer)# Quantity as gram, for now...
