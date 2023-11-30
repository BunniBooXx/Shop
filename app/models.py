from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



db = SQLAlchemy()




# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address = db.Column(db.String(255))

    def __init__(self, username, password, email, first_name, last_name, address):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

    def compare_password(self, password):
        result =  check_password_hash(self.password, password)
        return result

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == "password":
                setattr(self, key, generate_password_hash(value))
            else:
                setattr(self, key, value)
        db.session.commit()


    def to_response(self):
        return {
            "id": self.id, 
            "username":self.username, 
            "password":self.password, 
            "first_name": self.first_name, 
            "last_name": self.last_name, 
            "address":self.address
        }
    

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, product_name, description, price, stock_quantity):
        self.product_name = product_name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_response(self):
        return {
            "id": self.id,
            "product_name": self.product_name,
            "description": self.description,
            "price": self.price,
            "stock_quantity": self.stock_quantity
        }


# Cart Model
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='cart', lazy=True)


    def __init__(self, user_id): 
        self.user_id = user_id


    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_response(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            
        }
    

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship('Product', backref='cart_item', lazy=True)
    
    def __init__(self, cart_id, user_id, product_id, product_price, quantity): 
        self.cart_id = cart_id
        self.user_id = user_id
        self.product_id = product_id
        self.product_price = product_price
        self.quantity = quantity
    
    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_response(self):
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "product_price": self.product_price,
            "quantity": self.quantity
        }



# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='orders', lazy=True)
    order_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    

    def __init__(self, user_id, order_date): 
        self.user_id = user_id
        self.order_date = order_date

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

def to_response(self):
    return {
        "id": self.id,
        "user_id": self.user_id,
        "order_date": self.order_date,
       
    }


# OrderItem Model
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, order_id, product_id, quantity, price): 
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price


    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_response(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price": self.price
    }



