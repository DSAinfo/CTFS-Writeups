# Imports
from database import Database
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from sqlalchemy.sql import select
import hashlib

app = Flask(__name__)
app.secret_key = 'muyfacil'

db = Database()
db_user = os.getenv("DB_USER") if os.getenv("DB_USER") != None else "example"
db_pass = os.getenv("DB_PASS") if os.getenv("DB_PASS") != None else "example"
db_host = os.getenv("DB_HOST") if os.getenv("DB_HOST") != None else "db"
db_name = os.getenv("DB_NAME") if os.getenv("DB_NAME") != None else "wally"
db_port = os.getenv("DB_PORT") if os.getenv("DB_PORT") != None else "3306"

connection = 'mysql+mysqlconnector://%s:%s@%s:%s/%s' % (db_user,db_pass,db_host,db_port,db_name)
engine = create_engine(connection)
connection = engine.connect()
Session = sessionmaker(bind=engine)        
db_session = Session()




@app.route('/', methods=['GET', 'POST'])
def nivel1():
    if 'numero' in request.args:
        numero = request.args['numero']
        gatos_db=db.get_cat_by_id(numero)
    else:
        gatos_db=db.get_cat_by_id(1)
    return render_template('gatos.html',value=gatos_db)


if __name__ == "__main__":
    # Define HOST and port
    app.run(host='0.0.0.0', port=8888, debug=True)

