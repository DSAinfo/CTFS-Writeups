from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "muy secreta"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # CAMBIAR EL NOMBRE PARA CREAR OTRA DB (NO EDITAR EN BRANCH MASTER!)
db = SQLAlchemy(app)


class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


""" DESCOMENTAR PARA CREAR/CAMBIAR LA DB Y DESPUÉS DE UNA EJECUCIÓN VOLVER A COMENTAR (NO EDITAR EN BRANCH MASTER!)
db.create_all()
db.session.add(User(username='admin', password='admin'))
db.session.commit()
"""


@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('index.html', data="Bienvenido!")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        data = User.query.filter_by(username=name, password=passw).first()
        if data and name and passw:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Login incorrecto")


@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
