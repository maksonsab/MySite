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

def bad_cookie() -> response: #cleaning cookies 
    response = make_response(redirect(url_for('login')), 302)
    response.set_cookie('username', '', max_age=0)
    session.clear()
    return response

@app.before_request
def is_loggined(cookies=None) -> bool:
    print('before first req')
    session_bool = session.get('loggined')
    if session_bool == True:
        #return 'session_bool = True'
        pass

    user = request.cookies.get('username')
    if user:
        #print ('not user', f'var user contains: {user}') #False
        
        try:
            username, sign = user.split('.')
        except ValueError:
            print('value error')  #False
        correct_cookie = check_user_from_cookie(username, sign)
        if correct_cookie[0]: 
            print('Cookies OK!')
            session['username'] = correct_cookie[1]
            session['loggined'] = True
            session.modified = True
        #return False








@app.route('/', methods=['GET'])
def index():
    print()
    return render_template('index.html',  data = dbase().get_last_posts())


@app.route('/post/<int:id>', methods=['GET'])
def post(id = None):
    return render_template('post.html', data = dbase().get_post(id))

@app.route('/posts/', methods=['GET'])
def posts():
    return render_template('posts.html', data = dbase().get_posts())

@app.route('/create', methods=['GET', 'POST'])
def create():    
    if request.method == 'GET':
        try:
            username, sign = request.cookies.get('username').split('.')
            print(username, sign)
            if auth.check_user_from_cookie(username, sign)[0]:
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
def login():

    if request.method == 'GET':
        user = request.cookies.get('username')
        if user:
            try:
                username, sign = user.split('.')
            except ValueError:
                return bad_cookie()
            correct_cookie = check_user_from_cookie(username, sign)
            if correct_cookie[0]: 
                response = make_response(redirect(url_for('create')), 302) #login OK
                session['username'] = correct_cookie[1] 
                print(session)
                return response
            else:
                return bad_cookie()
        print(session)        
        response = make_response(render_template('login.html'), 200)
        return response
    if request.method == 'POST':
            
        login = request.form['login']
        password = request.form['password']
            
        message = dbase().authorize(login, password)
        if message[0]:
            response = make_response((redirect(url_for('create')), 302))
            response.set_cookie('username', auth.sign_data(login), max_age = 1*24*3600)
            #print(message[1])
            session['username'] = login
            session['loggined'] = True
            session.modified = True
            return response
        else:
            return bad_cookie()
                
@app.route('/logout', methods = ['GET'])
def logout():
    return bad_cookie()


@app.route('/test', methods = ['GET'])
def test():
    print('COOKIES:\n', request.cookies)
    loggined = session.get('loggined')
    if loggined:
        string = session
        return string
    return 'Not loggined'



if __name__ == '__main__':
    app.run()
