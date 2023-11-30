from flask import Flask, render_template, request, redirect, url_for, session
from . import shop
from flask import request, make_response , jsonify
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_login import login_required, login_user, current_user
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
    return jsonify(product=product_object)

@shop.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    current_user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=current_user_id).all()

    print('cart items', cart_items)
    cart_data = [{'id': item.id, 'name': item.product.product_name, 'description': item.product.description, 'price': item.product_price} for item in cart_items]
    return jsonify({'cart': cart_data }), 200




@shop.route('/add_to_cart/<int:product_id>', methods=['POST'])
@jwt_required()
def add_to_cart(product_id):
    current_user_id = get_jwt_identity()

    product = Product.query.get_or_404(product_id)
    cart = Cart.query.filter_by(user_id=current_user_id).first()

    if cart is None:
        cart = Cart(user_id=current_user_id)
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem(
        cart_id=cart.id,
        user_id=current_user_id,
        product_id=product.id,
        product_price=product.price,
        quantity=1
    )

    db.session.add(cart_item)
    db.session.commit()

    return jsonify({'message': 'Product added to cart successfully'}), 200


@shop.route('/remove_all_from_cart', methods=['POST'])
@jwt_required()
def remove_all_from_cart():
    current_user_id = get_jwt_identity()

    cart = Cart.query.filter_by(user_id=current_user_id).first()

    if cart:
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()

        return jsonify({'message': 'All items removed from cart successfully'}), 200
    else:
        return jsonify({'message': 'User not found or cart is empty'}), 404



@shop.route('/remove_from_cart/<int:cart_item_id>', methods=['POST'])
@jwt_required()
def remove_from_cart(cart_item_id):
    current_user_id = get_jwt_identity()

    cart_item = CartItem.query.filter_by(id = cart_item_id).one_or_none()

    print('casrt_item', cart_item)

    if cart_item.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({'message': 'Item removed from cart successfully'}), 200




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
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        address = request.json.get('address')

        

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('signup.html', message='Username already exists. Please choose a different one.')

        print('password', password)
        new_user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name, address=address)

       
        db.session.add(new_user)
        db.session.commit()

        session['user'] = username  
        return redirect(url_for('shop.index'))

    return render_template('signup.html')



@shop.post("/login")
def handle_login(): 
    body = request.json

    if body is None: 
        response = {
            "message": "username and password are required to login"
        }
        return response,400
    
    username=body.get("username")
    if username is None:
        response = {
            "message": "username is required"
        }
        return response, 400
    
    password = body.get("password")
    if password is None: 
        response = {
            "message": "password is required"
        }
        return response, 400

    print('password', password)
    user = User.query.filter_by(username=username).one_or_none()
    if user is None: 
        response = {
            "message": "please create an account before trying to login"
        }
        return response, 400
    
    ok = user.compare_password(password)

    print('ok', ok)
    if not ok:
        response={
            "message": "invalid login"

        }
        return response, 401
    


    auth_token = create_access_token(identity=user, expires_delta=timedelta(days=1))

    response = make_response({"message": "successfully logged in", "auth_token" : auth_token})
     
    response.headers["Authorization"] = f"Bearer {auth_token}"
    return response , 200


@shop.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('shop.index'))


