from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from blueprints.shorter.models import Url
from werkzeug.security import generate_password_hash, check_password_hash
from blueprints import db


# Blueprint configuration
login = Blueprint(
    "login", __name__, template_folder="templates", static_folder="static")


@login.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        # Forms
        username = request.form['username']
        password = request.form['password']
        if current_user.is_authenticated:
            flash("Вы уже авторизованы.")
            return redirect('/')
        if username and password:
            # Find user
            user = User.query.filter(User.username == username).first()
            if user:
                # Check password
                if check_password_hash(user.password, password):
                    login_user(user)
                    flash('Успешная авторизация')

                    return redirect('/')
                else:
                    flash('Неккоректный логин или пароль.')
                    return redirect('/login')
            else:
                flash('Данного пользователя не существует.')
                return redirect('/login')
        else:
            flash('Поля неккоректно заполнены.')
            return redirect('/login')
    return render_template('login.html')


@login.route('/register', methods=['POST'])
def user_register():
    # Forms
    username = request.form['reg-username']
    password = request.form['reg-password']
    if current_user.is_authenticated:
        flash("Вы уже авторизованы.")
        return redirect('/')
    if username and password:
        # Find user
        user = User.query.filter(User.username == username).first()
        # If user is not found(not registered)
        if not user:
            new_user = User(
                username=username,
                password=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()

            # Login user
            login_user(new_user)
            flash('Пользователь успешно зарегистрирован.')

            return redirect('/')
        else:
            flash('Данный пользователь уже зарегистрирован.')
            return redirect('/login')
    else:
        flash('Поля неккоректно заполнены.')
        return redirect('/login')


# Logout
@login.route('/logout', methods=['GET', 'POST'])
@login_required
def user_logout():
    logout_user()

    flash('Вы успешно вышли из аккаунта.')
    return redirect('/')


# Profile
@login.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    # Find all links where current_user is creator
    user_urls = Url.query.filter(Url.creator == current_user.username).all()
    return render_template('profile.html', user_urls=user_urls)
