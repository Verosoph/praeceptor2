from flask import Blueprint
from flask import render_template

from flask import flash, request, redirect, url_for, session, logging
from myapp import mysql

from flask_mysqldb import MySQL               # you have to install "flask-mysqldb" like this: pip install flask-mysqldb
                                                # ifyou get an error install like this: sudo apt install libmysqlclient-devls
                                                # a documentation you can find here: http://flask-mysqldb.readthedocs.io/en/latest/

from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps


mod = Blueprint('view_auth', __name__,template_folder='templates', static_folder='static')

@mod.route('/auth')
def auth():
    return render_template('view_auth.html')



# Register From Class
class RegisterForm(Form):                       # you will find the documentation here: https://wtforms.readthedocs.io/en/stable/forms.html#the-form-class
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=25)])
    password = PasswordField('Password', [
        validators.data_required(),
        validators.equal_to('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')



@mod.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #create cursor    like this here  http://flask-mysqldb.readthedocs.io/en/latest/
        cur = mysql.connection.cursor()

        #execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        #Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))      #return to index.html
    return render_template('register.html', form=form)

# UserLogin



@mod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        #get form fields
        username = request.form['username']
        password_candidate = request.form['password']

        #create cursor
        cur = mysql.connection.cursor()

        #get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s",[username])


        if result > 0:
            #get stored hash
            data = cur.fetchone()           # if there are more then on users he will take the first one
            password = data['password']

            #compare passwords
            if sha256_crypt.verify(password_candidate, password):            # compares the passwords
                #app.logger.info('PASSWORD MATCHED')                         # create an outout on console

                #if Passed
                session['logged_in'] = True                                     # comes from Flask, ist included above
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('desk.desk'))


            else:
                #app.logger.info('PASSWORD NOT MATCHED')
                error = 'Invalid login'
                return render_template('login.html', error=error)

            #Close connection
            cur.close()
        else:
            #app.logger.info('NO USER')
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


#check if user is logged in                                    #http://flask.pocoo.org/snippets/category/decorators/
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('view_auth.login'))
    return wrap


# Logout
@mod.route('/logout')
def logout():
    session.clear()
    flash('You are logged out', 'success')
    return redirect(url_for('view_auth.login'))