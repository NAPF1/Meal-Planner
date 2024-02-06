from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from meals import meals_info as meals
from sides import sides_info as sides
from PIL import Image
import requests, random

app = Flask(__name__)
bootstrap = Bootstrap5(app)
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def get_all_ingredients():
    allIngredients = set()  # Using a set to automatically remove duplicates
    for meal in meals:
        allIngredients.update(meal['ingredients'])
    for side in sides:
        allIngredients.update(side['ingredients'])
    print(allIngredients)
    return sorted(allIngredients)

def get_ingredients(names):
    ingredients = [] # Master ingredients list for populating div in list.html
    for meal in meals: # For each available meal
        for name in names: # And for each selected meal
            if meal['name'] == name: # If the available meal matches a selected meal
                for ingredient in meal['ingredients']: # Cycle thorugh those ingredients
                    ingredients.append(ingredient) # Add each ingredient to master list
    for side in sides: # For each available meal
        for name in names: # And for each selected meal
            if side['name'] == name: # If the available meal matches a selected meal
                for ingredient in side['ingredients']: # Cycle thorugh those ingredients
                    ingredients.append(ingredient) # Add each ingredient to master list
    return ingredients

# Home route
@app.route('/')
def home():
    return render_template('index.html', meals=meals, sides=sides)

# Grocery List route (Displays EMPTY grid when routed from navbar!)
@app.route('/list', methods=['GET', 'POST'])
def list():
    selected_meals = [] # New list every time
   
    # Uses list of weekdays (top of file) to refer to the names of the dropdown choices
    for day in days: 
        print(request.form.get(day))
        selected_meals.append(request.form.get(day)) # Fetches and appends all chosen meal names
        for i in range(0,3):
            print(request.form.get(f"{day}{i}"))
            selected_meals.append(request.form.get(f"{day}{i}"))
    # cals = get_meals_nutrition(selected_meals)  # Uses function to get calories and serving size from ingredients
    ings = get_ingredients(selected_meals) # Uses function to get ingredients from matching meals
    
    ingredients = {} # Dict needed to append it to meals.py list of dicts
    for ing in ings: # For each ingredient in the list
        if ing in ingredients: # Checks for already existing ingredient
            ingredients[ing] += 1 # Adds number for multiplier for simpler display
        else:
            ingredients[ing] = 1 # It's a new one so add it and make it 1
    ingredients = dict(sorted(ingredients.items()))
    
    # calories = [] # List needed to append it to meals.py list 
    # for cal in cals: # For each calories in the list append to the calories list above
    #     calories.append(cal)


    # Loads list with the master list of combined ingredients from all selected meals
    # return render_template('list.html', ingredients=ingredients, calories=calories)
    return render_template('list.html', ingredients=ingredients)
    
# View/Edit Meals route
@app.route('/meal', methods=['GET', 'POST'])
def meal():
    message = '' # For updating on POST requests only

    if request.method == 'POST': # Avoid null references if 'get' request
        name = request.form.get('name') # User-entered name
        ings = request.form.get('ingredients') # User-entered ingredients (str)
        drop = request.form.get('type') # User-entered type of meal
        ingredients = ings.split(',') # List of user-entered ingredients
        
        message = 'Added succesfully!' # Default to success unless meal already exists
        for meal in meals: # Checks for already already matching meal
            if meal['name'] == name:
                message = 'Error. Meal already exists.' # Error message for printing
        for side in sides:
            if side['name'] == name:
                message = 'Error. Side already exists.' # Error message for printing

        if message.__contains__('succesfully'):
            if drop == "Main": # Only adds if message not altered.
                new_meal = { # Create dict from meal attributes
                    "name" : name,
                    "ingredients" : ingredients,
                    # "img_url" : ""
                }
                meals.append(new_meal) # Append the meal to the list of dicts from meals.py
            elif drop == "Side":
                new_side = { # Create dict from meal attributes
                    "name" : name,
                    "ingredients" : ingredients,
                    # "img_url" : ""
                }
                sides.append(new_side) # Append the meal to the list of dicts from meals.py

    random.shuffle(meals) # Shuffle a new order every time for fresh look
    return render_template('addmeal.html', meals=meals, message=message)

@app.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    all_ingredients = get_all_ingredients()  # Implement a function to get all ingredients
    return render_template('ingredients.html', allIngredients=all_ingredients)