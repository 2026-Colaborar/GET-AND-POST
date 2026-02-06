from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "clave_secreta"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sistema_gestion"
)
cursor = db.cursor()

# ---------- LOGIN ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario=%s AND password=%s",
            (usuario, password)
        )
        user = cursor.fetchone()

        if user is not None:
            session["user"] = usuario
            return redirect("/dashboard")

    return render_template("login.html")

# ---------- REGISTRO ----------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        cursor.execute(
            "INSERT INTO usuarios (usuario, password) VALUES (%s, %s)",
            (usuario, password)
        )
        db.commit()
        return redirect("/")

    return render_template("registro.html")

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")

# ---------- CLIENTES ----------
@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        telefono = request.form["telefono"]

        cursor.execute(
            "INSERT INTO clientes (nombre, email, telefono) VALUES (%s, %s, %s)",
            (nombre, email, telefono)
        )
        db.commit()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    return render_template("clientes.html", clientes=clientes)


# ---------- EDITAR CLIENTE ----------
@app.route("/editar_cliente/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        telefono = request.form["telefono"]

        cursor.execute(
            "UPDATE clientes SET nombre=%s, email=%s, telefono=%s WHERE id=%s",
            (nombre, email, telefono, id)
        )
        db.commit()
        return redirect("/clientes")

    cursor.execute("SELECT * FROM clientes WHERE id=%s", (id,))
    cliente = cursor.fetchone()

    if cliente is None:
        return redirect("/clientes")

    return render_template("editar_cliente.html", cliente=cliente)

# ---------- ELIMINAR CLIENTE ----------
@app.route("/eliminar_cliente/<int:id>")
def eliminar_cliente(id):
    if "user" not in session:
        return redirect("/")

    cursor.execute("DELETE FROM clientes WHERE id=%s", (id,))
    db.commit()
    return redirect("/clientes")

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

