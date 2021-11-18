import math
import sqlite3


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
        '''Возвращает список всех статей отсортированных в по id в порядке уменьшения'''
        sql = 'SELECT * FROM posts ORDER BY id DESC'
        data = self.__cur.execute(sql).fetchall()
        print(type(data), data)
        self.__connection.close()
        print('db connection closed!')
        return data

    def get_post(self, id:int) -> dict:
        '''Возвращает словарь с содержимым статьи'''
        sql = f'SELECT * FROM posts WHERE id={id}'
        data = self.__cur.execute(sql).fetchall()
        self.__connection.close()
        print('db connection closed!')
        return dict(data[0])
    
    def create_post(self, data:dict): 
        print(data)
        self.__cur.execute('INSERT INTO posts (title, post_description, content) VALUES (?,?,?)', (data['title'], data['post_description'], data['content']))
        self.__connection.commit()
        self.__connection.close()
        print('db connection closed!')






