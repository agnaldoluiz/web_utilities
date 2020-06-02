from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    style_pwd = {'class': 'form-control mr-sm-2', 'placeholder': 'Password'}
    style_sbm = {'class': 'btn btn-md btn-secondary'}
    password = PasswordField('Password', validators=[DataRequired()], render_kw=style_pwd)
    submit = SubmitField('Access', render_kw=style_sbm)