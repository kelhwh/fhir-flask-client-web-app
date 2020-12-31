from flask import render_template, Blueprint, redirect, url_for,flash
from flask_login import login_user, current_user, logout_user, login_required
from application import db
from application.models import UserModel
from application.users.forms import LoginForm, RegistrationForm

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = UserModel(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            date_of_birth=form.date_of_birth.data,
            insurance_id=form.insurance_id.data,
            email=form.email.data,
            password=form.password.data
        )

        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.first_name.data}! Please login now.')
        return redirect(url_for('users.login'))
    else:
        print('validation failed')
    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        print(user)
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.first_name}!')
            return redirect(url_for('core.main'))

        else:
            flash('Incorrect email or password, please try again.')
            return redirect(url_for('users.login'))

    return render_template('login.html', form=form)


@users.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('core.welcome'))
