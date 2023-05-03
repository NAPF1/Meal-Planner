from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from meals import meals_info
import requests
from PIL import Image

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
    return render_template('index.html', meals=meals_info)


# @app.route('/list')
# def list():
#     return render_template('list.html')