from database import Base
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String

class Recipe(Base):
	__tablename__ = "recipe"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, nullable=False)
	calorie_adjustment = Column(Numeric(5,2))
	protein_adjustment = Column(Numeric(5,2))
	adjustment_reason = Column(String)

class Ingredient(Base):
	__tablename__ = "ingredient"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, nullable=False)
	uom = Column(String, nullable=False)
	calorie_density = Column(Numeric(5, 2), nullable=False) # The way the ingredient is used in preparing a recipe may change the value e.g deep frying chicken with oil, those information we later put inside Recipe itself as either deficit or additional nutrition during preparation
	protein_density = Column(Numeric(5, 2), nullable=False) # Same case

class RecipeIngredient(Base):
	"""Joint table"""
	__tablename__ = "recipe_ingredient"

	recipe_id = Column(Integer, ForeignKey("recipe.id"), primary_key=True)
	ingredient_id = Column(Integer, ForeignKey("ingredient.id"), primary_key=True)
	quantity = Column(Integer)

class InventoryLot(Base):
	__tablename__ = "inventory_lot"

	id = Column(Integer, primary_key=True, index=True)
	ingredient_id = Column(Integer, ForeignKey("ingredient.id"))
	quantity_purchased = Column(Numeric(6,2), nullable=False)
	quantity_remaining = Column(Numeric(6,2), nullable=False)
	total_price = Column(Numeric(5,2))
	purchased_at = Column(Date, nullable=False)
	expires_at = Column(Date)
	opened_at = Column(Date)
	consume_after_open = Column(Date) # Not sure if we could put this column to ingredient instead
