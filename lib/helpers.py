from db.models import session, Recipe, Ingredient, RecipeIngredient

def add_recipe(name, instructions, prep_time, dietary_restrictions, ingredients):
    """Add a new recipe to the database"""
    recipe = Recipe(
        name=name,
        instructions=instructions,
        prep_time=prep_time,
        dietary_restrictions=dietary_restrictions
    )
    
    for ing_name, quantity, unit in ingredients:
        ingredient = session.query(Ingredient).filter_by(name=ing_name.lower()).first()
        if not ingredient:
            ingredient = Ingredient(name=ing_name.lower())
            session.add(ingredient)
        
        recipe.recipe_ingredients.append(RecipeIngredient(
            ingredient=ingredient,
            quantity=quantity,
            unit=unit
        ))
    
    session.add(recipe)
    session.commit()
    return recipe

def get_all_recipes():
    """Return all recipes"""
    return session.query(Recipe).all()

def search_by_ingredient(ingredient_name):
    """Search recipes by ingredient"""
    return session.query(Recipe).join(RecipeIngredient).join(Ingredient).filter(
        Ingredient.name.ilike(f'%{ingredient_name.lower()}%')
    ).all()

def filter_by_dietary_restriction(restriction):
    """Filter recipes by dietary restriction"""
    return session.query(Recipe).filter(
        Recipe.dietary_restrictions.ilike(f'%{restriction.lower()}%')
    ).all()

def get_recipe_details(recipe_id):
    """Get full details for a specific recipe"""
    recipe = session.query(Recipe).filter_by(id=recipe_id).first()
    if recipe:
        return {
            'name': recipe.name,
            'instructions': recipe.instructions,
            'prep_time': f"{recipe.prep_time} minutes",
            'dietary_restrictions': recipe.dietary_restrictions or 'None',
            'ingredients': [
                {
                    'name': ri.ingredient.name,
                    'quantity': ri.quantity,
                    'unit': ri.unit
                } for ri in recipe.recipe_ingredients
            ]
        }
    return None