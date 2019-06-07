from wtforms import Form, StringField, PasswordField, SelectField, validators, TextAreaField
from models import Cities


class RegisterForm(Form):
    first = StringField('First Name', [validators.Length(min=1, max=50)])
    last = StringField('Last Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50),
                                  validators.Email(message="Please enter a valid email address")])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message="Passwords do not match")])
    confirm = PasswordField('Confirm Password')
    # generate select field of (id, name) or every city in the database
    city = SelectField('City', coerce=int,
                       choices=[(c.id, c.name) for c in Cities.query.order_by(Cities.name).all()])


class ContactForm(Form):
    name = StringField('Name', [validators.Length(min=3, max=100)])
    email = StringField('Email', [validators.Length(min=6, max=50),
                                  validators.Email(message="Please enter a valid email address")])
    subject = StringField('Name', [validators.Length(min=3, max=100)])
    message = TextAreaField('Message', [validators.Length(min=3, max=3000)])
