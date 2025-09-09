import requests

BASE_URL = "https://rapid-email-verifier.fly.dev/api/validate"

def validate_email(email: str) -> dict:
    """Validate a single email address."""
    response = requests.post(BASE_URL, json={"email": email})
    response.raise_for_status()
    return response.json()

def validate_batch(emails: list[str]):
    """Validate multiple emails by calling single validation for each."""
    if not emails:
        raise ValueError("Email list is empty.")
    if len(emails) > 100:
        raise ValueError("Batch limit exceeded: max 100 emails.")
    
    results = []
    for email in emails:
        try:
            result = validate_email(email)
            results.append(result)
        except Exception as e:
            results.append({
                "email": email,
                "validations": {},
                "score": 0,
                "status": f"ERROR: {str(e)}"
            })
    return results

def print_result(item: dict):
    """Helper to print results consistently."""
    print(f"Email: {item.get('email', '')}")
    print(" Validations:", item.get("validations", {}))
    print(" Score:", item.get("score"))
    print(" Status:", item.get("status"))
    print("-" * 40)

if __name__ == "__main__":
    choice = input("Do you want to validate a single email or multiple emails? (single/batch): ").strip().lower()

    if choice == "single":
        email = input("Enter the email address: ").strip()
        result = validate_email(email)
        print("\nValidation Result:")
        print_result(result)

    elif choice == "batch":
        raw_input_str = input("Enter multiple emails separated by commas: ").strip()
        emails = [e.strip() for e in raw_input_str.split(",") if e.strip()]
        results = validate_batch(emails)

        print("\nBatch Validation Results:")
        for item in results:
            print_result(item)

    else:
        print("Invalid choice. Please type 'single' or 'batch'.")
