import urllib

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import requests
from requests.exceptions import HTTPError


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
bootstrap = Bootstrap(app)

DETAIL_LIST_URL = "https://tasty.p.rapidapi.com/recipes/detail"
RECIPE_LIST_URL = "https://tasty.p.rapidapi.com/recipes/list"


@app.route('/', methods=["GET", "POST"])
def homepage():
    if request.method == "GET":
        return render_template("index.html")
    else:
        ingredients = request.form["ingredients"]

        recipe_list_querystring = {"from": "0", "size": "5", "q": ingredients}

        headers = {
            'x-rapidapi-host': "tasty.p.rapidapi.com",
            'x-rapidapi-key': "b9e6268896mshbd1cd81a784b355p197503jsn22ea39ac9f87"
        }

        response = requests.request("GET", RECIPE_LIST_URL, headers=headers, params=recipe_list_querystring)
        response.raise_for_status()
        recipe_list = response.json()
        no_of_recipes = len(recipe_list["results"])
        # Create  an empty list to hold lists of ingredients, lists of instructions and recipe names
        recipe_names = []
        full_recipe_ingredients = []
        full_recipe_instructions = []
        recipe_images = []

        for i in range(no_of_recipes):
            # Create empty arrays for ingredients and instructions
            recipe_ingredients = []
            recipe_instructions = []
            # Find recipe name and add to the recipe names list
            recipe_name = recipe_list["results"][i]["name"]
            recipe_names.append(recipe_name)
            # Find the recipe id
            recipe_id = recipe_list["results"][i]["id"]
            print("RECIPE: " + recipe_name)
            print("INGREDIENTS: ")
            # Find the recipe image
            recipe_img = recipe_list["results"][i]["thumbnail_url"]
            print(recipe_img)
            recipe_images.append(recipe_img)
            detail_querystring = {"id": f"{recipe_id}"}
            # Use recipe ID to get the recipe details from the API
            try:
                response = requests.request("GET", DETAIL_LIST_URL, headers=headers, params=detail_querystring)
                response.raise_for_status()
                recipe_detail = response.json()
                # Find no of ingredients in recipe
                no_of_ingredients = len(recipe_detail["sections"][0]["components"])
                # loop through ingredients adding each one to the ingredients list for this recipe
                for y in range(no_of_ingredients):
                    ingredients = recipe_detail["sections"][0]["components"][y]["raw_text"]
                    recipe_ingredients.append(ingredients)
                    print(ingredients)
                print("INSTRUCTIONS: ")
                # Find no. of instructions in recipe
                no_of_instructions = len(recipe_detail["instructions"])
                # loop through no of instruction adding each one to instruction list for this recipe
                for n in range(no_of_instructions):
                    instruction = f"{n+1}. " + recipe_detail["instructions"][n]["display_text"]
                    recipe_instructions.append(instruction)
                    print(instruction)
                # append the lists of ingredients and instructions to the main lists of all the recipes ingredients and
                # instructions.
                full_recipe_ingredients.append(recipe_ingredients)
                full_recipe_instructions.append(recipe_instructions)
            except HTTPError:
                pass

        return render_template("index.html", recipe_names=recipe_names, full_recipe_ingredients=full_recipe_ingredients,
                               no_of_recipes=no_of_recipes, full_recipe_instructions=full_recipe_instructions,
                               recipe_images=recipe_images)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)


