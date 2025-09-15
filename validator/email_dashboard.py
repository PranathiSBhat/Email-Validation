import json
from utils.db_utils import db_connection

def fetch_email_validation_results():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM email_results WHERE DATE(created_at) = CURDATE() ORDER BY created_at DESC") # current date data is extracted
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    parsed_results = []

    for row in rows:
        validations = {}
        try:
            validations = json.loads(row['validations']) if row['validations'] else {}
        except Exception as e:
            print(f"Error parsing JSON for email {row['email']}: {e}")

        parsed_results.append({
            "email": row["email"],
            "status": row["status"],
            "score": row.get("score"),
            "syntax_check": validations.get("syntax", "-"),
            "domain_exists": validations.get("domain_exists", "-"),
            "mx_records": validations.get("mx_records", "-"),
            "mailbox_exists": validations.get("mailbox_exists", "-"),
            "is_disposable": validations.get("is_disposable", "-"),
            "is_role_based": validations.get("is_role_based", "-"),
            "created_at": row.get("created_at")
        })

    return parsed_results
