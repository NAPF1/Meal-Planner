from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from meals import meals_info as meals
from PIL import Image
import requests

app = Flask(__name__)
bootstrap = Bootstrap5(app)

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



@app.route('/')
def home():
    return render_template('index.html', meals=meals)


@app.route('/list', methods=['POST'])
def list():
    names = [] # For transferring selected meals to the list route
    names.append(request.form['m1'], request.form['m2'], request.form['m3'], 
                    request.form['m4'], request.form['m5'], request.form['m6'], 
                    request.form['m7']) # Fetches all selected meals and creates list
    
    ingredients = [] # Master ingredients list for populating div in list.html
    for meal in meals: # For each available meal
        for name in names: # And for each selected meal
            if meal['name'] == name: # If the available meal matches a selected meal
                for ingredient in meal['ingredients']: # Cycle thorugh those ingredients
                    ingredients.append(ingredient) # Add each ingredient to master list

    print(ingredients)
    # ingredients = ingredients.sort()
    return render_template('list.html', ingredients=ingredients)
    # return ingredients

@app.route('/meal')
def meal():
    return render_template('addmeal.html')