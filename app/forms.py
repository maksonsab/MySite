from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    login = StringField("Логин: ", validators = [InputRequired(), Length(min=4, max=50)])
    psw = PasswordField("Пароль: ", validators = [InputRequired(), Length(min = 6)])
    submit = SubmitField('Войти')


class PostForm(FlaskForm):
    title = StringField('Название поста: ',  
        render_kw = {'placeholder' : 'Название'}, 
        validators = [InputRequired(), Length(min=5, max=50, message = 'Название от 5 до 50 символов!') ],)
    description = StringField('Описание поста: ', 
        render_kw = {'placeholder': 'Описание'}, 
        validators = [InputRequired(), Length(min=10, max=150, message = 'Описание от 10 до 150 символов!')])
    content = TextAreaField('Статья: ', 
        render_kw = {'placeholder':'Содержание статьи, поддерживается markdown...', 'cols':120, 'rows':20}, 
        validators = [InputRequired()])
    uri = StringField('Cсылка',
            render_kw={'placeholder' : 'Ссылка на статью...'},
            validators=[InputRequired(message='Обязательное поле '), Length(min=7, max=35)])
    post_image = StringField('Основное изображение',
            render_kw={'placeholder' : 'Здесь будет ссылка после загрузки изображения', 'id' : 'image_uri'},
            validators= [InputRequired()])
    submit = SubmitField('Опубликовать')
    