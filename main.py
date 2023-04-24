from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from meals import meals_info
app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/list')
def list():
    return render_template('list.html')