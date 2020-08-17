from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    style_pwd = {'class': 'form-control mr-sm-2', 'placeholder': 'Password'}
    style_email = {'class': 'form-control mr-sm-2', 'placeholder': 'E-mail'}
    style_sbm = {'class': 'btn btn-md btn-secondary'}
    email = StringField('Email', validators=[Email()], render_kw=style_email)
    password = PasswordField('Password', validators=[DataRequired()], render_kw=style_pwd)
    submit = SubmitField('Access', render_kw=style_sbm)

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')