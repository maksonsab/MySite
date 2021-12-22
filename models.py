import hashlib, hmac, os, base64, datetime

import sqlalchemy


from app import db 



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
        self.passwrd = self.hash_password(passwrd)
        self.first_name = f_n
        self.last_name = l_n

    @staticmethod
    def get_user(username:str):
        return Users.query.filter_by(username=username).first()
    
    @staticmethod
    def authorize(login: str, password: str) -> tuple:
        '''Возвращает кортеж с bool-ключем авторизации и сообщением для вывода в консоль (отладка)'''
        try:
            user = Users.query.filter_by(username = login).one()
            if Users.hash_password(password) == user.passwrd:
                return user.username
        except Exception:
            print(f'Bad authorize request:\nLogin: {login}\nPassword: {password}')
            pass
        return False

    @staticmethod
    def create_sign(username: str) -> str:
        '''Возвращает подписанную строку для Coockies'''
        return hmac.new(
            os.environ['SECRET_KEY'].encode(),
            msg=username.encode(),
            digestmod=hashlib.sha256).hexdigest().lower()
    
    @staticmethod
    def sign_data(username: str) -> str:
        '''Возвращает строку с логином и подписью'''
        b64_login = base64.b64encode(username.encode()).decode()
        sign_data = '.'.join([b64_login, Users.create_sign(username)])
        return sign_data
    @staticmethod
    def hash_password(password: str) -> str:
        '''Возвращает хэш пароля для сверкой с БД'''
        password_with_salt = password + os.environ['PASSWORD_SALT']
        secure_password = hashlib.sha256(password_with_salt.encode()).hexdigest()
        return secure_password

    def check_user_from_cookie(login: str, sign: str) -> bool:
        '''Возвращает массив с результатом сравнения подписи из куки и подписи сгенерированной для логина из куки'''
        login_from_cookie = base64.b64decode(login.encode()).decode()
        sign_generated = Users.create_sign(login_from_cookie)
        return sign == sign_generated, login_from_cookie




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


    @staticmethod
    def get_last_posts() -> list:
        '''Возвращает три послдених статьи для отображения на главной странице'''
        data = Posts.query.filter(Posts.visible).order_by(Posts.id.desc()).limit(3).all()
        return data


    @staticmethod
    def get_posts() -> list:
        '''Возвращает три послдених статьи для отображения на главной странице'''
        data = Posts.query.filter(Posts.visible).order_by(Posts.id.desc()).all()
        return data

    def change_visible(self):
        if self.visible:
            self.visible = False
        else: self.visible = True
        db.session.commit()
        

if __name__ == '__main__':
    pass