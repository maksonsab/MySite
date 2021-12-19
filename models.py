from enum import unique

from sqlalchemy.orm import backref
from app import db 
from auth import hash_password
import datetime

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    passwrd = db.Column(db.String(50), nullable = False)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(50))
    avatar = db.Column(db.LargeBinary())
    posts = db.relationship('Posts', backref='author', )

    def __repr__(self) -> str:
        return f'User object id {self.id}'

    def __init__(self, username:str, passwrd:str, f_n:str, l_n:str) -> None:
        self.username = username
        self.passwrd = hash_password(passwrd)
        self.first_name = f_n
        self.last_name = l_n


    def get_user(username:str):
        return Users.query.filter_by(username=username).first()
    
    @staticmethod
    def authorize(login: str, password: str) -> tuple:
        '''Возвращает кортеж с bool-ключем авторизации и сообщением для вывода в консоль (отладка)'''
        print(login, password)
        user = Users.query.filter_by(username = login).one()
        if user:
            print(user)
            if hash_password(password) == user.passwrd:
                return (True, 'All OK!')
            else: 
                return (False, 'Wrong password!')
        else:
            return(False, 'Wrong username!')




class Posts(db.Model):
    __table_args__ = ( db.UniqueConstraint('title', 'uri'),)
    id = db.Column(db.Integer, primary_key = True)
    creation_date = db.Column(db.DateTime, nullable = False)
    title = db.Column(db.String(100), nullable = False)
    post_description = db.Column(db.String(255), nullable = False)
    content = db.Column(db.Text, nullable = False)
    viewes = db.Column(db.Integer, default = 0)
    rating = db.Column(db.Integer, default = 0)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    visible = db.Column(db.Boolean, default = True)
    uri = db.Column(db.String(50), nullable = False)
    

    def __repr__(self) -> str:
        return f'Post object with id: {self.id}, title: {self.title}.'

    def __init__(self, post: dict, author) -> None: #title, post_description, content, uri, author
        self.creation_date = datetime.datetime.now()
        self.title = post.get('title')
        self.post_description = post.get('description')
        self.content = post.get('content')
        self.uri = post.get('uri')
        self.author = author
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    
    def get_post(uri:str):
        '''Возвращает пост с автором поста по id автора'''
        post = Posts.query.filter_by(uri = uri).one()
        if post:
            post.author_name = post.author.first_name + ' ' + post.author.last_name
            #post.creation_date = time.strftime('%d.%m.%Y', time.gmtime(post.creation_date))
            post.viewes += 1
            db.session.commit()
            return post
        return None    




if __name__ == '__main__':
    pass