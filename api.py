from multiprocessing import connection
from flask import Flask, render_template, request,redirect,url_for
import sqlite3
from sqlite3 import Error
from wtforms import Form, StringField, validators
app = Flask(__name__)



def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path,check_same_thread=False)
        print("Connection to RECIPES DB successful")
    except Error as e:
        print(f"The error {e} occurred")

    return connection


def execute_query(connection, query, values= ()):
    # cursor = connection.cursor()
    # print(values)
    try:
        if len(values) > 0:
            connection.execute(query,(values,))
        else:
            connection.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error{e} occurred")

create_recipesjess_table = """
CREATE TABLE IF NOT EXISTS recipes (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  image BLOB NOT NULL,
  link INTEGER NOT NULL
);
"""
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

class CreateRecipeForm(Form):
    title = StringField('Recipe Title', [validators.Length(min=4, max=50)])
    image = StringField('Image Address', [validators.Length(min=10)])
    link = StringField('Link Address', [validators.Length(min=10)])


@app.route('/recipe/', methods=['POST', 'GET'])
def create_recipe():
    form = CreateRecipeForm() #instantiate the form to send when the request.method != POST
    if request.method == 'POST':
        form = CreateRecipeForm(request.form)
        if form.validate():
            title = form.title.data #access the form data
            image = form.image.data
            link = form.link.data
            insert_recipe = '''INSERT INTO recipes (title, image, link) VALUES (?,?,?)'''
            data = (title, image, link)
            execute_query(conn, insert_recipe, data)
            return redirect(url_for('home'))
    return render_template('create-recipe.html', form=form)



@app.route('/')
def home():
    fetch_query =''' 
        SELECT  * FROM recipes
        '''

    allrecipes=execute_read_query(conn,fetch_query)
    # print(allrecipes)
    return render_template("home.html",recipes=allrecipes)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/recipe/delete/<id>/', methods=['POST'])
def delete_recipe(id):
    execute_query(conn, '''DELETE FROM recipes WHERE id=?''', (id))
    return redirect(url_for("home"))

@app.route('/recipe/<id>', methods=['GET', 'POST'])
def show_recipe(id):
    form = CreateRecipeForm()
    if request.method == 'POST':
        form = CreateRecipeForm(request.form)
        if form.validate():
            title = form.title.data
            image = form.image.data
            link = form.link.data
            update_query = f'''UPDATE recipes set title=?, image=?, link=? WHERE id={id}'''
            execute_query(conn, update_query, (title, image, link))
            return redirect(url_for('home'))
    select_query = f'''SELECT * FROM recipes WHERE id={id}'''
    recipe = execute_read_query(conn, select_query)
    form = CreateRecipeForm(link=recipe[0][3], title=recipe[0][1], image=recipe[0][2])
    return render_template('edit_recipe.html', form=form, id=id)

   


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

    conn =create_connection("recipesjess.db")
    execute_query(conn,create_recipesjess_table)
    app.run(debug=True)