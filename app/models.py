from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Boxy(UserMixin, db.Model):
    __tablename__ = 'boxies'
    id = db.Column(db.Integer, primary_key=True)
    clave_boxy = db.Column(db.String(64), unique=True)
    sala = db.Column(db.String(16))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    boxies = db.relationship('Boxy', backref='owner', lazy='dynamic')
    
    
    @property
    def password(self):
        raise AttributeError('La contraseña no es un atributo válido')
    

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    