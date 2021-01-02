from flask import render_template, Blueprint, redirect, url_for,flash
from flask_login import login_user, current_user, logout_user, login_required
from application import db
from application.models import UserModel
from application.users.forms import LoginForm, RegistrationForm
from application.fhir.search import ResourceFinder

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        patient = ResourceFinder.find_by_identifier(
            'Patient',
            form.identifier_system.data,
            form.identifier_value.data,
            first=True
        )

        if not patient:
            flash(f'No patient record found, please check again. If you keep failing the verification, please contact your provider.')

        else:
            check_patient_duplicated = UserModel.query.filter_by(patient_id=patient.id).first()
            check_dob_matched = patient.birthDate.date == form.date_of_birth.data
            check_family_matched = patient.name[0].family == form.family_name.data

            if check_patient_duplicated:
                flash(f'The patient has been registered already.')
            elif not (check_dob_matched or check_family_matched):
                flash(f'No patient record found, please check again. If you keep failing the verification, please contact your provider.')
            else:
                user = UserModel(
                    given_name=patient.name[0].given[0],
                    family_name=form.family_name.data,
                    date_of_birth= form.date_of_birth.data,
                    identifier_system=form.identifier_system.data,
                    identifier_value=form.identifier_value.data,
                    patient_id=patient.id,
                    email=form.email.data,
                    password=form.password.data
                )

                db.session.add(user)
                db.session.commit()
                flash(f'Welcome {patient.name[0].given[0]}! Please login now.')
                return redirect(url_for('users.login'))
    else:
        print('failed validation')
    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        print(user)
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.given_name}!')
            return redirect(url_for('core.main'))

        else:
            flash('Incorrect email or password, please try again.')
            return redirect(url_for('users.login'))

    return render_template('login.html', form=form)


@users.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('core.welcome'))
