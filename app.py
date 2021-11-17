from os import environ

from logging import DEBUG
from flask import Flask, request, render_template, redirect, session, url_for
from markdown import markdown
import sqlite3

from db_operations import db_operation

app = Flask(__name__, template_folder='templates')

app.config.update(

    DEBUG = True,
    SECRET_KEY = environ['SECRET_KEY'],
    ENV = 'development',
    creating = False
)


def get_db_connection(): 
    '''Возвращает подключение к БД sqlite3'''
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET'])
def index():

    conn = get_db_connection()
    dbase = db_operation(conn)
    data = dbase.get_last_posts()
    
    return render_template('index.html', data = data)


@app.route('/post/<int:id>', methods=['GET'])
def post(id = None):
    conn = get_db_connection()
    dbase = db_operation(conn)
    data = dbase.get_post(id)
    data['content'] = markdown(data['content'])

    return render_template('post.html', data = data)

@app.route('/posts/', methods=['GET'])
def posts():
    conn = get_db_connection()
    dbase = db_operation(conn)
    data = dbase.get_posts()

    return render_template('posts.html', data = data)

@app.route('/create', methods=['GET', 'POST'])
def create(status = app.config.get('creating')):
    if status:     
        if request.method == 'GET':
            return render_template('create.html')
        if request.method == 'POST':
            conn = get_db_connection()
            post = request.form
            dbase = db_operation(conn)
            print(post)
            dbase.create_post(post)
            return redirect(url_for('index'))
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login(status = app.config.get('creating')):
    if status:
        return render_template('login.html')
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()