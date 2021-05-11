from app import app
from flask import render_template, redirect, url_for, request
from flask_login import current_user, logout_user, login_user, login_required, LoginManager
from werkzeug.security import check_password_hash
from models import User

login_app = LoginManager(app)


@login_app.user_loader
def load_user(id):
    return User.query.get(id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = User.query.filter_by(name=name).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('admin'))

        return redirect(url_for('login'))

    return render_template('admin/login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
