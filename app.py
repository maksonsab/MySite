from logging import DEBUG
from flask import Flask, request, render_template, redirect
from markdown import markdown
import sqlite3

app = Flask(__name__, template_folder='templates')

app.config.update(

    DEBUG = True,
    SECRET_KEY = 'somekey123' #сделать чтоб переменная окружения
)


def get_db_connection(): 
    '''Возвращает подключение к БД sqlite3'''
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_art_from_db(conn, *parameters: iter) ->list:
    """Принимает подключение к БД (conn) и список параметров запроса в БД"""
    param = ', '.join(parameters)
    command = f'SELECT {param} FROM articles ORDER BY id DESC;'
    db_articles = conn.execute(command).fetchall()
    articles = []
    for art in db_articles:
        art = dict(art)
        if 'content' in art.keys():
            art['content'] = markdown(art['content'])
        articles.append(art)
    conn.close()

    return articles


@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    data = get_art_from_db(conn, 'id', 'title', 'art_description')
    return render_template('index.html', data = data[:3])


@app.route('/articles/<id>', methods=['GET'])
def article(id = None):
    conn = get_db_connection()
    data = conn.execute(f'SELECT * FROM articles WHERE id={id}').fetchall() #return list, inside <class 'sqlite3.Row'> with article data (len = 1)
    data = dict(data[0]) #<class 'sqlite3.Row'> to dict
    data['content'] = markdown(data['content'])
    return render_template('article.html', data = data)

@app.route('/articles/', methods=['GET'])
def articles():
    conn = get_db_connection()
    data = get_art_from_db(conn, 'id', 'title', 'art_description')

    return render_template('articles.html', data = data)
 
@app.route('/create', methods=['GET', 'POST'])
def create(status = False):
    if status:
        conn = get_db_connection()
        if request.method == 'GET':
            return render_template('create.html')
        if request.method == 'POST':
            article = request.form
            conn.execute('INSERT INTO articles (title, art_description, content) VALUES (?,?,?)', (article['title'], article['art_description'], article['content']))
            conn.commit()
            conn.close()
            return redirect('/')
    return redirect('/')



if __name__ == '__main__':
    app.run(host = '0.0.0.0', )