from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from .models import Product, Location, ProductMovement, User
from aerele import db
from functools import wraps

main = Blueprint('main', __name__)

@main.before_request #authentication before entering the login or signup page 
def require_login():
    allowed_routes = ['main.login', 'main.signup', 'static']
    if request.endpoint not in allowed_routes and 'user_id' not in session:
        return redirect(url_for('main.login'))
@main.before_request #csrf 
def log_csrf_token():
    current_app.logger.info(f"CSRF Token in session: {request.cookies.get('csrf_token')}")
#----routes for the templates---!!
@main.route('/signup', methods=['GET', 'POST']) #function for signup page
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please log in.', 'danger')
            return redirect(url_for('main.login'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created. Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('signup.html')

@main.route('/login', methods=['GET', 'POST']) #funtion for login page
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('main.products'))
        else:
            return render_template('login.html', error_message='Invalid username or password.')
    return render_template('login.html')

@main.route('/logout')
def logout(): # function to logout 
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))

@main.route('/', methods=['GET'])
def products():
    products = Product.query.all() # showing the products in webpage
    return render_template('product.html', products=products)

@main.route('/locations', methods=['GET'])
def locations():
    locations = Location.query.all() # showing the location in webpage
    return render_template('location.html', locations=locations)

@main.route('/movements', methods=['GET', 'POST'])
def movements():  # there are 3 type of transactions 
    if request.method == 'POST':
        transaction_type = request.form['transaction_type']
        product_id = request.form['product_id']
        from_location = request.form.get('from_location') or None
        to_location = request.form.get('to_location') or None
        quantity = int(request.form['quantity'])
        product = Product.query.get(product_id)
        if not product:
            flash('Product not found.', 'error')
            return redirect(url_for('main.movements'))
        if transaction_type == 'purchase': #unknown to hub
            if not to_location:
                flash('Destination location is required.', 'error')
                return redirect(url_for('main.movements'))
            if quantity > product.quantity:
                flash(f'Insufficient stock. Available: {product.quantity}', 'error')
                return redirect(url_for('main.movements'))
            product.quantity -= quantity
            db.session.add(product)
        elif transaction_type == 'move': #hub to hub
            if not from_location or not to_location:
                flash('Both source and destination required.', 'error')
                return redirect(url_for('main.movements'))
            balance = db.session.query(
                db.func.sum(
                    db.case(
                        (ProductMovement.to_location == from_location, ProductMovement.quantity),
                        else_=0
                    ) - db.case(
                        (ProductMovement.from_location == from_location, ProductMovement.quantity),
                        else_=0
                    )
                )
            ).filter(ProductMovement.product_id == product_id).scalar() or 0

            if quantity > balance:
                flash(f'Insufficient stock in source location: {balance}', 'error')
                return redirect(url_for('main.movements'))
        elif transaction_type == 'sale': # hub to unknown
            if not from_location:
                flash('Source location is required.', 'error')
                return redirect(url_for('main.movements'))
            balance = db.session.query(
                db.func.sum(
                    db.case(
                        (ProductMovement.to_location == from_location, ProductMovement.quantity),
                        else_=0
                    ) - db.case(
                        (ProductMovement.from_location == from_location, ProductMovement.quantity),
                        else_=0
                    )
                )
            ).filter(ProductMovement.product_id == product_id).scalar() or 0
            if quantity > balance:
                flash(f'Insufficient stock in source location: {balance}', 'error')
                return redirect(url_for('main.movements'))
        new_movement = ProductMovement(
            product_id=product_id,
            from_location=from_location,
            to_location=to_location,
            quantity=quantity
        )
        db.session.add(new_movement)
        db.session.commit()
        flash('Movement recorded successfully!', 'success')
        return redirect(url_for('main.movements'))
    movements = ProductMovement.query.all()
    locations = Location.query.all()
    products = Product.query.all()
    balances = db.session.query(
        Product.name.label('product'),
        Location.name.label('warehouse'),
        db.func.sum(
            db.case(
                (ProductMovement.to_location == Location.id, ProductMovement.quantity),
                else_=0
            ) - db.case(
                (ProductMovement.from_location == Location.id, ProductMovement.quantity),
                else_=0
            )
        ).label('qty')
    ).join(ProductMovement, Product.id == ProductMovement.product_id).join(
        Location, db.or_(
            ProductMovement.to_location == Location.id,
            ProductMovement.from_location == Location.id
        )
    ).group_by(Product.id, Location.id).all()
    from_loc = db.aliased(Location)
    to_loc = db.aliased(Location)
    transactions = db.session.query(
        ProductMovement.timestamp,
        Product.name.label('product'),
        from_loc.name.label('from_location'),
        to_loc.name.label('to_location'),
        ProductMovement.quantity
    ).join(Product, ProductMovement.product_id == Product.id).join(
        from_loc, ProductMovement.from_location == from_loc.id, isouter=True
    ).join(
        to_loc, ProductMovement.to_location == to_loc.id, isouter=True
    ).all()
    return render_template('movement.html', movements=movements, balances=balances, locations=locations, products=products, transactions=transactions)

@main.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id): # for editing the product function
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.quantity = request.form['quantity']
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('main.products'))
    return render_template('edit_product.html', product=product)

@main.route('/edit_location/<int:id>', methods=['GET', 'POST'])
def edit_location(id):# editing the location function 
    location = Location.query.get_or_404(id)
    if request.method == 'POST':
        location.name = request.form['name']
        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('main.locations'))
    return render_template('edit_location.html', location=location)

@main.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):# delete the product by id 
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'success')
    return redirect(url_for('main.products'))

@main.route('/delete_location/<int:id>', methods=['POST'])
def delete_location(id):# delete the location by id
    location = Location.query.get_or_404(id)
    db.session.delete(location)
    db.session.commit()
    flash('Location deleted.', 'success')
    return redirect(url_for('main.locations'))

@main.route('/add_product', methods=['POST'])
def add_product():# function to add the product and updating in product.html page
    name = request.form['name']
    quantity = int(request.form['quantity'])
    new_product = Product(name=name, quantity=quantity)
    db.session.add(new_product)
    db.session.commit()
    flash('Product added successfully!', 'success')
    return redirect(url_for('main.products'))

@main.route('/add_location', methods=['POST'])
def add_location():# function for adding the location and updating in location page
    name = request.form['name']
    new_location = Location(name=name)
    db.session.add(new_location)
    db.session.commit()
    flash('Location added successfully!', 'success')
    return redirect(url_for('main.locations'))

@main.route('/clear_transactions', methods=['POST'])
def clear_transactions(): # function for clear the transaction for deleting all type of trasactions 
    db.session.query(ProductMovement).delete()
    db.session.commit()
    flash('All transactions cleared.', 'success')
    return redirect(url_for('main.movements'))

@main.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query', '').strip()         
    # Search in product balances
    balances = db.session.query(
        Product.name.label('product'),
        Location.name.label('warehouse'),
        db.func.sum(
            db.case(
                (ProductMovement.to_location == Location.id, ProductMovement.quantity),
                else_=0) - db.case((ProductMovement.from_location == Location.id, ProductMovement.quantity),
                else_=0 )).label('qty')).join(ProductMovement, Product.id == ProductMovement.product_id).join(
                Location, db.or_(ProductMovement.to_location == Location.id,ProductMovement.from_location == Location.id
        )).filter(db.or_(
            Product.name.ilike(f"%{query}%"),
            Location.name.ilike(f"%{query}%")
        )).group_by(Product.id, Location.id).all()

    from_loc = db.aliased(Location)   # Search in transaction history
    to_loc = db.aliased(Location)
    transactions = db.session.query(
        ProductMovement.timestamp,
        Product.name.label('product'),
        from_loc.name.label('from_location'),
        to_loc.name.label('to_location'),
        ProductMovement.quantity
    ).join(Product, ProductMovement.product_id == Product.id).join(
        from_loc, ProductMovement.from_location == from_loc.id, isouter=True ).join(
        to_loc, ProductMovement.to_location == to_loc.id, isouter=True).filter(
        db.or_(
            Product.name.ilike(f"%{query}%"),
            from_loc.name.ilike(f"%{query}%"),
            to_loc.name.ilike(f"%{query}%")
        )).all()
    return render_template('search_results.html', balances=balances, transactions=transactions, query=query)

