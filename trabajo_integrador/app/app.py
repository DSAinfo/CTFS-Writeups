import sqlite3
import os
from flask import Flask, request, render_template

app = Flask(__name__)

# Base de datos local en la carpeta del contenedor
DB_PATH = 'database.db'

def init_db():
    """Crea la base de datos y coloca la FLAG adentro de forma segura al iniciar."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Creamos la tabla de usuarios de juguete
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT ,
            role TEXT,
            secret_flag TEXT
        )
    ''')
    
    # Limpiamos datos viejos para evitar duplicados si el contenedor se reinicia
    cursor.execute("DELETE FROM users")
    
    # Insertamos los datos simulados y la FLAG que deben conseguir 
    cursor.execute("INSERT INTO users (id, username, role, secret_flag) VALUES (1, 'empleado_comun', 'user', 'Sigue buscando... la flag no esta aqui.')")
    cursor.execute("INSERT INTO users (id, username, role, secret_flag) VALUES (2, 'admin_sistema', 'administrator', 'FLAG{SQLi_D0ck3r_Succ3ss_2026}')")
    
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    user_data = None
    error = None
    
    if request.method == 'POST':
        search_id = request.form.get('user_id')
        
        # ⚠️ VULNERABILIDAD CRÍTICA INTENCIONAL: Concatenación directa de strings.
        # No se usan consultas preparadas, permitiendo SQL Injection basado en UNION.
        query = f"SELECT id, username, role FROM users WHERE id = {search_id}"
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Ejecuta la consulta rota del usuario, lo que permite inyección SQL
            cursor.execute(query)
            user_data = cursor.fetchall()
            conn.close()
        except Exception as e:
            # Mostramos el error para que el usuario sepa si rompió la sintaxis SQL
            error = f"Error en la consulta de base de datos: {str(e)}"
            
    return render_template('index.html', user_data=user_data, error=error)

if __name__ == '__main__':
    init_db()
    # Ejecutamos en modo producción (debug=False) para evitar fallos de RCE por consola interactiva
    app.run(host='0.0.0.0', port=5000, debug=False)
