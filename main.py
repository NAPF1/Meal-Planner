from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from meals import meals_info as meals
from PIL import Image
import requests, random

app = Flask(__name__)
bootstrap = Bootstrap5(app)
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def get_pixabay_image(query):
    print(type(query))
    url = 'https://pixabay.com/api/28306119-deb558f16f7c1989434e2b594'
    url2 = "https://pixabay.com/api/?key=28306119-deb558f16f7c1989434e2b594&q="
   
    response = requests.get(url2+query)
    if response.status_code == 200:
        data = response.json()
        if data['totalHits'] > 0:
            return data['hits'][0]['webformatURL']
    print(response.status_code)
    # else:
    #     return None

def get_calories(ingredient):
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(ingredient)
    response = requests.get(api_url, headers={'X-Api-Key': 'k8A8yajuNt3XDt+amiDpOg==TcDK914bT5PP0tuz'})
    if response.status_code == 200:
        data = response.json()
        print(data[0]['calories'])
        print(data[0]['serving_size_g'])
    print(response.status_code)


calories = get_calories('marinara sauce')
print(calories)

# image_url = get_pixabay_image('steak and rice')
# print(image_url)

def get_ingredients(names):
    ingredients = [] # Master ingredients list for populating div in list.html
    for meal in meals: # For each available meal
        for name in names: # And for each selected meal
            if meal['name'] == name: # If the available meal matches a selected meal
                for ingredient in meal['ingredients']: # Cycle thorugh those ingredients
                    ingredients.append(ingredient) # Add each ingredient to master list
    return ingredients

@app.route('/')
def home():
    return render_template('index.html', meals=meals)

@app.route('/list', methods=['GET', 'POST'])
def list():
    selected_meals = []
    for day in days:
        selected_meals.append(request.form.get(day))
    ings = get_ingredients(selected_meals)

    ingredients = {}
    for ing in ings:
        if ing in ingredients:
            ingredients[ing] += 1
        else:
            ingredients[ing] = 1

    return render_template('list.html', ingredients=ingredients)
    
@app.route('/meal', methods=['GET', 'POST'])
def meal():
    message = '' # For updating on POST requests only

    if request.method == 'POST': # Avoid null references if get response
        mealName = request.form.get('mealName') # User-entered name
        mealIngs = request.form.get('mealIngredients') # User-entered ingredients (str)
        mealIngredients = mealIngs.split(',') # List of user-entered ingredients
        
        message = 'Meal added succesfully!' # Default to success unless meal already exists
        for meal in meals: # Checks for already already matching meal
            if meal['name'] == mealName:
                message = 'Error. Meal already exists in the plan.' # Error message for printing
            
        if message.__contains__('succesfully'): # Only adds if message not altered.
            new_meal = { # Create dict from meal attributes
                "name" : mealName,
                "ingredients" : mealIngredients,
                "img_url" : ""
            }
            meals.append(new_meal) # Append the meal to the list of dicts from meals.py

    random.shuffle(meals) # Shuffle a new order every time for fresh look
    return render_template('addmeal.html', meals=meals, message=message)
    
    