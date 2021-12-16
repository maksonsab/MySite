from time import sleep, time
import sqlite3
import auth

connection = sqlite3.connect('../database.db')

try:
    with open('schema.sql') as f:
        connection.executescript(f.read())
except FileNotFoundError:
    print('File schema.sql not found\nExiting... ')
    sleep(5)
    exit()
else:
    print('Creating database!')

cur = connection.cursor()

username = input('Login: ')
password = auth.hash_password(input('Password: '))
f_n = input('First name: ')
l_n = input('Last name: ')
cur.execute('INSERT INTO users (username, passwrd, first_name, last_name) VALUES (?,?,?,?)', (username, password , f_n, l_n))

cur.execute("INSERT INTO posts (title, post_description, content, creation_date, uri) VALUES (?,?,?,?,?)", ('Hello, World!', 'Добро пожаловать на мой личный сайт! Давайте знакомиться!', 'Всем привет! Меня зовут Максим Сабирзанов, мне 26 лет и я занимаюсь изучением backend разработки на Python!', int(time()), 'hello_world' ))
cur.execute('INSERT INTO posts (title, post_description, content, creation_date, uri) VALUES (?,?,?,?,?)', ('Вторая статья', 'Тут я не думал над описанием', 'Над текстом тоже как-то не думал, но это не важно же, потому что тестовое всё!', int(time()), 'second' )) 
cur.execute('INSERT INTO posts (title, post_description, content, creation_date, uri) VALUES (?,?,?,?,?)', ('Третья статья', 'Просто пишу буквы чтоб было описание!', 'Какой-то текст чтоб заполнить хоть что-то, но в целом есть над чем ещё думать, много даже над чем... Например, как выводить картиник и т.д.', int(time()), 'test' ))


connection.commit()
connection.close()