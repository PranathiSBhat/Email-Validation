#!/usr/bin/env python3
"""
Script to set up the spam detection database table
"""

import mysql.connector

def create_spam_table():
    """Create the spam_results table in the database"""
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="email_validation",
            auth_plugin="mysql_native_password"
        )
        cursor = conn.cursor()
        
        # Create spam_results table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS spam_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email_text TEXT NOT NULL,
            naive_bayes_pred TINYINT,
            xgboost_pred TINYINT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_sql)
        print("✅ Table 'spam_results' created/verified")
        
        cursor.close()
        conn.close()
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    print("Setting up spam detection database...")
    if create_spam_table():
        print("🎉 Spam detection database setup completed!")
    else:
        print("❌ Failed to setup spam detection database")
