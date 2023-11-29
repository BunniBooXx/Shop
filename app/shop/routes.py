from flask import Flask, render_template, request, redirect, url_for, session
from . import shop
from flask import jsonify
from flask_login import login_required
from ..models import db, User, Product, Cart, CartItem, Order, OrderItem



@shop.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@shop.route('/test')
def test(): 
    products = Product.query.all()
    products_list = []
    for product in products:
        product_object = {
            "id" : product.id, 
            "product_name" : product.product_name, 
            "description": product.description, 
            "price": product.price, 
            "stock_quantity": product.stock_quantity
        }
        products_list.append(product_object)
    return products_list



@shop.route('/product/<int:product_id>')
def product(product_id):
    selected_product = Product.query.get_or_404(product_id)
    product_object = {
        "id": selected_product.id,
        "product_name": selected_product.product_name,
        "description": selected_product.description,
        "price": selected_product.price,
        "stock_quantity": selected_product.stock_quantity
    }
    return render_template('product.html', product=product_object)




@shop.route('/cart')
def cart():
    if 'user' not in session:
        return redirect(url_for('shop.login'))

    user = User.query.filter_by(username=session['user']).first()

    if not user:
        return redirect(url_for('shop.login'))

    cart = Cart.query.filter_by(user_id=user.id).first()

    if not cart:
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()

    if cart:
        cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
        total = sum(item.product_price * item.quantity for item in cart_items)
    else:
        cart_items = []
        total = 0

    return render_template('cart.html', cart_items=cart_items, total=total, cart = cart)



@login_required
@shop.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user' not in session:
        return redirect(url_for('shop.login'))

    user = User.query.filter_by(username=session['user']).first()

    if not user:
        return redirect(url_for('shop.login'))

    product = Product.query.get_or_404(product_id)
    cart = Cart.query.filter_by(user_id=user.id).first()

    if cart is None:
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem(
        cart_id=cart.id,
        user_id=user.id,
        product_id=product.id,
        product_price=product.price,
        quantity=1
    )

    db.session.add(cart_item)
    db.session.commit()

    return redirect(url_for('shop.cart'))


@shop.route('/remove_from_cart/<int:cart_item_id>', methods=['POST'])
def remove_from_cart(cart_item_id):
    if 'user' not in session:
        return redirect(url_for('shop.login'))

    user = User.query.filter_by(username=session['user']).first()
    cart = Cart.query.filter_by(user_id=user.id).first()

    if cart:
        cart_item = CartItem.query.filter_by(id=cart_item_id, cart_id=cart.id).first()

        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()

    return redirect(url_for('shop.cart'))

@shop.route('/remove_all_from_cart', methods=['POST'])
def remove_all_from_cart():
    if 'user' not in session:
        return redirect(url_for('shop.login'))

    user = User.query.filter_by(username=session['user']).first()
    cart = Cart.query.filter_by(user_id=user.id).first()

    if cart:
        # Delete all cart items associated with the cart
        CartItem.query.filter_by(cart_id=cart.id).delete()

        db.session.commit()

    return redirect(url_for('shop.cart'))


@shop.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock_quantity = int(request.form.get('stock_quantity'))

        new_product = Product(product_name=product_name, description=description, price=price, stock_quantity=stock_quantity)

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('shop.index'))

    return render_template('addproduct.html')



@shop.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('signup.html', message='Username already exists. Please choose a different one.')

      
        new_user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name, address=address)

       
        db.session.add(new_user)
        db.session.commit()

        session['user'] = username  
        return redirect(url_for('shop.index'))

    return render_template('signup.html')

@shop.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user'] = username
            return redirect(url_for('shop.index'))

    return render_template('login.html')

@shop.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('shop.index'))


