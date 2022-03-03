from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import requests

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
        recipe_names = []
        full_recipe_ingredients = []
        full_recipe_instructions = []

        for i in range(no_of_recipes):
            recipe_ingredients = []
            recipe_instructions = []
            recipe_name = recipe_list["results"][i]["name"]
            recipe_names.append(recipe_name)
            recipe_id = recipe_list["results"][i]["id"]
            print("RECIPE: " + recipe_name)
            print("INGREDIENTS: ")
            detail_querystring = {"id": f"{recipe_id}"}
            response = requests.request("GET", DETAIL_LIST_URL, headers=headers, params=detail_querystring)
            response.raise_for_status()
            recipe_detail = response.json()
            no_of_ingredients = len(recipe_detail["sections"][0]["components"])
            for y in range(no_of_ingredients):
                ingredients = recipe_detail["sections"][0]["components"][y]["raw_text"]
                recipe_ingredients.append(ingredients)
                print(ingredients)
            print("INSTRUCTIONS: ")
            no_of_instructions = len(recipe_detail["instructions"])
            for n in range(no_of_instructions):
                instruction = recipe_detail["instructions"][n]["display_text"]
                recipe_instructions.append(instruction)
                print(f"{n + 1}:" + instruction)
            full_recipe_ingredients.append(recipe_ingredients)
            full_recipe_instructions.append(recipe_instructions)

        return render_template("index.html", recipe_names=recipe_names, full_recipe_ingredients=full_recipe_ingredients,
                               no_of_recipes=no_of_recipes, full_recipe_instructions=full_recipe_instructions)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)


