from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

#Config MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'                  # here was a problem if you use localhost instead - always use 127.0.0.1
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'simple'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#init MySQL
mysql = MySQL(app)


from myapp.home.view_home import mod

app.register_blueprint(home.view_home.mod)
