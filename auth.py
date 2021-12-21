import hashlib, hmac, os, base64

def create_sign(username: str) -> str:
    '''Возвращает подписанную строку для Coockies'''
    return hmac.new(
        os.environ['SECRET_KEY'].encode(),
        msg=username.encode(),
        digestmod=hashlib.sha256).hexdigest().lower()
    

def sign_data(username: str) -> str:
    '''Возвращает строку с логином и подписью'''
    b64_login = base64.b64encode(username.encode()).decode()
    sign_data = '.'.join([b64_login, create_sign(username)])
    return sign_data

def hash_password(password: str) -> str:
    '''Возвращает хэш пароля для сверкой с БД'''
    password_with_salt = password + os.environ['PASSWORD_SALT']
    secure_password = hashlib.sha256(password_with_salt.encode()).hexdigest()
    return secure_password

def check_user_from_cookie(login: str, sign: str) -> bool:
    '''Возвращает массив с результатом сравнения подписи из куки и подписи сгенерированной для логина из куки'''
    login_from_cookie = base64.b64decode(login.encode()).decode()
    sign_generated = create_sign(login_from_cookie)
    return sign == sign_generated, login_from_cookie