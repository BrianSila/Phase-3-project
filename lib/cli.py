import click
from helpers import (
    add_recipe, get_all_recipes, search_by_ingredient,
    filter_by_dietary_restriction, get_recipe_details
)

@click.group()
def cli():
    """Recipe Manager CLI - Store and search recipes with ingredients"""
    pass

@cli.command()
@click.option('--name', prompt='Recipe name', help='Name of the recipe')
@click.option('--instructions', prompt='Instructions', help='Cooking instructions')
@click.option('--prep-time', prompt='Preparation time (minutes)', type=int, help='Prep time in minutes')
@click.option('--dietary', prompt='Dietary restrictions (comma separated)', default='', help='Dietary restrictions')
def add(name, instructions, prep_time, dietary):
    """Add a new recipe"""
    ingredients = []
    click.echo("Add ingredients (leave name blank when done):")
    while True:
        ing_name = click.prompt("Ingredient name", default='', show_default=False)
        if not ing_name:
            break
        quantity = click.prompt("Quantity", type=float)
        unit = click.prompt("Unit (cups, tbsp, etc.)")
        ingredients.append((ing_name, quantity, unit))
    
    recipe = add_recipe(name, instructions, prep_time, dietary, ingredients)
    click.echo(f"Successfully added recipe: {recipe.name}")

@cli.command()
def list_all():
    """List all recipes"""
    recipes = get_all_recipes()
    if not recipes:
        click.echo("No recipes found.")
        return
    
    for recipe in recipes:
        click.echo(f"{recipe.id}: {recipe.name} ({recipe.prep_time} mins)")

@cli.command()
@click.argument('ingredient')
def search(ingredient):
    """Search recipes by ingredient"""
    recipes = search_by_ingredient(ingredient)
    if not recipes:
        click.echo(f"No recipes found with ingredient: {ingredient}")
        return
    
    click.echo(f"Recipes containing {ingredient}:")
    for recipe in recipes:
        click.echo(f"{recipe.id}: {recipe.name}")

@cli.command()
@click.argument('restriction')
def filter(restriction):
    """Filter recipes by dietary restriction"""
    recipes = filter_by_dietary_restriction(restriction)
    if not recipes:
        click.echo(f"No {restriction} recipes found.")
        return
    
    click.echo(f"{restriction.capitalize()} recipes:")
    for recipe in recipes:
        click.echo(f"{recipe.id}: {recipe.name}")

@cli.command()
@click.argument('recipe_id', type=int)
def details(recipe_id):
    """Show detailed recipe information"""
    recipe = get_recipe_details(recipe_id)
    if not recipe:
        click.echo(f"Recipe with ID {recipe_id} not found.")
        return
    
    click.echo(f"\nRecipe: {recipe['name']}")
    click.echo(f"Prep time: {recipe['prep_time']}")
    click.echo(f"Dietary restrictions: {recipe['dietary_restrictions']}")
    
    click.echo("\nIngredients:")
    for ing in recipe['ingredients']:
        click.echo(f"- {ing['quantity']} {ing['unit']} {ing['name']}")
    
    click.echo("\nInstructions:")
    click.echo(recipe['instructions'])

if __name__ == '__main__':
    cli()