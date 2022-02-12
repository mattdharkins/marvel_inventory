from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired(), EqualTo('confirm', message='Make sure to enter correct password')])
    confirm = PasswordField('Repeat Password')
    submit_button = SubmitField()

class UserSignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired(), EqualTo('confirm', message='Make sure to enter correct password')])
    confirm = PasswordField('Repeat Password')
    submit_button = SubmitField()
