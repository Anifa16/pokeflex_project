from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    img_url=StringField('Image Url', validators=[DataRequired()],render_kw={"placeholder": "Image"})
    title=StringField('Title', validators=[DataRequired()],render_kw={"placeholder": "Post title"})
    caption=StringField('Caption', validators=[DataRequired()],render_kw={"placeholder": "Caption"})
    submit=SubmitField('Post')