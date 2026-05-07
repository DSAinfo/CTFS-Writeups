from flask import Flask, render_template, request, redirect, url_for
import random
import string
import base64
import os

app = Flask(__name__)

def generar_contrasena(longitud):
    caracteres = string.ascii_letters + string.digits
    contrasena = ''.join(random.choice(caracteres) for i in range(longitud))
    return contrasena

USUARIOS = [{"id": 1, "usuario": "user", "contrasena": "pass", "apellido": "Rodriguez", "nombre": "Juan", "tarjeta_credito": "5252-1412-4242-4444"},
            {"id": random.randint(31,100), "usuario": "admin", "contrasena": generar_contrasena(20), "apellido": "Tengo la flag", "nombre": "Flagger", "tarjeta_credito": os.environ.get("FLAG")}]

for i in range(1,30):
    usuario = {}
    usuario["id"] = i+1
    usuario["usuario"] = "usuario" + str(i + 1)
    usuario["contrasena"] = generar_contrasena(8)
    usuario["apellido"] = "Apellido" + str(i + 1)
    usuario["nombre"] = "Nombre" + str(i + 1)
    usuario["tarjeta_credito"] = str(random.randint(1000, 9999)) + "-" + str(random.randint(1000, 9999)) + "-" + str(random.randint(1000, 9999)) + "-" + str(random.randint(1000, 9999))
    USUARIOS.append(usuario)

# Renderiza la página de inicio
@app.route("/")
def index():
    return render_template("index.html")

# Renderiza la página de inicio de sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]
        for usuario_bd in USUARIOS:
            if usuario_bd["usuario"] == usuario and usuario_bd["contrasena"] == contrasena:
                return redirect(url_for("perfil", id=usuario_bd["id"]))
        error = "Nombre de usuario o contraseña incorrectos"
    return render_template("login.html", error=error)

# Renderiza la página de perfil
@app.route("/perfil/<int:id>", methods=["GET", "POST"])
def perfil(id):
    usuario_bd = None
    for usuario in USUARIOS:
        if usuario["id"] == id:
            usuario_bd = usuario
            break
    if usuario_bd is None:
        return redirect(url_for("login"))

    if request.method == "POST":
        usuario_bd["nombre"] = request.form["nombre"]
        usuario_bd["tarjeta_credito"] = request.form["tarjeta_credito"]
        return redirect(url_for("perfil", id=id))
    return render_template("perfil.html", usuario=usuario_bd)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)

