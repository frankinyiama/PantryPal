import streamlit as st
import google.generativeai as genai
from google.cloud import bigquery
from PIL import Image
from streamlit_tags import st_tags
from recipe import *
from shared_func import *

st.title("Pantry Pal")

generate_new_recipes, view_saved_recipes = st.tabs(["Generate new recipe", "View saved recipes"])

with view_saved_recipes:
    count = 0
    recipe_list = get_recipe()
    if not recipe_list:
        st.info('You have no saved recipes.')
    else:
        for recipe in recipe_list:
            count += 1
            with st.expander(recipe.name):
                print_recipe(recipe)
                recipe_download = download_recipe(recipe)
                download, delete = st.columns(2, gap='large')
                with download:
                    st.download_button('Download recipe', recipe_download, file_name=recipe.name,
                                       key=recipe.name + ' download ' + str(count))
                with delete:
                    delete_button = st.button('Delete recipe', key=recipe.name + ' delete' + str(count))
                    if delete_button:
                        delete_recipe(recipe.name)

with generate_new_recipes:
    ingredients_from_text = st_tags(
        label='# Input Ingredients by text',
        text='Press enter to add more',
        maxtags=100,
    )

    st.header("Input ingredients by uploading a picture from device")
    picture_from_device = st.file_uploader("Upload a picture of your pantry!")
    ingredients_from_upload = []

    if picture_from_device:
        ingredients_from_upload = process_picture(picture_from_device)

    st.header("Input ingredients by taking a picture of your pantry")
    picture_from_camera = st.camera_input("Take a picture of your pantry!")
    ingredients_from_pantry = []

    if picture_from_camera:
        ingredients_from_pantry = process_picture(picture_from_device)

    ingredients = ingredients_from_text + ingredients_from_upload + ingredients_from_pantry

    recipe_query = '''

        Generate various recipes utilizing these ingredients listed ''' + str(ingredients) + '''
        Return the result as a list of dictionaries containing recipes in the following format:
        [
            {
                name: String containing the name of the recipe
                calorie: Integer of the amount of calories in unit cal
                protein: Integer of the anount of protein in unit grams
                ingredients: A list of all ingredients used in the recipe with the first letter starting with capital letters
                time: The time it takes to prepare the recipe in minutes
                directions: A list of the steps taken to cook the recipe. It should be formatted as a Python list where the elements are the steps.
            }
        ]
        If there are no ingredients provided or there are no recipes from the ingredients given, return an empty list.

        RETURN A LIST OF DICTIONARIES CONTAINING RECIPES OR AN EMPTY LIST. DO NOT RETURN ANYTHING ELSE

    '''

    generate_recipes = st.button('Generate recipes!')
    recipes = []
    if 'recipes' not in st.session_state:
        st.session_state.recipes = []

    if generate_recipes:
        st.session_state.recipes = []
        response = gen_ai_call(recipe_query).text
        recipes = eval(response)

    recipe_list = []
    if recipes or st.session_state.recipes:
        if recipes:
            st.session_state.recipes = recipes
        else:
            recipes = st.session_state.recipes
        for recipe in recipes:
            name = Recipe(
                recipe['name'],
                recipe['calorie'],
                recipe['protein'],
                recipe['ingredients'],
                recipe['time'],
                recipe['directions']
            )
            recipe_list.append(name)

    if not recipe_list:
        st.info('No recipe could be generated. Try again')
    else:
        st.subheader('Here you go: ')
        for recipe in recipe_list:
            with st.expander(recipe.name):
                print_recipe(recipe)
                recipe_download = download_recipe(recipe)
                download, save = st.columns(2, gap='large')
                with download:
                    download_button('Download recipe', recipe_download, recipe.name, recipe.name + ' download')
                with save:
                    save_button = st.button('Save recipe', key=recipe.name + ' save')
                    if save_button:
                        save_recipe(recipe.name, recipe.calorie, recipe.protein, list_to_string(recipe.ingredients),
                                    recipe.time, list_to_string(recipe.directions))

        st.write('Enjoy!')