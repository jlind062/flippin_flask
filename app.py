from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, PasswordField, SelectField, validators
from passlib.hash import sha256_crypt
from functools import wraps

# create the flask app from config file and instantiate db
app = Flask(__name__)
app.config.from_object('config.LocalConfig')
db = SQLAlchemy(app)
# have to pass in models after since it imports the db object
from models import Cities, Users


# custom decorator to verify user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash ("Please login to see this content.", "danger")
            return redirect(url_for('login'))
    return wrap


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = Users(first=form.first.data,
                         last=form.last.data,
                         email=form.email.data,
                         username=form.username.data,
                         city=form.city.data,
                         password=sha256_crypt.encrypt(str(form.password.data)))
        db.session.add(new_user)
        db.session.commit()
        flash('Welcome to flippin!\nYour account has been successfully created.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        result = Users.query.filter_by(username=username).first()
        if result is not None:
            password = result.password
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                session['city'] = result.city
                session['city_name'] = Cities.query.filter_by(id=result.city).first().name
                flash('Log in successful. Enjoy!', 'success')
                return redirect(url_for('items'))
            else:
                return render_template('login.html', error="Invalid password")
        else:
            return render_template('login.html', error="No user found")

    return render_template('login.html')


@app.route('/items')
@is_logged_in
def items():
    return render_template('items.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
