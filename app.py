from flask import Flask, jsonify, request
from models import db, User, Product, Purchase, Complaint, PaymentMethod
from config import Config
from seed_users import create_random_data

# Add Flask-Admin imports
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Create tables when the app starts
with app.app_context():
    db.create_all()

# Set up Flask-Admin
admin = Admin(app, name='WarriorCRM Admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Purchase, db.session))
admin.add_view(ModelView(Complaint, db.session))
admin.add_view(ModelView(PaymentMethod, db.session))

@app.route('/')
def home():
    return "Flask app is running!"

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'email': u.email} for u in users])

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created!'}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

# --- Product Endpoints ---

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price} for p in products])

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created!'}), 201

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price})

# --- Purchase Endpoints ---

@app.route('/purchases', methods=['GET'])
def get_purchases():
    purchases = Purchase.query.all()
    return jsonify([
        {
            'id': p.id,
            'user_id': p.user_id,
            'product_id': p.product_id,
            'payment_method_id': p.payment_method_id,
            'timestamp': p.timestamp.isoformat() if p.timestamp else None
        } for p in purchases
    ])

@app.route('/purchases', methods=['POST'])
def add_purchase():
    data = request.get_json()
    new_purchase = Purchase(
        user_id=data['user_id'],
        product_id=data['product_id'],
        payment_method_id=data['payment_method_id']
    )
    db.session.add(new_purchase)
    db.session.commit()
    return jsonify({'message': 'Purchase created!'}), 201

@app.route('/purchases/<int:purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    return jsonify({
        'id': purchase.id,
        'user_id': purchase.user_id,
        'product_id': purchase.product_id,
        'payment_method_id': purchase.payment_method_id,
        'timestamp': purchase.timestamp.isoformat() if purchase.timestamp else None
    })

@app.route('/complaints/<int:complaint_id>', methods=['GET'])
def get_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    return jsonify({
        'id': complaint.id,
        'purchase_id': complaint.purchase_id,
        'description': complaint.description,
        'created_at': complaint.created_at.isoformat() if complaint.created_at else None
    })

@app.route('/payment_methods/<int:payment_method_id>', methods=['GET'])
def get_payment_method(payment_method_id):
    payment_method = PaymentMethod.query.get_or_404(payment_method_id)
    return jsonify({
        'id': payment_method.id,
        'user_id': payment_method.user_id,
        'type': payment_method.type,
        'details': payment_method.details
    })

@app.cli.command('seed-data')
def create_random_data_command():
    """Create random data for the application."""
    create_random_data(app)
    print("Random data created successfully.")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
