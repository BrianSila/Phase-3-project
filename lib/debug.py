from db.models import session, Recipe, Ingredient, RecipeIngredient

def debug_queries():
    """Helper function for debugging database queries"""
    print("Recipes:")
    for recipe in session.query(Recipe).all():
        print(f"{recipe.id}: {recipe.name}")
        for ri in recipe.recipe_ingredients:
            print(f"  - {ri.quantity}{ri.unit} {ri.ingredient.name}")
    
    print("\nIngredients:")
    for ingredient in session.query(Ingredient).all():
        print(f"{ingredient.id}: {ingredient.name}")

if __name__ == '__main__':
    debug_queries()