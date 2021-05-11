from app import app
from flask_sqlalchemy import SQLAlchemy
from config import config_name, config_password
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

db = SQLAlchemy(app)


@app.before_first_request
def create_all():
    db.create_all()
    user = User(name=config_name,
                password=config_password)
    db.session.add(user)
    db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(20))

    def __init__(self, name, password):
        self.name = name
        self.password = generate_password_hash(password)


class Items(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(100), nullable=True)
    item_num = db.Column(db.Integer, nullable=True)
    size = db.Column(db.String(10), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)

    def __init__(self, category, name, item_num, size, quantity):
        self.category = category
        self.name = name
        self.item_num = item_num
        self.size = size
        self.quantity = quantity

    def __str__(self):
        return self.category


class Customers(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    discount = db.Column(db.Boolean, default=False)

    def __init__(self, email):
        self.email = email
