#!/usr/bin/env python3
"""
Simple Flask test to debug the issue
"""

from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

def db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="email_validation"
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route("/api/emails", methods=["GET"])
def get_emails():
    try:
        conn = db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"})
            
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM email_results ORDER BY created_at DESC")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/")
def home():
    return "Email Validation API is running!"

if __name__ == "__main__":
    print("🚀 Starting simple Flask test...")
    print("🌐 API: http://127.0.0.1:5000/api/emails")
    print("🏠 Home: http://127.0.0.1:5000/")
    print("Press Ctrl+C to stop")
    app.run(debug=True, host='127.0.0.1', port=5000)
