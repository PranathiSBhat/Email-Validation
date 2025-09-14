#!/usr/bin/env python3
"""
Script to create the database and table with correct schema
"""

import mysql.connector

def create_database_and_table():
    try:
        # Connect to MySQL server (without specifying database)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            auth_plugin="mysql_native_password"
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS email_validation")
        print("✅ Database 'email_validation' created/verified")
        
        # Use the database
        cursor.execute("USE email_validation")
        
        # Drop existing table if it exists
        cursor.execute("DROP TABLE IF EXISTS email_results")
        print("✅ Dropped existing table")
        
        # Create table with correct schema
        create_table_sql = """
        CREATE TABLE email_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            syntax_check TINYINT(1) DEFAULT 0,
            domain_exists TINYINT(1) DEFAULT 0,
            mx_records TINYINT(1) DEFAULT 0,
            mailbox_exists TINYINT(1) DEFAULT 0,
            is_disposable TINYINT(1) DEFAULT 0,
            is_role_based TINYINT(1) DEFAULT 0,
            score FLOAT DEFAULT 0.0,
            status VARCHAR(255) DEFAULT 'Unknown',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_sql)
        print("✅ Table 'email_results' created with correct schema")
        
        cursor.close()
        conn.close()
        print("🎉 Database setup completed successfully!")
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    create_database_and_table()
