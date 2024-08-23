from flask import Flask, render_template, url_for, request
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from datetime import datetime
import configparser
import os
import re

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG


app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)

# this context processors allows the below variables to be used in all templates, and you dont need to define it in each.
@app.context_processor
def inject_global_variables():
    config = configparser.ConfigParser()
    config.read('api/config.ini')

    # Access the variables in the "configs" section
    domain = config['configs']['domain']
    email = config['configs']['email']
    your_name = config['configs']['your_name']
    github = config['configs']['github']
    blog_comments = config['configs']['blog_comments']
    hubspot = config['configs']['hubspot']
    linkedin = config['configs']['linkedin']
    twitter = config['configs']['twitter']
    current_year = datetime.now().year

    return {
        'domain': domain,
        'email': email,
        'your_name': your_name,
        'github': github,
        'blog_comments': blog_comments,
        'hubspot': hubspot,
        'linkedin': linkedin,
        'twitter': twitter,
        'current_year': current_year
    }


# Фіктивні дані товарів
products = [
    {"name": "Енциклопедія прикрас", "image": "static\images\img_ToBap\Енциклопедія_прикрас.jpg", "price": "1999"},
    {"name": "Набір металевих прикрас для волосся", "image": "static\images\img_ToBap\Набір_металевих_прикрас_для_волосся.jpg", "price": "2299"},
    {"name": "Цукрова прикраса Серце I love you", "image": "static\images\img_ToBap\Цукрова прикраса Серце I love you.jpg", "price": "2499"}
]

@app.route('/')
def home():
    return render_template('home.html', products=products)

@app.route('/about')
def about():
  return render_template("about.html")


@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    if query:
        found_products = [product for product in products if query in product['name'].lower()]
    else:
        found_products = products  # Показати всі продукти, якщо запит порожній
    return render_template("home.html", products=found_products)