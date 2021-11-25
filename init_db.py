import sqlite3
from auth import hash_password

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, post_description, content) VALUES (?,?,?)", ('Hello, World!', 'Добро пожаловать на мой личный сайт! Давайте знакомиться!', 'Всем привет! Меня зовут Максим Сабирзанов, мне 26 лет и я занимаюсь изучением backend разработки на Python!'))
cur.execute('INSERT INTO posts (title, post_description, content) VALUES (?,?,?)', ('Вторая статья', 'Тут я не думал над описанием', 'Над текстом тоже как-то не думал, но это не важно же, потому что тестовое всё!')) 
cur.execute('INSERT INTO posts (title, post_description, content) VALUES (?,?,?)', ('Третья статья', 'Просто пишу буквы чтоб было описание!', 'Какой-то текст чтоб заполнить хоть что-то, но в целом есть над чем ещё думать, много даже над чем... Например, как выводить картиник и т.д.'))
username = input('Login: ')
password = hash_password(input('Password: '))
f_n = input('First name: ')
l_n = input('Last name: ')
cur.execute('INSERT INTO users (username, passwrd, first_name, last_name) VALUES (?,?,?,?)', (username, password , f_n, l_n))

connection.commit()
connection.close()
