#!/usr/bin/env python3
"""
Test script to add sample email validation data to the database
"""

import mysql.connector
from datetime import datetime

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="email_validation",
        auth_plugin="mysql_native_password"
    )

def add_sample_data():
    """Add sample email validation data to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Sample data
    sample_emails = [
        {
            "email": "test@example.com",
            "syntax_check": 1,
            "domain_exists": 1,
            "mx_records": 1,
            "mailbox_exists": 0,
            "is_disposable": 0,
            "is_role_based": 0,
            "score": 0.8,
            "status": "valid"
        },
        {
            "email": "admin@company.com",
            "syntax_check": 1,
            "domain_exists": 1,
            "mx_records": 1,
            "mailbox_exists": 1,
            "is_disposable": 0,
            "is_role_based": 1,
            "score": 0.9,
            "status": "valid"
        },
        {
            "email": "invalid-email",
            "syntax_check": 0,
            "domain_exists": 0,
            "mx_records": 0,
            "mailbox_exists": 0,
            "is_disposable": 0,
            "is_role_based": 0,
            "score": 0.0,
            "status": "invalid"
        },
        {
            "email": "spam@tempmail.com",
            "syntax_check": 1,
            "domain_exists": 1,
            "mx_records": 1,
            "mailbox_exists": 1,
            "is_disposable": 1,
            "is_role_based": 0,
            "score": 0.3,
            "status": "invalid"
        }
    ]
    
    sql = """
    INSERT INTO email_results 
    (email, syntax_check, domain_exists, mx_records, mailbox_exists, is_disposable, is_role_based, score, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    for email_data in sample_emails:
        try:
            cursor.execute(sql, (
                email_data["email"],
                email_data["syntax_check"],
                email_data["domain_exists"],
                email_data["mx_records"],
                email_data["mailbox_exists"],
                email_data["is_disposable"],
                email_data["is_role_based"],
                email_data["score"],
                email_data["status"]
            ))
            print(f"✅ Added: {email_data['email']}")
        except mysql.connector.Error as e:
            print(f"❌ Error adding {email_data['email']}: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("\n🎉 Sample data added successfully!")

if __name__ == "__main__":
    add_sample_data()
