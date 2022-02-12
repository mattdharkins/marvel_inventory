# package imports
from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

# project file imports
from marvel_inventory.forms import UserLoginForm, UserSignupForm
from marvel_inventory.models import User,db, check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignupForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            print(email,password)

            # Add user to db
            user = User(first_name, last_name, email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account for {first_name} {last_name}', 'user-created')
            return redirect(url_for('auth.signin'))


    except:
        raise Exception('Invalid Form Data: Please check your form')

    return render_template('signup.html', form=form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            # Query user table for users with this info
            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in: Via Email/Password', 'auth-success')
                return redirect(url_for('site.home'))
            else:
                flash('Your Email/Password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))


    except:
        raise Exception('Invalid Form Data: Please check your form')

    return render_template('signin.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))

