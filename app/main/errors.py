##
# Define possible errors & actions to take
##

from . import main
from ..models import User
from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import login_user
from forms import LoginForm, process_login


##
# This page will be loaded when the server fails to find a requested page
##
@main.app_errorhandler(404)
def page_not_found(e):

    form = LoginForm()

    if form.validate_on_submit():
        process_login(form)

    flash('The page requested could not be found. Here\'s a haiku instead.', 'info')
    return render_template('404.html', form=form), 404

##
# Define action for internal server error
##
@main.app_errorhandler(500)
def error_internal(e):

    form = LoginForm()

    if form.validate_on_submit():
        process_login(form)

    return render_template('500.html', form=form), 500
