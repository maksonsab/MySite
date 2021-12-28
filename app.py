from os import environ,path
import random
from string import ascii_lowercase, digits


from flask import Flask, request, render_template, redirect, session, url_for, make_response, abort, json, send_file
from werkzeug.wrappers import response
from flask_sqlalchemy import SQLAlchemy


from forms import LoginForm, PostForm
import models

app = Flask(__name__, template_folder='templates')
app.config.update(
    DEBUG = True,
    SECRET_KEY = environ['SECRET_KEY'],
    ENV = 'development',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db',
    SQLALCHEMY_TRACK_MODIFICATIONS = False,

)

db = SQLAlchemy(app)



def bad_cookie(where='login') -> response: #cleaning cookies 
    response = make_response(redirect(url_for(where)), 302)
    response.set_cookie('username', '', max_age=0)
    session.clear()
    session['loggined'] = False
    return response


def random_name(extension:str) -> str:
    '''Возвращает рандомное имя файла с его расширением'''
    return ''.join(random.sample(ascii_lowercase + digits, 10)) + '.' + extension



@app.before_request
def print_ses():
    print(session)

@app.before_first_request
def is_loggined():
    user = request.cookies.get('username')
    if user:
        try:
            username, sign = user.split('.')
        except ValueError:
            bad_cookie()
        else:
            correct_cookie = models.Users.check_user_from_cookie(username, sign)
            if correct_cookie[0]: 
                session['user'] = models.Users.get_user(correct_cookie[1]).username
                session['loggined'] = True
                session.modified = True
                
    else:
        session['loggined'] = False
        session.modified = True
        



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',  data = models.Posts.get_last_posts(), loggined = session)

@app.route('/post/<uri>', methods=['GET'])
def post(uri = None):
    data = models.Posts.get_post(uri)
    if data:
        return render_template('post.html', data = data, loggined = session)
    return abort(404)

@app.route('/posts/', methods=['GET'])
def posts():
    return render_template('posts.html', data = models.Posts.get_posts(), loggined = session)

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = PostForm()   
    if session.get('loggined'):
        if request.method == 'GET':
            return render_template('create.html', loggined = session, form = form)
        if form.validate_on_submit():
            is_loggined()
            if session.get('loggined'):
                post = form.data
                models.Posts(post, author = models.Users.get_user(session.get('user')))
                return redirect(url_for('index'))
            else:
                return bad_cookie()
    return redirect(url_for('login'))
                

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        if session.get('loggined'):
            return redirect(url_for('create'), 302)
        print(session)        
        response = make_response(render_template('login.html', loggined = session, form = form), 200)
        return response

    if form.validate_on_submit():
        login = form.login.data
        password = form.psw.data
        message = models.Users.authorize(login, password)
        if message:
            response = make_response((redirect(url_for('create')), 302))
            response.set_cookie('username', models.Users.sign_data(login), max_age = 1*24*3600)
            session['user'] = message
            session['loggined'] = True
            return response
        else:
            return bad_cookie()



                
@app.route('/logout', methods = ['GET'])
def logout():
    return bad_cookie(where = 'index')


@app.route('/vote/<int:id>', methods = ['PUT'])
def vote(id):
    post = models.Posts.query.get(id)
    print(post.rating, type(post.rating))
    post.voteup()
    data = json.dumps({'rating' : post.rating})
    print(data, type(data))
    response = make_response(data, 200,)
    response.headers['Content-Type'] = 'aplication/json'
    return response

@app.route('/upload_img', methods = ['POST'])
def upload_img():
    '''Загружает фото на сервер и возвращает JSON с ключами путь и имя файла'''
    if request.files:
        image = request.files['image-input']
        image_extension = image.filename.rsplit('.')[1]
        image.filename = random_name(image_extension)
        image.save(path.join('./static/images/posts', image.filename))
        pim = 'posts/' + image.filename #path to image
        print('\n\n\nFILE OK!')
        response = make_response(json.dumps({'path':pim, 'name' : image.filename}), 200)
        response.headers['Content-Type'] = 'aplication/json'
        return response

    return redirect(url_for('index'))

@app.route('/image/<path:path_to_image>')
def get_image(path_to_image):
    try:
        image_dir = path.join('./static/images/')
        image = image_dir + path_to_image
        return send_file(image, mimetype='image/jpeg')
    except Exception:
        return abort(404)

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
