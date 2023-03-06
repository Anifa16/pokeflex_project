from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired

#forms
class LoginForm(FlaskForm):
    email=EmailField('email', validators=[DataRequired()],render_kw={"placeholder": "Email"})
    password =PasswordField('password', validators=[DataRequired()],render_kw={"placeholder": "Password"})
    submit=SubmitField('Submit')