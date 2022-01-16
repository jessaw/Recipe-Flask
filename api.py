from multiprocessing import connection
from flask import Flask, render_template, request,redirect,url_for

app = Flask(__name__)



import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to RECIPES DB successful")
    except Error as e:
        print(f"The error {e} occurred")

    return connection


def execute_query(connection, query, values= ()):
    cursor = connection.cursor()
    print(values)
    try:
        if len(values) > 0:
            cursor.execute(query,values)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error{e} occurred")

create_recipesflask_table = """
CREATE TABLE IF NOT EXISTS recipes (
  id INTEGER PRIMARY KEY,
  image BLOB NOT NULL,
  link INTEGER NOT NULL
);
"""


@app.route('/')
def home():
    return render_template("home.html",recipes=recipes)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/recipe/', methods=['POST', 'GET'])
def create_recipe():
    form =request.form
    #  print(form)
    # title = request.form.get('title')
    # print(request.form.get('title'))
    return redirect(url_for('home'))


recipes = [
        {
            "title": "BBQ Sweet and Sour Chicken Wings",
            "image": "https://image.freepik.com/free-photo/chicken-wings-barbecue-sweetly-sour-sauce-picnic-summer-menu-tasty-food-top-view-flat-lay_2829-6471.jpg",
            "link": "https://cookpad.com/us/recipes/347447-easy-sweet-sour-bbq-chicken"
        },
        {
            "title": "Pasta Bolognese",
            "image": "https://www.jocooks.com/wp-content/uploads/2018/01/spaghetti-bolognese-1-3-500x375.jpg",
            "link": "https://www.onceuponachef.com/recipes/pasta-bolognese.html"
        }
    ]

if __name__ == '__main__':

    conn =create_connection("recipesflask.db")
    execute_query(conn,create_recipesflask_table)
    app.run(debug=True)