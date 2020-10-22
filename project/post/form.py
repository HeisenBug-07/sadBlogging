from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class addPost(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', render_kw={"rows": 16, "cols": 70}, validators=[DataRequired()])
    postImage = FileField('Post image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Create Post')


class updatePost(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', render_kw={"rows": 11, "cols": 70}, validators=[DataRequired()])
    postImage = FileField('Post image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Post')
