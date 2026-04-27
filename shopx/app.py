import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
import resend

load_dotenv()

app = Flask(__name__)

# App configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-me')

# Primary option: single DATABASE_URL
# Fallback option: TiDB split variables (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT)
database_uri = os.getenv('DATABASE_URL')
if not database_uri:
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    db_port = os.getenv('DB_PORT', '4000')

    if all([db_host, db_user, db_password, db_name]):
        database_uri = (
            f"mysql+pymysql://{quote_plus(db_user)}:{quote_plus(db_password)}"
            f"@{db_host}:{db_port}/{db_name}?ssl_verify_cert=true&ssl_verify_identity=true"
        )

if not database_uri:
    database_uri = 'sqlite:///shopx.db'

if database_uri.startswith('postgres://'):
    database_uri = database_uri.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

resend_api_key = os.getenv('RESEND_API_KEY')
if resend_api_key:
    resend.api_key = resend_api_key

paystack_public_key = os.getenv('PAYSTACK_PUBLIC_KEY', '')
paystack_merchant_email = os.getenv('PAYSTACK_MERCHANT_EMAIL', '')


@app.context_processor
def inject_public_config():
    return {
        'PAYSTACK_PUBLIC_KEY': paystack_public_key,
        'PAYSTACK_MERCHANT_EMAIL': paystack_merchant_email,
    }


# Database Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(500), nullable=True)
    city = db.Column(db.String(100), nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Routes
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/products')
def products():
    return render_template('products.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        confirm_password = request.form.get('confirm_password') or ''

        if not email or not password:
            flash('Email and password are required.', 'danger')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        if resend_api_key:
            try:
                resend.Emails.send(
                    {
                        'from': 'onboarding@resend.dev',
                        'to': email,
                        'subject': 'Welcome to ShopX!',
                        'html': f'<strong>Welcome to the ShopX family!</strong><p>Your account for {email} has been created successfully.</p>',
                    }
                )
            except Exception as e:
                print(f'Error sending email: {e}')

        flash('Account created. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))

        flash('Login unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.phone = request.form.get('phone')
        current_user.address = request.form.get('address')
        current_user.city = request.form.get('city')
        db.session.commit()
        flash('Profile updated!', 'success')
    return render_template('profile.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/checkout_details', methods=['POST'])
@login_required
def checkout_details():
    current_user.phone = request.form.get('phone')
    current_user.address = request.form.get('address')
    current_user.city = request.form.get('city')
    db.session.commit()
    return {'status': 'success'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
