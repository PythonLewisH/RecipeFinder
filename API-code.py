import requests

ingredients = input("Enter your ingredients: ")
DETAIL_LIST_URL = "https://tasty.p.rapidapi.com/recipes/detail"
RECIPE_LIST_URL = "https://tasty.p.rapidapi.com/recipes/list"
RECIPE_LIST_QUERYSTRING = {"from": "0", "size": "20", "q": ingredients}

headers = {
    'x-rapidapi-host': "tasty.p.rapidapi.com",
    'x-rapidapi-key': "b9e6268896mshbd1cd81a784b355p197503jsn22ea39ac9f87"
    }

response = requests.request("GET", RECIPE_LIST_URL, headers=headers, params=RECIPE_LIST_QUERYSTRING)
response.raise_for_status()
recipe_list = response.json()
no_of_recipes = len(recipe_list["results"])

for i in range(no_of_recipes - 1):
    recipe_name = recipe_list["results"][i]["name"]
    recipe_id = recipe_list["results"][i]["id"]
    print("RECIPE: " + recipe_name)
    print("INGREDIENTS: ")
    detail_querystring = {"id": f"{recipe_id}"}
    response = requests.request("GET", DETAIL_LIST_URL, headers=headers, params=detail_querystring)
    response.raise_for_status()
    recipe_detail = response.json()
    no_of_ingredients = len(recipe_detail["sections"][0]["components"])
    for y in range(no_of_ingredients -1):
        ingredients = recipe_detail["sections"][0]["components"][y]["raw_text"]
        print(ingredients)
    print("INSTRUCTIONS: ")
    no_of_instructions = len(recipe_detail["instructions"])
    for n in range(no_of_instructions -1):
        instruction = recipe_detail["instructions"][n]["display_text"]
        print(f"{n + 1}:" + instruction)



