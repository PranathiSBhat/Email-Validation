#!/usr/bin/env python3
"""
Script to populate the spam_results table with sample data for testing
"""

import mysql.connector
import random
from datetime import datetime, timedelta

def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="email_validation",
        auth_plugin="mysql_native_password"
    )

def populate_sample_data():
    """Populate the spam_results table with sample data"""
    
    # Sample spam and ham texts
    spam_texts = [
        "Congratulations! You've won $1000! Click here to claim your prize now!",
        "URGENT: Your account will be suspended unless you verify your information immediately!",
        "FREE MONEY! No strings attached! Get rich quick with this amazing opportunity!",
        "Limited time offer! 50% off all products! Order now before it's too late!",
        "You have been selected for a special promotion! Act now!",
        "Your credit card has been compromised. Click here to secure your account.",
        "Win a free iPhone! Just send us your personal information!",
        "Make money from home! Earn $5000 per week with this simple trick!",
        "Your subscription will expire soon. Renew now to avoid service interruption.",
        "Exclusive offer for you! Buy now and save 90% on all items!",
        "URGENT: Verify your account now or it will be permanently deleted!",
        "You have won a free vacation! Click here to claim your trip!",
        "Make $1000 per day working from home! No experience required!",
        "Your bank account has been locked. Click here to unlock immediately!",
        "Special discount! 75% off all items! Limited time only!",
        "You've been selected for a $500 cash prize! Claim now!",
        "Your email will be deleted in 24 hours unless you verify!",
        "Earn money fast! Get rich in 30 days with this secret method!",
        "Your payment failed. Click here to update your payment information!",
        "Congratulations! You're the 1,000,000th visitor! Claim your prize!"
    ]
    
    ham_texts = [
        "Hi, how are you doing today? I hope you're having a great week.",
        "Thanks for your email. I'll get back to you by tomorrow.",
        "The meeting has been scheduled for 3 PM tomorrow in the conference room.",
        "I wanted to follow up on our conversation from yesterday.",
        "Please find attached the document you requested.",
        "Let me know if you need any clarification on this matter.",
        "I hope you had a great weekend. Looking forward to working with you.",
        "The project deadline has been extended to next Friday.",
        "Could you please review the proposal and let me know your thoughts?",
        "I'll be out of office next week, but I'll respond to emails when I return.",
        "Thank you for your interest in our services. We'll contact you soon.",
        "The report you requested is ready for review.",
        "I wanted to confirm our appointment for next Tuesday at 2 PM.",
        "Please let me know if you have any questions about the project.",
        "I hope this email finds you well. I wanted to discuss the upcoming changes.",
        "Thank you for your patience. The issue has been resolved.",
        "I'm writing to follow up on our previous conversation about the budget.",
        "The team meeting has been moved to Thursday at 10 AM.",
        "I wanted to share some updates about the project status.",
        "Please confirm your attendance for the training session next week."
    ]
    
    try:
        conn = db_connection()
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM spam_results")
        print("Cleared existing data from spam_results table")
        
        # Insert sample spam data
        for text in spam_texts:
            cursor.execute(
                "INSERT INTO spam_results (email_text, xgboost_pred, created_at) VALUES (%s, %s, %s)",
                (text, 1, datetime.now() - timedelta(hours=random.randint(1, 24)))
            )
        
        # Insert sample ham data
        for text in ham_texts:
            cursor.execute(
                "INSERT INTO spam_results (email_text, xgboost_pred, created_at) VALUES (%s, %s, %s)",
                (text, 0, datetime.now() - timedelta(hours=random.randint(1, 24)))
            )
        
        conn.commit()
        print(f"✅ Inserted {len(spam_texts)} spam samples and {len(ham_texts)} ham samples")
        
        # Verify the data
        cursor.execute("SELECT COUNT(*) FROM spam_results")
        total_count = cursor.fetchone()[0]
        print(f"Total records in spam_results: {total_count}")
        
        cursor.execute("SELECT COUNT(*) FROM spam_results WHERE xgboost_pred = 1")
        spam_count = cursor.fetchone()[0]
        print(f"Spam records: {spam_count}")
        
        cursor.execute("SELECT COUNT(*) FROM spam_results WHERE xgboost_pred = 0")
        ham_count = cursor.fetchone()[0]
        print(f"Ham records: {ham_count}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Sample data populated successfully!")
        print("You can now test the dashboard at: http://127.0.0.1:5000/spam-dashboard")
        
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("📊 Populating spam_results table with sample data...")
    print("=" * 50)
    populate_sample_data()

