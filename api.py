from flask import Flask, render_template

app = Flask(__name__)

import sqlite3
from sqlite3 import Error

def create_connection(recipes.db):
    connection = None
    try:
        connection = sqlite3.connect(recipes.db)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection




@app.route('/')
def home():
    return render_template("home.html",recipes=recipes)

@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)

recipes = [
        {
            "title": "BBQ Sweet and Sour Chicken Wings",
            "image": "https://image.freepik.com/free-photo/chicken-wings-barbecue-sweetly-sour-sauce-picnic-summer-menu-tasty-food-top-view-flat-lay_2829-6471.jpg",
            "link": "https://cookpad.com/us/recipes/347447-easy-sweet-sour-bbq-chicken"
        },
        {
            "title": "Pasta Bolognese",
            "image": "https://www.jocooks.com/wp-content/uploads/2018/01/spaghetti-bolognese-1-3-500x375.jpg"
            "link": "https://www.onceuponachef.com/recipes/pasta-bolognese.html"
        }
    ]