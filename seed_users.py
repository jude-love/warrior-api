from models import db, User, Product, Purchase, Complaint, PaymentMethod
from faker import Faker
import random

fake = Faker()

def create_random_data(app):
    with app.app_context():
        # Create users
        users = []
        for _ in range(20):
            username = fake.user_name()
            email = fake.email()
            user = User(username=username, email=email)
            db.session.add(user)
            users.append(user)
        db.session.commit()

        # Create products
        products = []
        for _ in range(5):
            name = fake.word().capitalize()
            price = round(random.uniform(10, 100), 2)
            product = Product(name=name, price=price)
            db.session.add(product)
            products.append(product)
        db.session.commit()

        # Create payment methods
        payment_types = ['Apple Pay', 'Card', 'PayPal']
        for user in users:
            payment_type = random.choice(payment_types)
            details = None
            if payment_type == 'Card':
                details = f"**** **** **** {random.randint(1000, 9999)}"
            elif payment_type == 'PayPal':
                details = fake.email()
            payment_method = PaymentMethod(user_id=user.id, type=payment_type, details=details)
            db.session.add(payment_method)
        db.session.commit()

        # Create purchases
        purchases = []
        for user in users:
            for _ in range(10):
                product = random.choice(products)
                payment_method = PaymentMethod.query.filter_by(user_id=user.id).first()
                purchase = Purchase(user_id=user.id, product_id=product.id, payment_method_id=payment_method.id)
                db.session.add(purchase)
                purchases.append(purchase)
        db.session.commit()

        # Add complaints for 4 customers (one complaint each)
        for user in users[:4]:
            user_purchases = Purchase.query.filter_by(user_id=user.id).all()
            if user_purchases:
                purchase = random.choice(user_purchases)
                complaint = Complaint(
                    purchase_id=purchase.id,
                    description=fake.sentence(nb_words=12)
                )
                db.session.add(complaint)
        db.session.commit()

        print("20 random users, 5 products, payment methods, ~10 purchases per user, and complaints for 4 customers created.")