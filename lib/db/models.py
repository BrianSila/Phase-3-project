
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    instructions = Column(String)
    prep_time = Column(Integer)  # in minutes
    dietary_restrictions = Column(String)  # comma-separated values
    
    # Relationships
    recipe_ingredients = relationship('RecipeIngredient', back_populates='recipe', cascade='all, delete-orphan')
    ingredients = association_proxy('recipe_ingredients', 'ingredient')
    
    def __repr__(self):
        return f"<Recipe {self.id}: {self.name}>"


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    # Relationships
    recipe_ingredients = relationship('RecipeIngredient', back_populates='ingredient')
    recipes = association_proxy('recipe_ingredients', 'recipe')
    
    def __repr__(self):
        return f"<Ingredient {self.id}: {self.name}>"
class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'
    
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))
    quantity = Column(Float)
    unit = Column(String)
    
    # Relationships
    recipe = relationship('Recipe', back_populates='recipe_ingredients')
    ingredient = relationship('Ingredient', back_populates='recipe_ingredients')
    
    def __repr__(self):
        return f"<RecipeIngredient {self.recipe.name} - {self.ingredient.name}: {self.quantity}{self.unit}>"

# Database setup
engine = create_engine('sqlite:///recipe_manager.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()