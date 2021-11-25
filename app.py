from os import environ

from logging import DEBUG
from flask import Flask, request, render_template, redirect, session, url_for, make_response


from werkzeug.wrappers import response
from auth import check_user_from_cookie

from db_operations import db_operation
import auth

app = Flask(__name__, template_folder='templates')

app.config.update(

    DEBUG = True,
    SECRET_KEY = environ['SECRET_KEY'],
    ENV = 'development',
    creating = True
)

'dbase = '
def dbase():
    return db_operation('database.db')

def bad_cookie() -> response: #cleaning cookies 
    response = make_response(redirect(url_for('login')), 302)
    response.set_cookie('username', '')
    return response

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',  data = dbase().get_last_posts())


@app.route('/post/<int:id>', methods=['GET'])
def post(id = None):
    return render_template('post.html', data = dbase().get_post(id))

@app.route('/posts/', methods=['GET'])
def posts():
    return render_template('posts.html', data = dbase().get_posts())

@app.route('/create', methods=['GET', 'POST'])
def create(status = app.config.get('creating')):    
    if request.method == 'GET':
        try:
            username, sign = request.cookies.get('username').split('.')
            print(username, sign)
            if auth.check_user_from_cookie(username, sign):
                return render_template('create.html')
            else:
                print('badcookie'.title())
                return bad_cookie()
        except:
            print('badcookie')
            return bad_cookie()
    
    if request.method == 'POST':
        post = request.form
        print(post)

        dbase().create_post(post)
        return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login(status = app.config.get('creating')):
    if status:
        if request.method == 'GET':
            user = request.cookies.get('username')
            if user:
                try:
                    username, sign = user.split('.')
                except ValueError:
                    return bad_cookie()
                correct_cookie = check_user_from_cookie(username, sign)
                if correct_cookie: 
                    response = make_response(redirect(url_for('create')), 302)
                    return response
                else:
                    return bad_cookie()
                
            response = make_response(render_template('login.html'), 200)
            return response
        else:
            pass
        if request.method == 'POST':
            
            login = request.form['login']
            password = request.form['password']
            
            message = dbase().authorize(login, password)
            if message[0]:
                response = make_response((redirect(url_for('create')), 302))
                response.set_cookie('username', auth.sign_data(login))
                print(message[1])
                return response
            else:
                return bad_cookie()
                



if __name__ == '__main__':
    app.run()
