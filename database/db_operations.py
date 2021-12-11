import math
import sqlite3
import time


from markdown import markdown
from database import auth

class db_operation(object):
    '''Выполняет операции с базой данных'''
    def __init__(self, db:str):
        self.__connection = sqlite3.connect(db)
        self.__connection.row_factory = sqlite3.Row
        self.__cur = self.__connection.cursor()
        print('db connection opened!')
    
    def get_last_posts(self)-> list:
        '''Возвращает три послдених статьи для отображения на главной странице'''
        sql = 'SELECT * FROM posts ORDER BY id DESC LIMIT 3'
        self.__cur.execute(sql)
        data = self.__cur.fetchall()
        self.__connection.close()
        print('db connection closed!')
        return data

    def get_posts(self) -> list:
        '''Возвращает список всех статей отсортированных по id в порядке уменьшения'''
        sql = 'SELECT * FROM posts ORDER BY id DESC'
        data = self.__cur.execute(sql).fetchall()
        print(type(data), data)
        self.__connection.close()
        print('db connection closed!')
        return data

    def get_post(self, id:int) -> dict:
        '''Возвращает словарь с содержимым статьи'''
        sql = f'SELECT * FROM posts WHERE id={id}'
        data = dict(self.__cur.execute(sql).fetchone())
        counter = data.get('viewes') + 1
        update_view = f'UPDATE posts SET viewes = {counter} WHERE id={id}'
        self.__cur.execute(update_view)
        self.__connection.commit()
        data['content'] = markdown(data['content']) #markdown post content! !!markdown to html when add to database???????
        data['creation_date'] = time.strftime('%d.%m.%Y', time.gmtime(data['creation_date']))
        self.__connection.close()
        print('db connection closed!')
        return data
    
    def create_post(self, data:dict): 
        '''Добавляет статью в базу данных'''
        self.__cur.execute('INSERT INTO posts (title, post_description, content, creation_date) VALUES (?,?,?,?)', (data['title'], data['description'], data['content'], int(time.time())))
        self.__connection.commit()
        self.__connection.close()
        print('db connection closed!')

    def authorize(self, login: str, password: str) -> tuple:
        '''Возвращает кортеж с bool-ключем авторизации и сообщением для вывода в консоль (отладка)'''
        command = f'SELECT * FROM users WHERE username="{login}"'
        get_user = self.__cur.execute(command).fetchone()
        self.__connection.close()
        print('db connection closed!')
        if get_user:
            get_user = dict(get_user)
            if auth.hash_password(password) == get_user['passwrd']:
                return (True, 'All OK!')
            else: 
                return (False, 'Wrong password!')
        else:
            return(False, 'Wrong username!')

        







