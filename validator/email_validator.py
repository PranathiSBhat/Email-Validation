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
    
    # The API does not return per-email results for batch, so validate each email individually
    results = []
    for email in emails:
        res = validate_email(email)
        results.append(res)
    print("\nDEBUG Raw batch response:", results)  # Debug line
    return results

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
        emails_data = []
        # Try to extract list of email results from common keys
        if isinstance(results, list):
            emails_data = results
        elif isinstance(results, dict):
            # Look for 'results', 'emails', or values that are lists
            if 'results' in results and isinstance(results['results'], list):
                emails_data = results['results']
            elif 'emails' in results and isinstance(results['emails'], list):
                emails_data = results['emails']
            else:
                # Sometimes dict values are emails
                for v in results.values():
                    if isinstance(v, list):
                        emails_data.extend(v)
                    elif isinstance(v, dict) and 'email' in v:
                        emails_data.append(v)
        # Print per-email results
        if emails_data:
            for item in emails_data:
                print(f"Email: {item.get('email', '')}")
                print(" Validations:", item.get("validations", {}))
                print(" Score:", item.get("score"))
                print(" Status:", item.get("status"))
                print("-" * 40)
        else:
            print("No per-email results found. Raw response:", results)

    else:
        print("Invalid choice. Please type 'single' or 'batch'.")
