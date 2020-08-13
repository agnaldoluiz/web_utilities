from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
import sqlite3
import pandas as pd

conn = sqlite3.connect('contacts.db')
contacts = pd.read_sql_query("SELECT * from contacts", conn)
email_senha = pd.Series(contacts.senha.values, index=contacts.email).to_dict()
#from flask_login import current_user, login_user

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	#if current_user.is_authenticated:
    #    return redirect(url_for('test'))
    form = LoginForm()
    if form.validate_on_submit():
        pwd = form.password.data
        email = form.email.data
        # user = 'random'
        if email in email_senha and pwd == email_senha[email]:
            return redirect(url_for('ups'))
        else:
            flash('Password Incorrect. Try again')
            # login_user(user)
            return redirect(url_for('index'))
    return render_template('cover.html', form=form)

@app.route('/ups', methods=['GET', 'POST'])
def ups():
    return render_template('ups.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/usecase/<number>')
def usecase(number):
	name = request.args.get('name')
	return render_template('usecase.html', number=number, name=name)