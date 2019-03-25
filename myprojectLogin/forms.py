# forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from wtforms.fields.html5 import DateField


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired(), EqualTo('pass_confirm', message = 'Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password', validators = [DataRequired()])
    submit = SubmitField('Sign Up')

    def check_email(self):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been already registered')

    def check_username(self):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is Taken!')


class AddForm(FlaskForm):
    ID = IntegerField('CodeID:', validators = [DataRequired()])
    location = StringField('Locations:', validators = [DataRequired()])
    drawcode = StringField('Drawing No.:',  validators = [DataRequired()])
    description = StringField('Description:',  validators = [DataRequired()])
    draw_date = DateField('Date Submitted:',  format='%Y-%m-%d', validators = [DataRequired()])
    submit = SubmitField('Submit')


class DelForm(FlaskForm):
    id = IntegerField('please type the CodeID',  validators = [DataRequired()])
    submit = SubmitField('Delete')


class Dowload_File(FlaskForm):
     donwload_button= SubmitField('Download Sample')

