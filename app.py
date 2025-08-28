from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="capstone_project"
    )
    return conn

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = db_connection()
        cursor = conn.cursor(dictionary=True)

        # fetch user by email and password
        cursor.execute("SELECT * FROM user_sign WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            return redirect(url_for("landing"))
        else:
            error = "Invalid email or password!"

    return render_template("login.html",error=error)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # collecting the data
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO user_sign (name, email, password) VALUES (%s, %s, %s)",
                (name, email, password),
            )
            conn.commit()
        except mysql.connector.Error as err:
            return f"Error: {err}"
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/landing")
def landing():
    return render_template('landing.html')

@app.route("/spam")
def spam():
    return render_template('spam.html')

@app.route("/validations")
def validations():
    return render_template("validations.html")


if __name__ == "__main__":
    app.run(debug=True)
