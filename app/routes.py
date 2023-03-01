from app import app
from .models import User
from flask import render_template, flash, redirect
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {"username": "Ira"}
    services = [
        {
            'author': {'username': 'Ira'},
            'description': 'AI model that sorts photos.'
        },
        {
            'author': {'username': 'Stap'},
            'description': 'AI that improves photo quality.'
        }]
    return render_template('index.html', title='Home', user=user, services=services)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login request for user {}, remember me={}'.format(form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/users/', methods=['GET'])
def get_users():
    user = User(username='Oliver', password='feeding')
    result = {"username": user.username,
              "password": user.password}

    return result
