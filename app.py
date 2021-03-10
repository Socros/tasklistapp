from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
# from flask import RegistrationForm, LoginForm
import json
import os
import sqlite3
from sqlite3 import Error
import pandas as pd

app = Flask(__name__)

conn = sqlite3.connect("C:\\Users\\Socratis\\Desktop\\tasklist\\tasklist\\todo.db")


#Take the last tasks from jsron file
def getTodos():
    with open('todos.json', encoding="utf8") as json_file:
        return json.load(json_file)

#Giving at task an id
def getTodo(id):
    todos = getTodos()
    return next(filter(lambda x: x['id'] == int(id), todos))

#Add a task to json file
def addTodo(todo):
    todos = getTodos()
    todos.append(todo)
    with open('todos.json', 'w', encoding="utf8") as json_file:
        return json.dump(todos, json_file, ensure_ascii = False)

#When you create a new task, this, convert your task to a js which is our DB.
def toggleTodo(id):
    todos = getTodos()
    todo = next(filter(lambda x: x['id'] == int(id), todos))
    todo['status'] = abs(todo['status'] - 1)
    with open('todos.json', 'w', encoding="utf8") as json_file:
        return json.dump(todos, json_file, ensure_ascii = False)

#When you delete a task, it delete from json file.
def deleteTodo(id):
    todos = getTodos()
    # todos = list(filter(lambda x: x['id'] != int(id), todos))
    todos = list([x for x in todos if x['id'] != int(id)])
    with open('todos.json', 'w', encoding="utf8") as json_file:
        return json.dump(todos, json_file, ensure_ascii = False)

#When you update task, this, convert your task to a js which is our DB.
def updateTodo(todo_toedit):
    todos = getTodos()
    todo = next(filter(lambda x: x['id'] == int(todo_toedit['id']), todos))
    todo['name'] = todo_toedit['name']
    with open('todos.json', 'w', encoding="utf8") as json_file:
        return json.dump(todos, json_file, ensure_ascii = False)


#app
@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

#This is for complete tasks
@app.route('/toggle/<id>')
def toggle(id):
    toggleTodo(id)
    return redirect(url_for('tasks'))

#Delete a task
@app.route('/delete/<id>')
def delete(id):
    deleteTodo(id)
    return redirect(url_for('tasks'))

#Contact page url
@app.route('/contacts', methods=['GET', 'POST'])
def contact():
    return render_template('contacts.html')

#task page
@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        now = datetime.now()
        todo_name = request.form.get('todo_name')
        todoDict = {
            'id': int(datetime.timestamp(now)),
            'name' : todo_name,
            'status': 0,
            'create_at': now.strftime("%d-%m-%Y %H:%M:%S"),
            'deadline': None
        }
        addTodo(todoDict)
    return render_template('tasks.html', todos=getTodos())


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    todo = getTodo(id)
    if request.method == 'POST':
        todo_name = request.form.get('todo_name')
        todo['name'] = todo_name
        updateTodo(todo)
        return redirect(url_for('tasks'))
    return render_template('edit.html', todo=todo)

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

# ################################################################################
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"C:\Users\Socratis\Desktop\tasklist\tasklist\todo.db"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

        # create tasks table
        create_table(conn, sql_create_tasks_table)
        print ("The database connection is ready!")
    else:
        print("Error! cannot create the database connection.")


# ################################################################################



# conn = sqlite3.connect('todo.db')  # You can create a new database by changing the name within the quotes
# c = conn.cursor() # The database will be saved in the location where your 'py' file is saved

# Create table - CLIENTS
# c.execute('''CREATE TABLE CLIENTS
#              ([generated_id] INTEGER PRIMARY KEY,[Client_Name] text, [Country_ID] integer, [Date] date)''')
          
# Create table - COUNTRY
# c.execute('''CREATE TABLE COUNTRY
#              ([generated_id] INTEGER PRIMARY KEY,[Country_ID] integer, [Country_Name] text)''')
        
# Create table - DAILY_STATUS
# c.execute('''CREATE TABLE DAILY_STATUS
#              ([Client_Name] text, [Country_Name] text, [Date] date)''')
                 
# conn.commit()

# df = pd.read_csv (r'C:\Users\Socratis\Desktop\tasklist\tasklist\data.csv')
# print (df)

if __name__ == '__main__':
    app.run(debug=True)
