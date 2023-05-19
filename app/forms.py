from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
                    BooleanField, SubmitField, \
                    TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class CompanyRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    contact = StringField('Contact Info', validators=[DataRequired()])
    submit = SubmitField('Create company')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please enter a different username, this one is taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Email doesn't exist.")

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Username already taken')


class ModelIdeaForm(FlaskForm):
    # username = StringField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    description = TextAreaField('Short description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class HairTransForm(FlaskForm):
    image = FileField('Image', id='image',
                      validators=[DataRequired(), FileAllowed(['jpeg', 'jpg', 'webp', 'png'], 'Images only!')])
    submit = SubmitField('Upload Image')


class WeightLossForm(FlaskForm):
    image = FileField('Image', id='image',
                      validators=[DataRequired(), FileAllowed(['jpeg', 'jpg', 'webp', 'png'], 'Images only!')])
    submit = SubmitField('Upload Image')


class MuscleGainForm(FlaskForm):
    image = FileField('Image', id='image',
                      validators=[DataRequired(), FileAllowed(['jpeg', 'jpg', 'webp', 'png'], 'Images only!')])
    submit = SubmitField('Upload Image')
