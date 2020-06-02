from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
#from flask_login import current_user, login_user

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	#if current_user.is_authenticated:
    #    return redirect(url_for('test'))
    form = LoginForm()
    if form.validate_on_submit():
        pwd = form.password.data
        # user = 'random'
        if pwd == 'Kearney2020':
            return redirect(url_for('home'))
        else:
            flash('Password Incorrect. Try again')
            # login_user(user)
            return redirect(url_for('index'))
    return render_template('cover.html', form=form)

@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/usecase/<number>')
def usecase(number):
	name = request.args.get('name')
	return render_template('usecase.html', number=number, name=name)