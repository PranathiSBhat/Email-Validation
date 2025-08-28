import requests

BASE_URL = "https://rapid-email-verifier.fly.dev/api/validate"

def validate_email(email: str) -> dict:
    """Validate a single email address."""
    response = requests.post(BASE_URL, json={"email": email})
    response.raise_for_status()
    return response.json()

def validate_batch(emails: list[str]):
    """Validate a batch of emails (max 100)."""
    if not emails:
        raise ValueError("Email list is empty.")
    if len(emails) > 100:
        raise ValueError("Batch limit exceeded: max 100 emails.")
    
    # Try sending as list of dicts (as API may expect this format)
    payload = {"emails": [{"email": e} for e in emails]}
    response = requests.post(BASE_URL, json=payload)
    response.raise_for_status()
    data = response.json()
    
    print("\nDEBUG Raw batch response:", data)  # Debug line
    return data

if __name__ == "__main__":
    choice = input("Do you want to validate a single email or multiple emails? (single/batch): ").strip().lower()

    if choice == "single":
        email = input("Enter the email address: ").strip()
        result = validate_email(email)
        print("\nValidation Result:")
        print(result)

    elif choice == "batch":
        raw_input = input("Enter multiple emails separated by commas: ").strip()
        emails = [e.strip() for e in raw_input.split(",") if e.strip()]
        results = validate_batch(emails)

        print("\nBatch Validation Results:")

        # If API returns a list
        if isinstance(results, list):
            for item in results:
                print(f"Email: {item.get('email', '')}")
                print(" Validations:", item.get("validations", {}))
                print(" Score:", item.get("score"))
                print(" Status:", item.get("status"))
                print("-" * 40)

        # If API returns a dict with 'emails' or 'results'
        elif isinstance(results, dict):
            for key, value in results.items():
                # Sometimes key is "results", sometimes directly the email
                if isinstance(value, dict):
                    print(f"Email: {value.get('email', key)}")
                    print(" Validations:", value.get("validations", {}))
                    print(" Score:", value.get("score"))
                    print(" Status:", value.get("status"))
                    print("-" * 40)
                elif isinstance(value, list):
                    for item in value:
                        print(f"Email: {item.get('email', '')}")
                        print(" Validations:", item.get("validations", {}))
                        print(" Score:", item.get("score"))
                        print(" Status:", item.get("status"))
                        print("-" * 40)

        else:
            print("Unexpected batch response format:", results)

    else:
        print("Invalid choice. Please type 'single' or 'batch'.")
