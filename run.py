from myapp import app

app.secret_key="key123"                         # its a session key I think, its needed to secure the session !?

if __name__ == '__main__':
    app.run(debug=True)
