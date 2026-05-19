from flask import Flask, request, render_template_string,render_template
app = Flask(__name__)

@app.route('/')
def hello_ssti():
    person = {'name':"mundo",'secret':"RXN0YV9ub19lc19sYV9mbGFnLlRlbmVzX3F1ZV9hYnJpcl9lbF9hcmNoaXZvX3NlY3JldHMudHh0Cg=="}
    if request.args.get('nombre'):
        person['name'] = request.args.get('nombre')
    template = '''<!--Mandame la variable nombre--><h2>Hola %s!</h2>''' % person['name']
    return render_template_string(template, person=person)


def abrir_archivo(f_name):
    with open(f_name) as f:
        return f.readlines()

app.jinja_env.globals['abrir_archivo'] = abrir_archivo

if __name__ == "__main__":
    app.run(debug=True)
