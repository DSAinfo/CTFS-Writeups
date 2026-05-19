from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import subprocess

app = Flask(__name__)
app.secret_key = 'muyfacil'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=="POST" and "ip" in request.form:
        ip = request.form['ip']
        command = "ping -c1 " + ip
        try:
          check_ping= subprocess.check_output(command, shell=True).decode("utf-8")
        except subprocess.CalledProcessError as e:
          check_ping="El host con la IP ingresada no responde"
        return render_template('index.html', result=check_ping)
    return render_template('index.html')


if __name__ == "__main__":
    # Define HOST and port
    app.run(host='0.0.0.0', port=8888, debug=True)

