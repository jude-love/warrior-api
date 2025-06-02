from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_method.id'), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship('User', backref=db.backref('purchases', lazy=True))
    product = db.relationship('Product', backref=db.backref('purchases', lazy=True))
    payment_method = db.relationship('PaymentMethod', backref=db.backref('purchases', lazy=True))

    def __repr__(self):
        return f'<Purchase User:{self.user_id} Product:{self.product_id} PaymentMethod:{self.payment_method_id}>'


class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    purchase = db.relationship('Purchase', backref=db.backref('complaints', lazy=True))

    def __repr__(self):
        return f'<Complaint Purchase:{self.purchase_id}>'


class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    type = db.Column(db.String(50), nullable=False)  # e.g., 'Apple Pay', 'Card', 'PayPal'
    details = db.Column(db.String(200), nullable=True)  # e.g., masked card number, PayPal email

    user = db.relationship('User', backref=db.backref('payment_method', uselist=False))

    def __repr__(self):
        return f'<PaymentMethod {self.type} for User:{self.user_id}>'

