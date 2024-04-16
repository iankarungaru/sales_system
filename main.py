from flask import Flask, flash, render_template, request, redirect, session, url_for
from database import (
    insert_products, get_data, insert_sales, sales_product,
    profit_product, daily_sales, daily_profit, register_user,
    authenticate_user, delete_product
)
from models import Product, Sale

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def hello():
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Your dashboard code here...
    return render_template('dashboard.html')

@app.route('/products')
def products():
    prods = get_data("products")
    return render_template("products.html", products=prods)

@app.route('/add_products', methods=['POST'])
def add_products():
    if request.method == 'POST':
        name = request.form['name']
        buying_price = request.form['buying_price']
        selling_price = request.form['selling_price']
        stock_quantity = request.form['quantity_stock']
        value = (name, buying_price, selling_price, stock_quantity)
        insert_products(value)
        return redirect(url_for('products'))

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product_route(product_id):
    if request.method == 'POST':
        delete_product(product_id)
    return redirect(url_for('products'))

@app.route('/sales')
def sales():
    sale = get_data("sales")
    products = get_data("products")
    return render_template('sales.html', sales=sale, products=products)

@app.route('/make_sales', methods=['POST'])
def make_sales():
    pid = request.form['pid']
    quantity = request.form['quantity']
    sale = (pid, quantity)
    insert_sales(sale)
    return redirect(url_for('sales'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        
        if register_user((fullname, email, password)):
            return redirect(url_for('index'))  # Redirect to index.html upon successful registration
        else:
            return render_template('login_or_register.html', error="Email already exists")
    else:
        return render_template('login_or_register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_email = request.form['login_email']
        login_password = request.form['login_password']
        
        if authenticate_user(login_email, login_password):
            session['email_address'] = login_email
            return redirect(url_for('index'))  # Redirect to index.html upon successful login
        else:
            return render_template('login_or_register.html', error="Invalid email or password")
    else:
        return render_template('login_or_register.html')

@app.route('/logout')
def logout():
    session.pop('email_address', None)
    flash("Logged Out", "success")
    return redirect(url_for('login_or_register'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        print("Name:", name)
        print("Email:", email)
        print("Subject:", subject)
        print("Message:", message)
        
        message="your message has been submitted successfully"
        return redirect(url_for('thank_you'))

    return render_template('contact.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
