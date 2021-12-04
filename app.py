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
)

def dbase(): #return database connection
    return db_operation('database.db')

def bad_cookie(where='login') -> response: #cleaning cookies 
    response = make_response(redirect(url_for(where)), 302)
    response.set_cookie('username', '', max_age=0)
    session.clear()
    session['loggined'] = False
    return response

@app.before_first_request
def is_loggined():
    print('before req')
    user = request.cookies.get('username')
    if user:
        try:
            username, sign = user.split('.')
        except ValueError:
            print('DEBUG: bad cookies!')  #False
            bad_cookie()
        else:
            correct_cookie = check_user_from_cookie(username, sign)
            if correct_cookie[0]: 
                print('DEBUG: cookies OK!')
                session['username'] = correct_cookie[1]
                session['loggined'] = True
                session.modified = True
    else:
        print('DEBUG: no cookies!')
        session['loggined'] = False
        



@app.route('/', methods=['GET'])
def index():
    print(session)
    return render_template('index.html',  data = dbase().get_last_posts(), loggined = session)


@app.route('/post/<int:id>', methods=['GET'])
def post(id = None):
    return render_template('post.html', data = dbase().get_post(id), loggined = session)

@app.route('/posts/', methods=['GET'])
def posts():
    return render_template('posts.html', data = dbase().get_posts(), loggined = session)

@app.route('/create', methods=['GET', 'POST'])
def create():    
    #print('cookies',request.cookies)
    if session.get('loggined'):
        if request.method == 'GET':
            return render_template('create.html', loggined = session)
        if request.method == 'POST':
            is_loggined()
            if session.get('loggined'):
                post = request.form
                print(post)
                dbase().create_post(post)
                return redirect(url_for('index'))
            else:
                return bad_cookie()
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('loggined'):
            print('redirect to create')
            return redirect(url_for('create'), 302)
        print(session)        
        response = make_response(render_template('login.html', loggined = session), 200)
        return response
    if request.method == 'POST': 
        login = request.form['login']
        password = request.form['password']
        message = dbase().authorize(login, password)
        if message[0]:
            response = make_response((redirect(url_for('create')), 302))
            response.set_cookie('username', auth.sign_data(login), max_age = 1*24*3600)
            session['username'] = login
            session['loggined'] = True
            return response
        else:
            print(message[1]) #debug
            return bad_cookie()

                
@app.route('/logout', methods = ['GET'])
def logout():
    return bad_cookie(where = 'index')


@app.route('/test', methods = ['GET'])
def test():
    is_loggined()
    print('COOKIES:\n', request.cookies)
    if session.get('loggined'):
        string = session
        return string
    return 'Not loggined'



if __name__ == '__main__':
    app.run()
