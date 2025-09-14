from flask import Flask, render_template, request, redirect, url_for
import pymysql
from validator.email_validator import validate_email, validate_batch
import import_ipynb 
from validator.spam_detector import classify_and_store_email 
import pickle
import os

# Load your spam_model and tfidf_vectorizer files
model_path = 'C:/CGI/Project/Email-Validation/ml_model/xgboost_model.pkl'
vectorizer_path = 'C:/CGI/Project/Email-Validation/ml_model/vectorizer.pkl'

with open(model_path, 'rb') as f:
    spam_model = pickle.load(f)

with open(vectorizer_path, 'rb') as f:
    tfidf_vectorizer = pickle.load(f)


app = Flask(__name__)

def db_connection():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="cgi@2025",
        database="email_validation"
    )
    return conn


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = db_connection()
        cursor = conn.cursor()

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
        except pymysql.Error as err:
            return f"Error: {err}"
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/landing")
def landing():
    return render_template('landing.html')



@app.route("/spam", methods=["GET", "POST"])
def spam():
    classification_result = None
    email_content = ""

    if request.method == "POST":
        email_content = request.form.get("message", "").strip()

        if email_content:
            result = classify_and_store_email(email_content)  # This runs prediction + saves to DB

            # Show combined results for both models
            classification_result = result["xgboost_prediction"]

    return render_template("spam.html", result=classification_result, email=email_content)


#email validation
@app.route("/validations", methods=["GET", "POST"])
def validations():
    result = None
    report = None

    if request.method == "POST":
        mode = request.form.get("mode")
        emails_input = request.form.get("emails", "").strip()

        if mode == "single":
            
            try:
                result = [validate_email(emails_input)]
            except Exception as e:
                result = [{"email": emails_input, "status": f"ERROR: {str(e)}"}]

        elif mode == "multiple":
            # Multiple email validation (comma-separated)
            emails = [e.strip() for e in emails_input.split(",") if e.strip()]
            try:
                result = validate_batch(emails)
            except Exception as e:
                result = [{"email": "Batch Error", "status": f"ERROR: {str(e)}"}]

        # Prepare a simple report
        if result:
            total = len(result)
            valid = sum(1 for r in result if r.get("status") == "valid" or r.get("status") == "Valid")
            invalid = total - valid
            report = {"total": total, "valid": valid, "invalid": invalid}

    return render_template("validation.html", result=result, report=report)

# integration for dashboard uncomment it once the integration is done

@app.route("/spam_dashboard")
def spam_dashboard():
     return render_template("spam_dashboard.html") # need to  change according to file name 

@app.route("/validation_dashboard")
def validation_dashboard():
     return render_template("email_dashboard.html") # need to change according to file name

# integration ends here

if __name__ == "__main__":
    app.run(debug=True)

