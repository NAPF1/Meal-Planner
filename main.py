# Course: CST205-01 - Multimedia Design and Programming - Avner
# Title: Meal Planner
# Abstract: Nightly meal-planning application for producing a weekly grocery list.
# Team: Nicolas Porras Falconio, Alexander Verdugo, Matthew Peters, Miguel Santiago
# Date: 5/17/23
# Link to Github: https://github.com/NAPF1/Meal-Planner

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from meals import meals_info
import requests
from PIL import Image

app = Flask(__name__)
bootstrap = Bootstrap5(app)

# def imageAPI(input):
#     r = requests.post(
#     "https://api.deepai.org/api/text2img",
#     data={
#         'text': input,
#     },
#     headers={'api-key': '33b734c1-0dc3-47a1-a8e8-0f13ea123127'}
#     )
#     print(r.json())

# imageAPI("pug")
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

image_url = get_pixabay_image('steak and rice')
print(image_url)

@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/list')
# def list():
#     return render_template('list.html')
