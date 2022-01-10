from os import path
import traceback
import random
from string import ascii_lowercase, digits

from flask import request, render_template, redirect, session, url_for, make_response, abort, json, send_file
from app import app
from werkzeug.wrappers import response

from app.forms import LoginForm, PostForm
from app.models import Users, Posts


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
            correct_cookie = Users.check_user_from_cookie(username, sign)
            if correct_cookie[0]: 
                session['user'] = Users.get_user(correct_cookie[1]).username
                session['loggined'] = True
                session.modified = True
                
    else:
        session['loggined'] = False
        session.modified = True




@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',  data = Posts.get_last_posts(), loggined = session)

@app.route('/post/<uri>', methods=['GET'])
def post(uri = None):
    data = Posts.get_post(uri)
    if data:
        return render_template('post.html', data = data, loggined = session)
    return abort(404)

@app.route('/posts/', methods=['GET'])
def posts():
    return render_template('posts.html', data = Posts.get_posts(), loggined = session)


@app.route('/user/<user>', methods = ['GET'])
def about_user(user):
    try:
        user = Users.query.filter_by(username = user).one()
        posts = Posts.query.with_entities(Posts.id).filter_by(author_id = user.id)
        response = make_response(render_template('user.html', user = user, loggined = session, posts = posts.count()), 200)
        return response
    except Exception:
        traceback.print_exc()
        return abort(404)

        
    

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
                Posts(post, author = Users.get_user(session.get('user')))
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
        print(request.form)
        login = form.login.data
        password = form.psw.data
        print(login, password)
        message = Users.authorize(login, password)
        if message:
            response = make_response((redirect(url_for('create')), 302))
            response.set_cookie('username', Users.sign_data(login), max_age = 1*24*3600)
            session['user'] = message
            session['loggined'] = True
            return response
        else:
            return bad_cookie()
    if request.method == 'POST':
        return redirect(url_for('index'))



                
@app.route('/logout', methods = ['GET'])
def logout():
    return bad_cookie(where = 'index')


@app.route('/vote/<int:id>', methods = ['PUT'])
def vote(id):
    post = Posts.query.get(id)
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
    if session.get('loggined') and request.files:
        image = request.files['image-input']
        image_extension = image.filename.rsplit('.')[1]
        image.filename = random_name(image_extension)
        image.save(path.join('./app/static/images/posts', image.filename))
        pim = '/image/posts/' + image.filename #path to image
        print('\n\n\nFILE OK!')
        response = make_response(json.dumps({'path':pim, 'name' : image.filename}), 200)
        response.headers['Content-Type'] = 'aplication/json'
        return response

    return abort(401)

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