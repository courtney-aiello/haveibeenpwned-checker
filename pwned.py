import os
import requests

# Load API Key
API_KEY = os.getenv("HIBP_API_KEY")

# Check API key
if not API_KEY:
    raise ValueError("Missing API Key")

# HIBP API URL
HIBP_URL = "https://haveibeenpwned.com/api/v3/breachedaccount/"


# Headers
HEADERS = {
    "hibp-api-key": API_KEY,
    "User-Agent": "OSINT-SecurityScript",
    "Accept": "application/json"
}

# Function to chack email for breaches
def check_email_breach(email):
    try:
        response = requests.get(f"{HIBP_URL}{email}", headers=HEADERS)

        if response.status_code == 200:
            breaches = response.json()
            print(f"\n[!] The email {email} was found in {len(breaches)} breaches. \n")

            # Save results to file
            with open("hibp_results.txt", "w") as file:
                for breach in breaches:
                    file.write(f"Breach: {breach['Name']}\n")
                    file.write(f"Domain: {breach['Domain']}\n")
                    file.write(f"Date: {breach['BreachDate']}\n")
                    file.write(f"Data Compromised: {',  '.join(breach['DataClasses'])}\n")
                    file.write("=" * 50 + "\n")
            print("[+] Results saved to hipb_results.txt")

        elif response.status_code == 404:
            print(f"[+] No breaches found for {email}. ")
        else:
            print(f"[!] Error: {response.status_code}, {response.text}")

    except requests.RequestException as e:
        print(f"[!] Network error: {e}")

# Function for user input
if __name__ == "__main__":
    email_to_check = input("Enter email to check: ")
    check_email_breach(email_to_check)