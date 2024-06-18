from flask_login import login_user

from flask import Blueprint, render_template, request, redirect, url_for

from app.utils.config import EMAIL_REGEX
from app.auth.models import User
from app.extensions import db

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']

        if not EMAIL_REGEX.match(email):
            return render_template('auth/register.html', error='Invalid email address')
        
        if User.query.filter(db.func.lower(User.email) == email.lower()).first():
            return render_template('auth/register.html', error='Email address already in use')

        password = request.form['password']

        if len(password) < 8:
            return render_template('auth/register.html', error='Invalid password')
        
        user = User(email=email, password=password)

        db.session.add(user)
        db.session.commit()

        login_user(user)

    return render_template('auth/register.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.authenticate(email, password)

        if not user:
            return render_template('auth/login.html', error='Invalid email address or password')
        
        login_user(user)

        return redirect(url_for('main.index'))

    return render_template('auth/login.html')
