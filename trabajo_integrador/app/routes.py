from flask import Flask, request, render_template_string

app = Flask(__name__)

# Ruta vulnerable a SQL Injection 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        password = request.form.get("password")
        # Vulnerabilidad: concatenación directa
        query = f"SELECT * FROM users WHERE username='{user}' AND password='{password}'"
        return f"Ejecutando consulta: {query}"
    return '''
        <form method="post">
            Usuario: <input name="username"><br>
            Contraseña: <input name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

# Ruta vulnerable a XSS
@app.route("/comentario", methods=["GET", "POST"])
def comentario():
    if request.method == "POST":
        texto = request.form.get("texto")
        return render_template_string(f"<h2>Comentario recibido:</h2><p>{texto}</p>")
    return '''
        <form method="post">
            Comentario: <input name="texto"><br>
            <input type="submit" value="Enviar">
        </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
