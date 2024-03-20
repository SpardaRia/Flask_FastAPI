from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def creation_pass(self, password):
        self.password = generate_password_hash(password)

    def check_pass(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'{self.firstname} {self.lastname} {self.email}'