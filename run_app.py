#!/usr/bin/env python3
"""
Script to run the Flask application with proper output
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    print("🚀 Starting Email Validation Dashboard...")
    print("=" * 50)
    print("🌐 Dashboard: http://127.0.0.1:5000/dashboard")
    print("📧 API: http://127.0.0.1:5000/api/emails")
    print("🔍 Validation: http://127.0.0.1:5000/validations")
    print("📧 Spam Detection: http://127.0.0.1:5000/spam")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Run the Flask app
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
    
except Exception as e:
    print(f"❌ Error starting Flask app: {e}")
    import traceback
    traceback.print_exc()
