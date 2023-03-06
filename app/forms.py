from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo

#forms
class LoginForm(FlaskForm):
    email=EmailField('email', validators=[DataRequired()],render_kw={"placeholder": "Email"})
    password =PasswordField('password', validators=[DataRequired()],render_kw={"placeholder": "Password"})
    submit=SubmitField('Submit')

class RegistrationForm(FlaskForm):
    first_name=StringField('First Name', validators=[DataRequired()],render_kw={"placeholder": "FirstName"})
    last_name=StringField('Last Name', validators=[DataRequired()],render_kw={"placeholder": "LastName"})
    email=EmailField('email', validators=[DataRequired()],render_kw={"placeholder": "Email"})
    password=PasswordField('password', validators=[DataRequired()],render_kw={"placeholder": "password"})
    confirm_password =PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')],render_kw={"placeholder": "Password"})
    submit=SubmitField('SignUp')