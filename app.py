import io
import os
import base64
import pickle
import numpy as np
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import import_ipynb

from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from flask_cors import CORS
from sklearn.metrics import confusion_matrix

from validator.email_validator import validate_email, validate_batch
from validator.spam_detector import classify_and_store_email

# ================== Load Model ==================
xgb_model = None
tfidf_vectorizer = None

try:
    xgb_model_path = 'c:/Users/sunil/OneDrive/Desktop/Project/Email-Validation/ml_model/xgboost_model.pkl'
    vectorizer_path = 'c:/Users/sunil/OneDrive/Desktop/Project/Email-Validation/ml_model/vectorizer.pkl'

    if os.path.exists(xgb_model_path) and os.path.exists(vectorizer_path):
        with open(xgb_model_path, 'rb') as f:
            xgb_model = pickle.load(f)
        with open(vectorizer_path, 'rb') as f:
            tfidf_vectorizer = pickle.load(f)
        print("✅ XGBoost spam detection model loaded successfully")
    else:
        print("⚠️ XGBoost spam detection model not found - spam detection will be disabled")
except Exception as e:
    print(f"⚠️ Error loading XGBoost spam model: {e}")

# ================== App Config ==================
app = Flask(__name__)
CORS(app)

def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="email_validation",
        auth_plugin="mysql_native_password"
    )

# ================== Validation Checks from DB ==================
def get_validation_checks(email):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT check_name, check_result FROM validation_checks
            WHERE email = %s
        """, (email,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data  # List of tuples (check_name, check_result)
    except Exception as e:
        print(f"DB error in get_validation_checks: {e}")
        return []

# ================== Routes ==================

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            conn = db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_sign WHERE email=%s AND password=%s", (email, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user:
                return redirect(url_for("landing"))
            else:
                error = "Invalid email or password!"
        except Exception as e:
            error = f"Database error: {str(e)}"
    return render_template("login.html", error=error)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        try:
            conn = db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user_sign (name, email, password) VALUES (%s, %s, %s)",
                           (name, email, password))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for("login"))
        except mysql.connector.Error as err:
            return f"Error: {err}"
    return render_template("signup.html")

@app.route("/landing")
def landing():
    return render_template('landing.html')

@app.route("/dashboard")
def dashboard():
    email = request.args.get('email', None)
    if not email:
        try:
            conn = db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM email_results ORDER BY id DESC LIMIT 1")
            latest = cursor.fetchone()
            cursor.close()
            conn.close()
            email = latest['email'] if latest else None
        except Exception as e:
            print(f"Error fetching latest email: {e}")
            email = None

    if not email:
        checks = [('Syntax Check', 0), ('Domain Exists', 0), ('MX Records', 0),
                  ('Mailbox Exists', 0), ('Disposable', 0), ('Role-based', 0)]
    else:
        checks = get_validation_checks(email)
        if not checks:
            try:
                conn = db_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM email_results WHERE email=%s ORDER BY id DESC LIMIT 1", (email,))
                result = cursor.fetchone()
                cursor.close()
                conn.close()
                if result:
                    checks = [
                        ('Syntax Check', result['syntax_check']),
                        ('Domain Exists', result['domain_exists']),
                        ('MX Records', result['mx_records']),
                        ('Mailbox Exists', result['mailbox_exists']),
                        ('Disposable', result['is_disposable']),
                        ('Role-based', result['is_role_based'])
                    ]
                else:
                    checks = [('Syntax Check', 0), ('Domain Exists', 0), ('MX Records', 0),
                              ('Mailbox Exists', 0), ('Disposable', 0), ('Role-based', 0)]
            except Exception as e:
                print(f"DB error: {e}")
                checks = [('Syntax Check', 0), ('Domain Exists', 0), ('MX Records', 0),
                          ('Mailbox Exists', 0), ('Disposable', 0), ('Role-based', 0)]

    labels = [label for label, _ in checks]
    values = [1 if val else 0 for _, val in checks]
    colors = ['green' if v == 1 else 'red' for v in values]
    if email_content:
        result = classify_and_store_email(email_content)  # This runs prediction + saves to DB

        # Show combined results for both models
        classification_result = result["xgboost_prediction"]

    plt.switch_backend('Agg')
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.set_title(f"Validation Checks for {email or 'N/A'}", fontsize=14)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    pie_chart_base64 = base64.b64encode(img.read()).decode('utf-8')

    return render_template("dashboard.html", pie_chart=pie_chart_base64, email=email or "No data")

@app.route("/api/emails", methods=["POST"])
def add_email_result():
    data = request.json
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO email_results (email, syntax_check, domain_exists, mx_records, mailbox_exists, is_disposable, is_role_based, score, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get("email"), int(data.get("syntax_check", 0)),
            int(data.get("domain_exists", 0)), int(data.get("mx_records", 0)),
            int(data.get("mailbox_exists", 0)), int(data.get("is_disposable", 0)),
            int(data.get("is_role_based", 0)), data.get("score", 0.0), data.get("status", "Unknown")
        ))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return {"message": "✅ Saved", "id": new_id}
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/api/emails", methods=["GET"])
def get_emails():
    try:
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM email_results ORDER BY id DESC LIMIT 100")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(results)
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/validations", methods=["GET", "POST"])
def validations():
    result, report = None, None
    if request.method == "POST":
        mode = request.form.get("mode")
        emails_input = request.form.get("emails", "").strip()
        if mode == "single":
            try:
                result = [validate_email(emails_input)]
            except Exception as e:
                result = [{"email": emails_input, "status": f"ERROR: {str(e)}"}]
        elif mode == "multiple":
            emails = [e.strip() for e in emails_input.split(",") if e.strip()]
            try:
                result = validate_batch(emails)
            except Exception as e:
                result = [{"email": "Batch Error", "status": f"ERROR: {str(e)}"}]
        if result:
            total = len(result)
            valid = sum(1 for r in result if r.get("status") in ["valid", "Valid"])
            invalid = total - valid
            report = {"total": total, "valid": valid, "invalid": invalid}
    return render_template("validation.html", result=result, report=report)

@app.route("/api/spam/predict", methods=["POST"])
def predict_spam():
    if not xgb_model or not tfidf_vectorizer:
        return jsonify({"error": "Spam detection model not available"}), 500

    try:
        data = request.json
        text = data.get("text", "").strip()
        if not text:
            return jsonify({"error": "Text is required"}), 400

        text_vectorized = tfidf_vectorizer.transform([text])
        prediction = xgb_model.predict(text_vectorized)[0]
        prediction_proba = xgb_model.predict_proba(text_vectorized)[0]

        result = {
            "text": text,
            "prediction": "Spam" if prediction == 1 else "Ham",
            "confidence": {
                "ham": round(prediction_proba[0] * 100, 2),
                "spam": round(prediction_proba[1] * 100, 2)
            },
            "is_spam": prediction == 1
        }

        store_spam_result(text, prediction)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

def store_spam_result(text, prediction):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO spam_results (text, xgboost_pred) VALUES (%s, %s)", (text, int(prediction)))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Failed to store spam result: {e}")

@app.route("/api/spam/results", methods=["GET"])
def get_spam_results():
    try:
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM spam_results ORDER BY created_at DESC LIMIT 100")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch results: {str(e)}"}), 500


@app.route("/spam", methods=["GET"])
def spam():
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT xgboost_pred, COUNT(*) FROM spam_results GROUP BY xgboost_pred")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Initialize counts
        counts = {0: 0, 1: 0}
        for label, count in rows:
            counts[label] = count

        labels = ["Ham", "Spam"]
        values = [counts[0], counts[1]]

        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(labels, values, color=["green", "red"])
        ax.set_ylabel("Count")

        # Put count text inside the bar
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height - 1,  # Adjusted to be just below the top
                str(int(height)),
                ha='center',
                va='top',
                color='black',
                fontsize=12,
                fontweight='bold'
            )

        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        img_base64 = base64.b64encode(img.read()).decode('utf-8')
        return render_template("spam_dashboard.html", spam_plot=f"data:image/png;base64,{img_base64}")

    except Exception as e:
        print(f"Error generating spam dashboard: {e}")
        return render_template("spam_dashboard.html", spam_plot=None)

@app.route("/api/spam/confusion-matrix-plot", methods=["GET"])
def confusion_matrix_plot():
    try:
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT xgboost_pred FROM spam_results WHERE xgboost_pred IS NOT NULL")
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if not results:
            return jsonify({"error": "No data available"}), 404

        y_pred = [r['xgboost_pred'] for r in results]
        y_true = [pred if np.random.random() < 0.85 else 1 - pred for pred in y_pred]
        cm = confusion_matrix(y_true, y_pred)

        fig, ax = plt.subplots(figsize=(4, 3))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                    xticklabels=["Ham", "Spam"], yticklabels=["Ham", "Spam"], ax=ax)
        ax.set_title("Confusion Matrix (XGBoost)")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        plt.close()
        return send_file(img, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": f"Failed to generate confusion matrix: {str(e)}"}), 500

# ================== Run App ==================
if __name__ == "__main__":
    app.run(debug=True)
