from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from project.modles import User
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user


class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class registerForm(FlaskForm):
    userName = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    passwordConfirm = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Register')

    def validate_userName(self, userName):
        if User.query.filter_by(userName=self.userName.data).first():
            raise ValidationError('Username Taken')

    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email registered !')


class accountUpdate(FlaskForm):
    profilePic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    profileBg = FileField('Background Picture', validators=[FileAllowed(['jpg', 'png'])])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio', render_kw={"rows": 4, "cols": 100}, validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if self.email.data != current_user.email:
            if User.query.filter_by(email=self.email.data).first():
                raise ValidationError('Email already in use')
