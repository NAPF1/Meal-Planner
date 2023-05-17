# Course: CST205-01 - Multimedia Design and Programming - Avner
# Title: Meal Planner
# Abstract: Nightly meal-planning application for producing a weekly grocery list.
# Team: Nicolas Porras Falconio, Alexander Verdugo, Matthew Peters, Miguel Santiago
# Date: 5/17/23
# Link to Github: https://github.com/NAPF1/Meal-Planner

from flask import Flask, render_template
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
        return data[0]['calories'], data[0]['serving_size_g']
    else:
        return None, None

# Old get nutritions function Do not use
# def get_meals_nutrition(meals):
#     for meal in meals:
#         #meal['calories'] = []  # Initialize 'calories' list
#         #meal['serving_size'] = []  # Initialize 'serving_size' list
#         calories = []
#         serving_size = []
#         for ingredient in meal['ingredients']:
#             calories, serving_size = get_calories(ingredient)
#             meal['calories'].append(calories)
#             meal['serving_size'].append(serving_size)
#     return meals

def get_meals_nutrition(names): # Updated get meal nutrition function
    caloriesAndServingSize = []  # Calories and serving size list     
    for meal in meals: # For each avaliable meal
        for name in names: # And for each selected meal
            if meal['name'] == name: # If the available meal matches a selected meal
                for ingredient in meal['ingredients']: # Cycle through the ingredients
                    caloriesAndSS= get_calories(ingredient) # Calling getCalories function to get calories and serving size
                    caloriesAndServingSize.append(caloriesAndSS) # Appending to list of Calories and Serving size
                    
    return caloriesAndServingSize # Returning the Calories and Serving size list


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

# Home route
@app.route('/')
def home():
    return render_template('index.html', meals=meals)

# Grocery List route (Displays EMPTY grid when routed from navbar!)
@app.route('/list', methods=['GET', 'POST'])
def list():
    selected_meals = [] # New list every time
   
    # Uses list of weekdays (top of file) to refer to the names of the dropdown choices
    for day in days: 
        selected_meals.append(request.form.get(day)) # Fetches and appends all chosen meal names
    cals = get_meals_nutrition(selected_meals)  # Uses function to get calories and serving size from ingredients
    ings = get_ingredients(selected_meals) # Uses function to get ingredients from matching meals
    
    ingredients = {} # Dict needed to append it to meals.py list of dicts
    for ing in ings: # For each ingredient in the list
        if ing in ingredients: # Checks for already existing ingredient
            ingredients[ing] += 1 # Adds number for multiplier for simpler display
        else:
            ingredients[ing] = 1 # It's a new one so add it and make it 1
    
    calories = [] # List needed to append it to meals.py list 
    for cal in cals: # For each calories in the list append to the calories list above
        calories.append(cal)


    # Loads list with the master list of combined ingredients from all selected meals
    return render_template('list.html', ingredients=ingredients, calories=calories)
    
# View/Edit Meals route
@app.route('/meal', methods=['GET', 'POST'])
def meal():
    message = '' # For updating on POST requests only

    if request.method == 'POST': # Avoid null references if 'get' request
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
