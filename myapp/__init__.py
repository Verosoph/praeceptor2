from flask import Flask

app = Flask(__name__)



from myapp.home.view_home import mod

app.register_blueprint(home.view_home.mod)
