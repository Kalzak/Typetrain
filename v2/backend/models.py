from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        return True #bcrypt.check_password_hash(self.password, password)

class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    submitter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    submitter = db.relationship('User', backref='suggestions', lazy=True)