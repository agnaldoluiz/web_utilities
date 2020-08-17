from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
import pandas as pd
from datetime import datetime, timedelta


googleSheetId = '12MX7va9uq9Uy99Ev7qNIqDKmAFwNTbLGt7DNfyB83Nk'
worksheetName = 'Sheet1'
URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
    googleSheetId,
    worksheetName
)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        today = datetime.now()
        return redirect(url_for('ups'))

    today = datetime.now()

    form = LoginForm()
    rform = RegistrationForm()

    # Registration
    if rform.validate_on_submit():
        user = User(email=rform.email.data)
        user.set_password(rform.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration complete!')
        return redirect(url_for('index'))

    # Login
    if form.validate_on_submit():
        access = pd.read_csv(URL)
        access['DataInicio'] = pd.to_datetime(access['DataInicio'], errors='coerce')
        access['DataFim'] = pd.to_datetime(access['DataFim'], errors='coerce')

        email = form.email.data
        user = User.query.filter_by(email=email).first()
        pwd = form.password.data

        # User doesn't exist or pwd is wrong
        if user is None or not user.check_password(pwd):
            flash('Invalid username or password')
            return redirect(url_for('index'))

        # User is not in the Google Sheets list
        if email not in access.Email.tolist():
            flash('Your e-mail is not enabled to access this content. Send an e-mail to diogo.cunha@kearney.com to get permission')
            return redirect(url_for('index'))

        # User time is expired
        if ((access[access.Email == email].AcessoConstante.iloc[0] == False) & ((access[access.Email == email].DataFim.iloc[0] + timedelta(days=1) > today) == False)):
            flash('Your 10-day free trial is expired. Send an e-mail to diogo.cunha@kearney.com to get info about how to get a new permission')
            return redirect(url_for('index'))
        
        login_user(user, remember=True)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('ups')
        return redirect(next_page)

    return render_template('cover.html', form=form, rform=rform)

@app.route('/ups', methods=['GET', 'POST'])
@login_required
def ups():
    # access = pd.read_csv(URL)
    # access['DataInicio'] = pd.to_datetime(access['DataInicio'], errors='coerce')
    # access['DataFim'] = pd.to_datetime(access['DataFim'], errors='coerce')
    # email = current_user.email
    # date= access[access.Email == email].DataFim.iloc[0]
    user = current_user.email
    return render_template('ups.html', user=user)

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
	return render_template('home.html')

@app.route('/usecase/<number>')
@login_required
def usecase(number):
	name = request.args.get('name')
	return render_template('usecase.html', number=number, name=name)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))