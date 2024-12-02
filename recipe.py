import streamlit as st
from google.cloud import bigquery

client = bigquery.Client('frankinyiama')


class Recipe:
    def __init__(self, name, calorie, protein, ingredients, time, directions):
        self.name = name
        self.calorie = calorie
        self.protein = protein
        self.ingredients = ingredients
        self.time = time
        self.directions = directions

    def __str__(self):
        result = f'''
        Name: {self.name}\n
        Calorie: {self.calorie}cal\n
        Protein: {self.protein}g\n
        Ingredients: {self.ingredients}\n
        Time: {self.time} minutes\n
        Directions: {self.directions}
        '''
        return result


def print_recipe(recipe):
    st.subheader(recipe.name)
    st.write('Calorie: ' + str(recipe.calorie) + 'cal')
    st.write('Protein: ' + str(recipe.protein) + 'g')
    st.write('Ingredients:')
    st.markdown("<ul><li>" + "</li><li>".join(recipe.ingredients) + "</li></ul>", unsafe_allow_html=True)
    st.write('Time: ' + str(recipe.time) + ' minutes')
    st.write('Directions:')
    st.markdown("<ul><li>" + "</li><li>".join(recipe.directions) + "</li></ul>", unsafe_allow_html=True)


def download_recipe(recipe):
    result = f'''
        Name: {recipe.name}\n
        Calorie: {recipe.calorie}cal\n
        Protein: {recipe.protein}g\n
        Ingredients: {recipe.ingredients}\n
        Time: {recipe.time} minutes\n
        Directions: {recipe.directions}
        '''

    return result


def save_recipe(recipe_name, recipe_calorie, recipe_protein, recipe_ingredients, recipe_time, recipe_directions):
    check_query = 'SELECT name FROM `frankinyiamatechx2024.recipes.recipe_table`'

    QUERY = (check_query)
    query_job = client.query(QUERY)
    recipe_names = query_job.result()

    names = []
    for val in recipe_names:
        names.append(val.name)

    if recipe_name in names:
        st.warning('This recipe already exists')
    else:
        my_query = f"INSERT INTO `frankinyiama.recipes.recipe_table` (name, calorie, protein, ingredients, time, directions) VALUES ('{recipe_name}', '{recipe_calorie}', '{recipe_protein}', '{recipe_ingredients}', '{recipe_time}', '{recipe_directions}')"

        QUERY = (my_query)
        query_job = client.query(QUERY)
        rows = query_job.result()
        st.success('Recipe saved!', icon="📩")


def list_to_string(lst):
    result = ''
    for element in lst:
        result += element + '***'
    if result:
        result = result[:-3]
    return result


def get_recipe():
    my_query = 'SELECT name, calorie, protein, ingredients, time, directions FROM `frankinyiama.recipes.recipe_table`'

    QUERY = (my_query)
    query_job = client.query(QUERY)
    rows = query_job.result()

    recipes = []
    for row in rows:
        ingredients = row.ingredients.split('***')
        directions = row.directions.split('***')
        recipe = Recipe(row.name, row.calorie, row.protein, ingredients, row.time, directions)
        recipes.append(recipe)
    return recipes


def delete_recipe(name):
    my_query = f"DELETE FROM `frankinyiama.recipes.recipe_table` WHERE name = '{name}'"

    QUERY = (my_query)
    query_job = client.query(QUERY)
    rows = query_job.result()

    st.info('Recipe deleted!', icon="🗑️")