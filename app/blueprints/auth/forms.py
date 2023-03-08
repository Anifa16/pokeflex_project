from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo
from app.models import User

# FORMS SECTION
class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired()],render_kw={"placeholder":"Email"})
    password = PasswordField('Password:', validators=[DataRequired()],render_kw={"placeholder":"Passward"})
    submit_btn = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()],render_kw={"placeholder":"AnifaName"})
    last_name = StringField('Last Name:', validators=[DataRequired()],render_kw={"placeholder":"LastName"})
    email = EmailField('Email:', validators=[DataRequired()],render_kw={"placeholder":"Email"})
    password = PasswordField('Password: ', validators=[DataRequired()],render_kw={"placeholder":"Passward"})
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password')],render_kw={"placeholder":"Confirm Passward"})
    submit_btn = SubmitField('Register')

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()],render_kw={"placeholder":"AnifaName"})
    last_name = StringField('Last Name:', validators=[DataRequired()],render_kw={"placeholder":"LastName"})
    email = EmailField('Email:', validators=[DataRequired()],render_kw={"placeholder":"Email"})
    submit_btn = SubmitField('Update')

