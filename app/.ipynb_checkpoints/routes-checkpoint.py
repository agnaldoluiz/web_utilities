from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
# import sqlite3
import pandas as pd


googleSheetId = '12MX7va9uq9Uy99Ev7qNIqDKmAFwNTbLGt7DNfyB83Nk'
worksheetName = 'Sheet1'
URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
    googleSheetId,
    worksheetName
)

access = pd.read_csv(URL)
access['DataInicio'] = pd.to_datetime(access['DataInicio'], errors='coerce')
access['DataFim'] = pd.to_datetime(access['DataFim'], errors='coerce')

email_senha = {'agnaldo.cunha@kearney.com': '9E%He7', 'claudio.goncalves@kearney.com': 'E8n*2d'}
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