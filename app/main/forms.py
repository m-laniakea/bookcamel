##
# Forms file
# Contains forms and validators
##
from flask import flash, redirect, url_for
from sqlalchemy import func
from flask.ext.login import login_user
from flask.ext.wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, ValidationError, IntegerField, DecimalField
from wtforms.validators import Required, Email, Length, EqualTo, Regexp, NumberRange
from .. models import db, User
from . import main 
from . location_list import user_locations
from datetime import datetime


## 
# LoginForm to be displayed on the navbar
##
class LoginForm(Form):
    login = StringField('email or username', validators=[Required(), Length(1, 64) ])
    password = PasswordField('password', validators=[Required()])


##
# SignupForm for '/register'
##
class SignupForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('username', validators=[Required(), Length(1,64), Regexp('^[a-zA-Z0-9][\._a-zA-Z0-9]*$', 0, 
        'Your username may start with an upper- or lowercase letter or a number. Letters, numbers, underscores, and periods may follow.')])

    location = StringField('Location', validators=[Required(), Length(1,64)])

    password = PasswordField('Password', validators = [Required(), EqualTo('password_confirmation', message='Your passwords must match.')]) 
    password_confirmation = PasswordField('Confirm Password', validators = [Required()])

    submit = SubmitField("Register")
    
    # Uncomment to enable ReCaptcha for registration
    # captcha = RecaptchaField()

    # Check if email already exists
    def validate_email(self, field):
        email = field.data.lower()

        if User.query.filter_by( email = email ).first():
            raise ValidationError('Email already in use.')

    # Check if username exists
    def validate_username(self, field):
        name = field.data.lower()
        if User.query.filter(func.lower(User.username) == name).first(): 
            raise ValidationError('Username already taken. Ignoring capitalization, your username must be unique.')


    # Check if location is on the list
    def validate_location(self, field):
        for l in user_locations:
            if l == field.data:
                # Matching location found
                return;
        # else (No matching location found)
        raise ValidationError('Please use an approved location. Type more slowly to see the available choices.')
##
# EditProfileForm for '/editprofile'
##
class EditProfileForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('username', validators=[Required(), Length(1,64), Regexp('^[a-zA-Z0-9][\._a-z0-9]*$', 0, 
        'Your username may start with an upper- or lowercase letter or a number. Only lowercase letters, numbers, underscores, and periods may follow.')])

    location = StringField('Location', validators=[Required(), Length(1,64)])

    password = PasswordField('Password', validators = [Required(), EqualTo('password_confirmation', message='Your passwords must match.')]) 
    password_confirmation = PasswordField('Confirm Password', validators = [Required()])

    submit = SubmitField("Save")
    

##
# BookForm form for '/add' + editing books
##
class BookForm(Form):
    title = StringField('Title', validators=[Required(), Length(1,128)])
    author = StringField('Author', validators=[Required(), Length(1,128)])
    condition = IntegerField('Condition', validators=[Required(), NumberRange(1,5)])
    isbn = StringField('ISBN13', validators=[Required()])
    price = DecimalField('Price', validators=[NumberRange(0,8888.89)] )

    submit = SubmitField("Save")


    def validate_isbn(self, field):

        if len(field.data) != 13:
            raise ValidationError('ISBN-13 code must have 13 digits')


##
# MessageForm for conversations
##
class MessageForm(Form):
    text = StringField('Text', validators=[Required(), Length(2, 256)])
    submit = SubmitField("Send")


##
# Conversation initiator for books page
##
class ConvInitForm(Form):
    submit = SubmitField("Contact Owner")



##
# Collect errors from form fields
# flash to user
##
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("%s field: %s" % (getattr(form, field).label.text, error), 'danger')


##
# Check LoginForm data against db
# Log in user if checks pass
##
def process_login(form):
    login_key = form.login.data.strip().lower()
    user = User.query.filter_by(email=login_key).first()

    # Check if user entered username instead
    if user is None:
        user = User.query.filter(func.lower(User.username) == login_key).first()

    if user is not None and user.check_password(form.password.data):
        login_user(user, True)
        user.is_online = True
        db.session.commit()
        flash('Welcome back, ' + user.username + '.', 'success')
        return True

    flash('Invalid email + password combination.', 'danger')
    return False


class SearchForm(Form):
    location = StringField('Location', validators=[Required(), Length(1,64)])
    search = StringField('Search Terms', validators=[Required(), Length(1,128)])
    submit = SubmitField('Search')
