from app import db 


class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    passwrd = db.Column(db.String(50), nullable = False)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(50))
    avatar = db.Column(db.LargeBinary())

    def __repr__(self) -> str:
        return f'User object id {self.id}'

    def __init__(self, username:str, passwrd:str, f_n:str, l_n:str) -> None:
        self.username = username
        self.passwrd = passwrd
        self.first_name = f_n
        self.last_name = l_n


    def get_user(username:str):
        return Users.query.filter_by(username=username).first()

        
if __name__ == '__main__':
    print(app.config)