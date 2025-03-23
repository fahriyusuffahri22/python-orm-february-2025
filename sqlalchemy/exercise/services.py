from main import Session
from models import Recipe, Chef


def create_recipe(name, ingredients, instructions):
    with Session() as session:
        recipe = Recipe(
                name=name,
                ingredients=ingredients,
                instructions=instructions
        )
        session.add(recipe)
        session.commit()

        return recipe


def update_recipe_by_name(name, new_name,  new_ingredients, new_instructions):
    with Session() as session:
        session.query(Recipe).filter_by(name=name).update({
            'name':new_name,
            'ingredients':new_ingredients,
            'instructions':new_instructions
        })

        session.commit()


def delete_recipe_by_name(name):
    with Session() as session:
        session.query(Recipe).filter_by(name=name).delete()
        session.commit()


def get_recipes_by_ingredient(ingredient_name):
    with Session() as session:
        return session.query(Recipe).filter(Recipe.ingredients.contains(ingredient_name)).all()


def swap_recipe_ingredients_by_name(first_recipe_name, second_recipe_name):
    session = Session()

    try:
        session.begin()

        first_recipe = session.query(Recipe).filter_by(name=first_recipe_name).first()
        second_recipe = session.query(Recipe).filter_by(name=second_recipe_name).first()
        first_recipe.ingredients, second_recipe.ingredients = second_recipe.ingredients, first_recipe.ingredients

        session.commit()

    except Exception as error:
        session.rollback()
        raise error

    finally:
        session.close()


def relate_recipe_with_chef_by_name(recipe_name, chef_name):
    with Session() as session:
        recipe = session.query(Recipe).filter_by(name=recipe_name).first()

        if recipe.chef:
            raise Exception(f'Recipe: {recipe_name} already has a related chef')

        chef = session.query(Chef).filter_by(name=chef_name).first()
        recipe.chef = chef
        session.commit()

        return f'Related recipe {recipe_name} with chef {chef_name}'


def get_recipes_with_chef():
    with Session() as session:
        return '\n'.join(
            f'Recipe: {recipe_name} made by chef: {chef_name}'
            for recipe_name, chef_name in session
            .query(Recipe.name, Chef.name)
            .join(Chef, Recipe.chef)
            .all()
        )
