from models import Recipe, Ingredient, RecipeIngredient, session
from faker import Faker
import random

fake = Faker()

dietary_options = ['vegetarian', 'vegan', 'gluten-free', 'dairy-free', 'nut-free']

def seed_database():
    # Clear existing data
    session.query(RecipeIngredient).delete()
    session.query(Recipe).delete()
    session.query(Ingredient).delete()
    
    # Create common ingredients
    ingredients = [
        Ingredient(name='chicken'),
        Ingredient(name='rice'),
        Ingredient(name='tomato'),
        Ingredient(name='onion'),
        Ingredient(name='garlic'),
        Ingredient(name='pasta'),
        Ingredient(name='cheese'),
        Ingredient(name='bell pepper'),
        Ingredient(name='potato'),
        Ingredient(name='carrot'),
    ]
    session.add_all(ingredients)
    session.commit()
    
    # Create recipes
    for _ in range(10):
        recipe = Recipe(
            name=fake.bs(),
            instructions=fake.paragraph(nb_sentences=5),
            prep_time=random.randint(10, 120),
            dietary_restrictions=', '.join(random.sample(dietary_options, k=random.randint(0, 3)))
        )
        # Add 3-6 random ingredients to each recipe
        selected_ingredients = random.sample(ingredients, k=random.randint(3, 6))
        for ingredient in selected_ingredients:
            recipe.recipe_ingredients.append(RecipeIngredient(
                ingredient=ingredient,
                quantity=random.uniform(0.5, 4),
                unit=random.choice(['cups', 'tbsp', 'tsp', 'oz', 'lbs', 'grams'])
            ))
        
        session.add(recipe)
    
    session.commit()
    print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()