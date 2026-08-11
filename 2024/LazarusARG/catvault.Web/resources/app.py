import random
import mariadb
from flask import (
    Flask,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
import db

app = Flask(__name__)
app.secret_key = random.randbytes(32)

DEFAULT_PREFS = {"theme": "light", "layout": "grid", "density": "cozy"}


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("vault"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", theme=session.get("theme", "light"))

    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    if not username or not password:
        flash("wtf do you think ur doing", "error")
        return redirect(url_for("register"))
    if len(username) > 32:
        flash("das too long", "error")
        return redirect(url_for("register"))

    try:
        user_id = db.create_user(username, password.encode())
    except mariadb.IntegrityError:
        flash("kitties can't all have the same name...", "error")
        return redirect(url_for("register"))

    session.clear()
    session["user_id"] = user_id
    session["username"] = username
    return redirect(url_for("vault"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", theme=session.get("theme", "light"))

    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""

    db.login(username, password.encode())
    row = db.cursor.fetchone()
    if row is None:
        flash("meowsername or pawssword incorrect", "error")
        return redirect(url_for("login"))

    user_id, name, _ = row
    session.clear()
    session["user_id"] = user_id
    session["username"] = name
    return redirect(url_for("vault"))


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/vault", methods=["GET", "POST"])
def vault():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        content = (request.form.get("content") or "").strip()
        if not content:
            flash("yap a bit more please", "error")
        elif len(content) > 2000:
            flash("didnt ask", "error")
        else:
            db.add_vault_entry(session["user_id"], content)
            flash("secret saved", "ok")
        return redirect(url_for("vault"))

    try:
        entries = db.get_vault_entries(session["user_id"])
    except mariadb.Error:
        entries = []
        flash("there's been a pawblem...", "error")

    return render_template(
        "vault.html",
        entries=entries,
        username=session.get("username", "cat"),
        theme=session.get("theme", "light"),
    )


@app.route("/api/settings", methods=["GET", "POST"])
def settings():
    if "user_id" not in session:
        abort(401)

    if request.method == "GET":
        prefs = {k: session.get(k, v) for k, v in DEFAULT_PREFS.items()}
        return jsonify(prefs)

    incoming = request.get_json(silent=True)
    if not isinstance(incoming, dict):
        abort(400)

    saved = {}
    for key, value in incoming.items():
        if not isinstance(key, str) or key.startswith("_") or not isinstance(value, str):
            continue
        session[key] = value
        saved[key] = value

    return jsonify({"ok": True, "saved": saved})


if __name__ == "__main__":
    db.connect()
    app.run(host="0.0.0.0", port=8080)
